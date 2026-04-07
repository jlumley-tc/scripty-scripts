#!/usr/bin/env python3
"""
Benchmark the two-step Elasticsearch flow:

1. Root query:
   - fetch root transactions for an account
   - last 6 months
   - no related_product_transaction_uuid
   - sorted by transaction_date desc, brand_transaction_id asc

2. Sub query:
   - fetch tax transactions for the same account
   - same date range
   - transaction_type in [network_tax, non_network_tax]
   - related_product_transaction_uuid in root brand_transaction_ids from query 1

Usage:
  ES_API_KEY=YOUR_API_KEY uv run python bench_es_two_step.py \
    --base-url http://localhost:9200 \
    --index datastream-search-account-history-financial-transaction-0 \
    --account c6390c71-c36f-4de3-adc7-7069a30f3843 \
    --iterations 10 \
    --range 6m \
    --root-size 50 \
    --sub-multiplier 2 \
    --target-ips 10 \
    --max-concurrency 10 \
    --request-cache false

Or from a file:
  ES_API_KEY=YOUR_API_KEY uv run python bench_es_two_step.py \
    --base-url http://localhost:9200 \
    --accounts-file accounts.txt
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class IterationResult:
    account_uuid: str
    iteration: int
    root_wall_ms: float
    root_es_took_ms: int | None
    root_ttfb_ms: float
    root_read_ms: float
    root_decode_ms: float
    root_hits: int
    root_brand_ids: int
    sub_wall_ms: float
    sub_es_took_ms: int | None
    sub_ttfb_ms: float
    sub_read_ms: float
    sub_decode_ms: float
    sub_hits: int
    total_wall_ms: float


def iso_utc(dt: datetime) -> str:
    return (
        dt.astimezone(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def build_root_query(
    account_uuid: str, start_date: str, end_date: str, size: int
) -> dict[str, Any]:
    return {
        "size": size,
        "_source": True,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"mse_account_uuid": account_uuid}},
                    {"terms": {"status": ["completed", "draft"]}},
                    {
                        "range": {
                            "transaction_date": {
                                "gte": start_date,
                                "lte": end_date,
                            }
                        }
                    },
                ],
                "must_not": [{"exists": {"field": "related_product_transaction_uuid"}}],
            }
        },
        "sort": [
            {"transaction_date": {"order": "desc"}},
            {"brand_transaction_id": {"order": "asc"}},
        ],
    }


def build_sub_query(
    account_uuid: str,
    start_date: str,
    end_date: str,
    root_brand_ids: list[str],
    size: int,
) -> dict[str, Any]:
    return {
        "size": size,
        "_source": True,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"mse_account_uuid": account_uuid}},
                    {"terms": {"status": ["completed", "draft"]}},
                    # {"terms": {"transaction_type": ["network_tax", "non_network_tax"]}},
                    {
                        "range": {
                            "transaction_date": {
                                "gte": start_date,
                                "lte": end_date,
                            }
                        }
                    },
                    {"terms": {"related_product_transaction_uuid": root_brand_ids}},
                ]
            }
        },
        "sort": [
            {"transaction_date": {"order": "asc"}},
            {"related_product_transaction_uuid": {"order": "asc"}},
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark two-step Elasticsearch transaction flow."
    )
    parser.add_argument(
        "--base-url",
        required=False,
        default="https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems",
        help="Base Elasticsearch URL, e.g. http://localhost:9200",
    )
    parser.add_argument(
        "--index",
        default="datastream-search-account-history-financial-transaction-0",
        help="Index or data stream name",
    )
    parser.add_argument(
        "--account",
        action="append",
        default=[],
        help="Account UUID to test. Repeat for multiple accounts.",
    )
    parser.add_argument(
        "--accounts-file",
        help="Optional file with one account UUID per line.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Measured runs per account",
    )
    parser.add_argument(
        "--root-size",
        type=int,
        default=100,
        help="Root query size",
    )
    parser.add_argument(
        "--sub-multiplier",
        type=float,
        default=2.0,
        help="Sub query size multiplier (sub_size = root_size * multiplier)",
    )
    parser.add_argument(
        "--request-cache",
        choices=["true", "false"],
        default="false",
        help="Set request_cache query parameter",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds",
    )
    parser.add_argument(
        "--range",
        default="6m",
        help="Date range in months, e.g. 1m, 3m, 18m",
    )
    parser.add_argument(
        "--target-ips",
        type=float,
        default=120.0,
        help="Target iterations per second across all accounts",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=1000,
        help="Maximum in-flight iterations",
    )
    parser.add_argument(
        "--max-connections",
        type=int,
        default=1000,
        help="Maximum total HTTP connections for the httpx client",
    )
    parser.add_argument(
        "--max-keepalive-connections",
        type=int,
        default=1000,
        help="Maximum keepalive HTTP connections for the httpx client",
    )
    parser.add_argument(
        "--api-key-env",
        default="ES_API_KEY",
        help="Env var name that holds the Elasticsearch API key",
    )
    parser.add_argument(
        "--pretty-root-query",
        action="store_true",
        help="Print the generated root query for the first account and exit.",
    )
    parser.add_argument(
        "--pretty-sub-query",
        action="store_true",
        help="Print an example generated sub query for the first account and exit.",
    )
    parser.add_argument(
        "--report-md",
        default=None,
        help="Write a markdown summary report to this path",
    )
    parser.add_argument(
        "--routing",
        action="store_true",
        help="Enable routing using the account UUID",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress to stdout",
    )
    parser.add_argument(
        "--debug-auth",
        action="store_true",
        help="Print auth header info (no secrets).",
    )
    return parser.parse_args()


def load_accounts(args: argparse.Namespace) -> list[str]:
    accounts = list(args.account)

    if args.accounts_file:
        with open(args.accounts_file, "r", encoding="utf-8") as f:
            for line in f:
                value = line.strip()
                if value and not value.startswith("#"):
                    accounts.append(value)

    deduped = list(dict.fromkeys(accounts))
    if not deduped:
        raise SystemExit("No accounts supplied. Use --account and/or --accounts-file.")
    return deduped


class HttpError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code


async def fetch_json(
    client: httpx.AsyncClient,
    url: str,
    query: dict[str, Any],
    timeout: float,
) -> tuple[dict[str, Any], float, float, float, float]:
    start = time.perf_counter()
    ttfb_ms: float | None = None
    read_start: float | None = None
    body_chunks: list[bytes] = []

    async with client.stream("POST", url, json=query, timeout=timeout) as response:
        async for chunk in response.aiter_bytes():
            if ttfb_ms is None:
                ttfb_ms = (time.perf_counter() - start) * 1000.0
                read_start = time.perf_counter()
            body_chunks.append(chunk)

        if ttfb_ms is None:
            ttfb_ms = (time.perf_counter() - start) * 1000.0
            read_start = time.perf_counter()

        read_ms = (time.perf_counter() - read_start) * 1000.0 if read_start else 0.0
        total_ms = (time.perf_counter() - start) * 1000.0
        body = b"".join(body_chunks)

        if response.status_code >= 400:
            snippet = body[:400].decode("utf-8", errors="replace").replace("\n", " ")
            raise HttpError(response.status_code, snippet)

    decode_start = time.perf_counter()
    try:
        payload = json.loads(body.decode("utf-8")) if body else {}
    except json.JSONDecodeError as exc:
        snippet = body[:400].decode("utf-8", errors="replace").replace("\n", " ")
        raise HttpError(0, f"Invalid JSON: {exc} | {snippet}") from exc
    decode_ms = (time.perf_counter() - decode_start) * 1000.0

    return payload, ttfb_ms, read_ms, decode_ms, total_ms


def extract_root_brand_ids(payload: dict[str, Any]) -> list[str]:
    hits = payload.get("hits", {}).get("hits", [])
    root_types = {"network_charge", "non_network_charge"}

    brand_ids: list[str] = []
    seen: set[str] = set()

    for hit in hits:
        source = hit.get("_source", {})
        txn_type = source.get("transaction_type")
        brand_id = source.get("brand_transaction_id")

        if (
            txn_type in root_types
            and isinstance(brand_id, str)
            and brand_id
            and brand_id not in seen
        ):
            seen.add(brand_id)
            brand_ids.append(brand_id)

    return brand_ids


def hit_count(payload: dict[str, Any]) -> int:
    total = payload.get("hits", {}).get("total", {})
    if isinstance(total, dict):
        return int(total.get("value", 0))
    return int(total or 0)


def build_report_table(results: list[IterationResult]) -> str:
    root_wall = [r.root_wall_ms for r in results]
    sub_wall = [r.sub_wall_ms for r in results]
    total_wall = [r.total_wall_ms for r in results]
    root_es = [r.root_es_took_ms for r in results if r.root_es_took_ms is not None]
    sub_es = [r.sub_es_took_ms for r in results if r.sub_es_took_ms is not None]
    root_ttfb = [r.root_ttfb_ms for r in results]
    root_read = [r.root_read_ms for r in results]
    root_decode = [r.root_decode_ms for r in results]
    sub_ttfb = [r.sub_ttfb_ms for r in results]
    sub_read = [r.sub_read_ms for r in results]
    sub_decode = [r.sub_decode_ms for r in results]
    root_counts = [r.root_hits for r in results]
    sub_counts = [r.sub_hits for r in results]
    brand_counts = [r.root_brand_ids for r in results]

    def mean_or_blank(values: list[float | int]) -> str:
        return f"{statistics.mean(values):.2f}" if values else ""

    def min_max(values: list[float]) -> str:
        return f"{min(values):.2f} / {max(values):.2f}" if values else ""

    def unique_list(values: list[int]) -> str:
        return ", ".join(str(v) for v in sorted(set(values))) if values else ""

    def percentile(values: list[float], p: float) -> str:
        if not values:
            return ""
        sorted_values = sorted(values)
        rank = max(0, math.ceil((p / 100.0) * len(sorted_values)) - 1)
        return f"{sorted_values[rank]:.2f}"

    rows = [
        ("Runs", str(len(results))),
        ("Root avg wall (ms)", mean_or_blank(root_wall)),
        ("Root min/max wall (ms)", min_max(root_wall)),
        ("Root p50 wall (ms)", percentile(root_wall, 50)),
        ("Root p90 wall (ms)", percentile(root_wall, 90)),
        ("Root p99 wall (ms)", percentile(root_wall, 99)),
        ("Root avg TTFB (ms)", mean_or_blank(root_ttfb)),
        ("Root p50 TTFB (ms)", percentile(root_ttfb, 50)),
        ("Root p90 TTFB (ms)", percentile(root_ttfb, 90)),
        ("Root p99 TTFB (ms)", percentile(root_ttfb, 99)),
        ("Root avg read (ms)", mean_or_blank(root_read)),
        ("Root p50 read (ms)", percentile(root_read, 50)),
        ("Root p90 read (ms)", percentile(root_read, 90)),
        ("Root p99 read (ms)", percentile(root_read, 99)),
        ("Root avg decode (ms)", mean_or_blank(root_decode)),
        ("Root p50 decode (ms)", percentile(root_decode, 50)),
        ("Root p90 decode (ms)", percentile(root_decode, 90)),
        ("Root p99 decode (ms)", percentile(root_decode, 99)),
        ("Sub avg wall (ms)", mean_or_blank(sub_wall)),
        ("Sub min/max wall (ms)", min_max(sub_wall)),
        ("Sub p50 wall (ms)", percentile(sub_wall, 50)),
        ("Sub p90 wall (ms)", percentile(sub_wall, 90)),
        ("Sub p99 wall (ms)", percentile(sub_wall, 99)),
        ("Sub avg TTFB (ms)", mean_or_blank(sub_ttfb)),
        ("Sub p50 TTFB (ms)", percentile(sub_ttfb, 50)),
        ("Sub p90 TTFB (ms)", percentile(sub_ttfb, 90)),
        ("Sub p99 TTFB (ms)", percentile(sub_ttfb, 99)),
        ("Sub avg read (ms)", mean_or_blank(sub_read)),
        ("Sub p50 read (ms)", percentile(sub_read, 50)),
        ("Sub p90 read (ms)", percentile(sub_read, 90)),
        ("Sub p99 read (ms)", percentile(sub_read, 99)),
        ("Sub avg decode (ms)", mean_or_blank(sub_decode)),
        ("Sub p50 decode (ms)", percentile(sub_decode, 50)),
        ("Sub p90 decode (ms)", percentile(sub_decode, 90)),
        ("Sub p99 decode (ms)", percentile(sub_decode, 99)),
        ("Total avg wall (ms)", mean_or_blank(total_wall)),
        ("Total min/max (ms)", min_max(total_wall)),
        ("Total p50 wall (ms)", percentile(total_wall, 50)),
        ("Total p90 wall (ms)", percentile(total_wall, 90)),
        ("Total p99 wall (ms)", percentile(total_wall, 99)),
        ("Root avg ES took (ms)", mean_or_blank(root_es)),
        ("Sub avg ES took (ms)", mean_or_blank(sub_es)),
        ("Root hits (unique)", unique_list(root_counts)),
        ("Root brand IDs (unique)", unique_list(brand_counts)),
        ("Sub hits (unique)", unique_list(sub_counts)),
    ]

    lines = ["| Metric | Value |", "| --- | --- |"]
    lines.extend([f"| {label} | {value} |" for label, value in rows])
    lines.append("")
    return "\n".join(lines)


def build_report(
    base_url: str,
    index: str,
    start_date: str,
    end_date: str,
    root_size: int,
    sub_multiplier: float,
    sub_size: int,
    iterations: int,
    request_cache: str,
    range_value: str,
    routing_enabled: bool,
    target_ips: float,
    achieved_ips: float | None,
    max_concurrency: int,
    all_results: list[IterationResult],
    sample_root_query: dict[str, Any] | None,
    sample_sub_query: dict[str, Any] | None,
    error_message: str | None,
) -> str:
    generated = iso_utc(datetime.now(timezone.utc))
    lines = [
        "# ES Performance Report",
        "",
        f"- Generated: {generated}",
        f"- Base URL: {base_url}",
        f"- Index: {index}",
        f"- Date range: {start_date} .. {end_date}",
        f"- Range: {range_value}",
        f"- Root size: {root_size}",
        f"- Sub multiplier: {sub_multiplier}",
        f"- Sub size: {sub_size}",
        f"- Iterations: {iterations}",
        f"- Target IPS: {target_ips}",
        (
            f"- Achieved IPS: {achieved_ips:.2f}"
            if achieved_ips is not None
            else "- Achieved IPS:"
        ),
        f"- Max concurrency: {max_concurrency}",
        f"- Request cache: {request_cache}",
        f"- Routing: {'enabled' if routing_enabled else 'disabled'}",
        "",
    ]

    lines.extend(["## Results Summary", ""])
    if error_message:
        lines.extend([f"Error: {error_message}", ""])

    if all_results:
        lines.append(build_report_table(all_results))
    else:
        lines.extend(["No results collected.", ""])

    if sample_root_query or sample_sub_query:
        lines.extend(
            [
                "## Sample Queries",
                "",
                "Account UUID and transaction IDs are redacted.",
                f"Routing: {'routing=<REDACTED_ACCOUNT>' if routing_enabled else 'disabled'}",
                "",
            ]
        )
        if sample_root_query:
            lines.extend(
                [
                    "### Root Query",
                    "",
                    "```json",
                    json.dumps(sample_root_query, indent=2),
                    "```",
                    "",
                ]
            )
        if sample_sub_query:
            lines.extend(
                [
                    "### Sub Query",
                    "",
                    "```json",
                    json.dumps(sample_sub_query, indent=2),
                    "```",
                    "",
                ]
            )

    return "\n".join(lines).rstrip() + "\n"


async def run_iteration(
    client: httpx.AsyncClient,
    account_uuid: str,
    url: str,
    start_date: str,
    end_date: str,
    root_size: int,
    sub_size: int,
    timeout: float,
    routing_enabled: bool,
) -> tuple[IterationResult, list[str]]:
    total_start = time.perf_counter()

    root_query = build_root_query(account_uuid, start_date, end_date, root_size)
    root_url = url
    if routing_enabled:
        root_url = f"{url}&routing={account_uuid}"
    (
        root_payload,
        root_ttfb_ms,
        root_read_ms,
        root_decode_ms,
        root_wall_ms,
    ) = await fetch_json(client, root_url, root_query, timeout)
    root_ids = extract_root_brand_ids(root_payload)

    sub_query = build_sub_query(account_uuid, start_date, end_date, root_ids, sub_size)
    sub_url = url
    if routing_enabled:
        sub_url = f"{url}&routing={account_uuid}"
    (
        sub_payload,
        sub_ttfb_ms,
        sub_read_ms,
        sub_decode_ms,
        sub_wall_ms,
    ) = await fetch_json(client, sub_url, sub_query, timeout)
    total_wall_ms = (time.perf_counter() - total_start) * 1000.0

    result = IterationResult(
        account_uuid=account_uuid,
        iteration=0,
        root_wall_ms=root_wall_ms,
        root_es_took_ms=root_payload.get("took"),
        root_ttfb_ms=root_ttfb_ms,
        root_read_ms=root_read_ms,
        root_decode_ms=root_decode_ms,
        root_hits=hit_count(root_payload),
        root_brand_ids=len(root_ids),
        sub_wall_ms=sub_wall_ms,
        sub_es_took_ms=sub_payload.get("took"),
        sub_ttfb_ms=sub_ttfb_ms,
        sub_read_ms=sub_read_ms,
        sub_decode_ms=sub_decode_ms,
        sub_hits=hit_count(sub_payload),
        total_wall_ms=total_wall_ms,
    )

    return result, root_ids


async def main() -> int:
    args = parse_args()
    accounts = load_accounts(args)

    range_value = args.range.strip().lower()
    if not range_value.endswith("m") or not range_value[:-1].isdigit():
        raise SystemExit("Range must be in months, e.g. 1m, 3m, 18m")
    range_months = int(range_value[:-1])
    if range_months <= 0:
        raise SystemExit("Range must be a positive month value, e.g. 1m")

    now = datetime.now(timezone.utc)
    start_date = iso_utc(now - timedelta(days=30 * range_months))
    end_date = iso_utc(now)
    sub_size = max(1, int(args.root_size * args.sub_multiplier))

    base_url = args.base_url.rstrip("/")
    url = f"{base_url}/{args.index}/_search?request_cache={args.request_cache}"

    if args.pretty_root_query:
        query = build_root_query(accounts[0], start_date, end_date, args.root_size)
        print(json.dumps(query, indent=2))
        return 0

    if args.pretty_sub_query:
        example_root_ids = [
            "S-9693-765030-4382",
            "Chg:GINV:12407947:20260301T00:09:26UTC:20260323T00:09:26UTC",
            "Chg:GINV:12407948:20260301T00:09:26UTC:20260323T00:09:26UTC",
        ]
        query = build_sub_query(
            accounts[0], start_date, end_date, example_root_ids, sub_size
        )
        print(json.dumps(query, indent=2))
        return 0

    def log(message: str) -> None:
        if args.verbose:
            print(message)

    log("Benchmark configuration")
    log(f"  URL:                     {url}")
    log(f"  Accounts:                {len(accounts)}")
    log(f"  Date range:              {start_date} .. {end_date}")
    log(f"  Range:                   {range_value}")
    log(f"  Root size:               {args.root_size}")
    log(f"  Sub multiplier:          {args.sub_multiplier}")
    log(f"  Sub size:                {sub_size}")
    log(f"  Iterations:              {args.iterations}")
    target_ips = args.target_ips if args.target_ips > 0 else 0.0
    log(f"  Target IPS:              {target_ips}")
    log(f"  Max concurrency:         {args.max_concurrency}")
    log(f"  Max connections:         {args.max_connections}")
    log(f"  Max keepalive conns:     {args.max_keepalive_connections}")
    log(f"  Routing:                 {'enabled' if args.routing else 'disabled'}")

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        raise SystemExit(
            f"Missing API key. Set env var {args.api_key_env} or pass --api-key-env."
        )
    api_key_value = api_key.strip()
    if api_key_value.lower().startswith("apikey "):
        auth_value = api_key_value
    else:
        auth_value = f"ApiKey {api_key_value}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_value,
    }

    if args.debug_auth:
        scheme = auth_value.split(" ", 1)[0] if auth_value else "<none>"
        token = auth_value.split(" ", 1)[1] if " " in auth_value else ""
        print(
            "Auth header set"
            f" | scheme={scheme}"
            f" | token_length={len(token)}"
            f" | env={args.api_key_env}"
        )

    limits = httpx.Limits(
        max_connections=args.max_connections,
        max_keepalive_connections=args.max_keepalive_connections,
    )

    all_results: list[IterationResult] = []
    error_message: str | None = None
    sample_root_query: dict[str, Any] | None = None
    sample_sub_query: dict[str, Any] | None = None
    sample_lock = asyncio.Lock()
    results_lock = asyncio.Lock()
    error_event = asyncio.Event()
    start_time = time.perf_counter()
    max_sample_ids = 10

    account_index = 0
    accounts_list = list(accounts)
    remaining_by_account = {account: args.iterations for account in accounts}

    async def record_sample(root_ids: list[str]) -> None:
        nonlocal sample_root_query, sample_sub_query
        async with sample_lock:
            if sample_root_query or sample_sub_query:
                return
            redacted_account = "<REDACTED_ACCOUNT>"
            redacted_ids = [
                f"<REDACTED_TXN_{i + 1}>"
                for i in range(min(len(root_ids), max_sample_ids))
            ]
            if len(root_ids) > max_sample_ids:
                redacted_ids.append("<REDACTED_TXN_MORE>")
            sample_root_query = build_root_query(
                redacted_account, start_date, end_date, args.root_size
            )
            sample_sub_query = build_sub_query(
                redacted_account,
                start_date,
                end_date,
                redacted_ids,
                sub_size,
            )

    async def run_one(account_uuid: str) -> None:
        nonlocal error_message
        if error_event.is_set():
            return
        try:
            result, root_ids = await run_iteration(
                client,
                account_uuid,
                url,
                start_date,
                end_date,
                args.root_size,
                sub_size,
                args.timeout,
                args.routing,
            )
            await record_sample(root_ids)
            async with results_lock:
                all_results.append(result)
            log(
                f"{account_uuid} | "
                f"root wall={result.root_wall_ms:8.2f} ms | "
                f"root took={str(result.root_es_took_ms):>4} ms | "
                f"root hits={result.root_hits:>4} | "
                f"root ids={result.root_brand_ids:>3} | "
                f"sub wall={result.sub_wall_ms:8.2f} ms | "
                f"sub took={str(result.sub_es_took_ms):>4} ms | "
                f"sub hits={result.sub_hits:>4} | "
                f"total={result.total_wall_ms:8.2f} ms"
            )
        except HttpError as exc:
            error_message = (
                "Query failed for account " f"{account_uuid}: HTTP {exc.status_code}"
            )
            if str(exc):
                error_message = f"{error_message} | {exc}"
            error_event.set()
        except httpx.RequestError as exc:
            error_message = f"Request error for account {account_uuid}: {exc}"
            error_event.set()

    def next_account() -> str | None:
        nonlocal account_index
        if not remaining_by_account:
            return None
        for _ in range(len(accounts_list)):
            account = accounts_list[account_index % len(accounts_list)]
            account_index += 1
            remaining = remaining_by_account.get(account, 0)
            if remaining > 0:
                remaining_by_account[account] = remaining - 1
                if remaining_by_account[account] == 0:
                    remaining_by_account.pop(account, None)
                return account
        return None

    total_iterations = args.iterations * len(accounts)
    max_concurrency = max(1, args.max_concurrency)
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks: set[asyncio.Task[None]] = set()

    async with httpx.AsyncClient(
        headers=headers,
        timeout=args.timeout,
        verify=False,
        limits=limits,
    ) as client:
        next_fire = time.perf_counter()
        for _ in range(total_iterations):
            if error_event.is_set():
                break
            account_uuid = next_account()
            if not account_uuid:
                break
            if target_ips > 0:
                now = time.perf_counter()
                sleep_for = next_fire - now
                if sleep_for > 0:
                    await asyncio.sleep(sleep_for)
            await semaphore.acquire()
            task = asyncio.create_task(run_one(account_uuid))
            tasks.add(task)

            def _done_callback(done_task: asyncio.Task[None]) -> None:
                tasks.discard(done_task)
                semaphore.release()

            task.add_done_callback(_done_callback)
            if target_ips > 0:
                next_fire += 1.0 / target_ips

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    end_time = time.perf_counter()
    elapsed = max(end_time - start_time, 0.000001)
    achieved_ips = len(all_results) / elapsed if all_results else 0.0

    if args.report_md is not None:
        report_path = Path(args.report_md)
    else:
        report_filename = f"es_performance_report_{range_value}_root{args.root_size}.md"
        report_path = Path("es_reports") / report_filename
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_content = build_report(
            base_url,
            args.index,
            start_date,
            end_date,
            args.root_size,
            args.sub_multiplier,
            sub_size,
            args.iterations,
            args.request_cache,
            range_value,
            args.routing,
            target_ips,
            achieved_ips,
            max_concurrency,
            all_results,
            sample_root_query,
            sample_sub_query,
            error_message,
        )
        report_path.write_text(report_content, encoding="utf-8")
        print(f"Report written: {report_path}")

    return 1 if error_message else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
