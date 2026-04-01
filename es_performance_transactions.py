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
    --request-cache false

Or from a file:
  ES_API_KEY=YOUR_API_KEY uv run python bench_es_two_step.py \
    --base-url http://localhost:9200 \
    --accounts-file accounts.txt
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class IterationResult:
    account_uuid: str
    iteration: int
    root_wall_ms: float
    root_es_took_ms: int | None
    root_hits: int
    root_brand_ids: int
    sub_wall_ms: float
    sub_es_took_ms: int | None
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
                    {"terms": {"transaction_type": ["network_tax", "non_network_tax"]}},
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
        default=1,
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


def run_query(
    session: requests.Session,
    url: str,
    query: dict[str, Any],
    timeout: float,
) -> tuple[float, requests.Response]:
    start = time.perf_counter()
    response = session.post(url, json=query, timeout=timeout, verify=False)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return elapsed_ms, response


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
    root_counts = [r.root_hits for r in results]
    sub_counts = [r.sub_hits for r in results]
    brand_counts = [r.root_brand_ids for r in results]

    def mean_or_blank(values: list[float | int]) -> str:
        return f"{statistics.mean(values):.2f}" if values else ""

    def min_max(values: list[float]) -> str:
        return f"{min(values):.2f} / {max(values):.2f}" if values else ""

    def unique_list(values: list[int]) -> str:
        return ", ".join(str(v) for v in sorted(set(values))) if values else ""

    rows = [
        ("Runs", str(len(results))),
        ("Root avg wall (ms)", mean_or_blank(root_wall)),
        ("Root min/max wall (ms)", min_max(root_wall)),
        ("Sub avg wall (ms)", mean_or_blank(sub_wall)),
        ("Sub min/max wall (ms)", min_max(sub_wall)),
        ("Total avg wall (ms)", mean_or_blank(total_wall)),
        ("Total min/max (ms)", min_max(total_wall)),
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


def main() -> int:
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
            accounts[0], start_date, end_date, example_root_ids, args.sub_size
        )
        print(json.dumps(query, indent=2))
        return 0

    def log(message: str) -> None:
        if args.verbose:
            print(message)

    log("Benchmark configuration")
    log(f"  URL:             {url}")
    log(f"  Accounts:        {len(accounts)}")
    log(f"  Date range:      {start_date} .. {end_date}")
    log(f"  Range:           {range_value}")
    log(f"  Root size:       {args.root_size}")
    log(f"  Sub multiplier: {args.sub_multiplier}")
    log(f"  Sub size:       {sub_size}")
    log(f"  Iterations:      {args.iterations}")
    log(f"  Routing:         {'enabled' if args.routing else 'disabled'}")

    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})

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
    session.headers.update({"Authorization": auth_value})

    if args.debug_auth:
        scheme = auth_value.split(" ", 1)[0] if auth_value else "<none>"
        token = auth_value.split(" ", 1)[1] if " " in auth_value else ""
        print(
            "Auth header set"
            f" | scheme={scheme}"
            f" | token_length={len(token)}"
            f" | env={args.api_key_env}"
        )

    all_results: list[IterationResult] = []
    sample_root_query: dict[str, Any] | None = None
    sample_sub_query: dict[str, Any] | None = None
    sample_account_uuid = accounts[0] if accounts else None
    max_sample_ids = 10
    error_message: str | None = None

    for account_uuid in accounts:
        account_results: list[IterationResult] = []

        for iteration in range(1, args.iterations + 1):
            total_start = time.perf_counter()

            root_query = build_root_query(
                account_uuid, start_date, end_date, args.root_size
            )
            root_url = url
            if args.routing:
                root_url = f"{url}&routing={account_uuid}"
            root_wall_ms, root_response = run_query(
                session, root_url, root_query, args.timeout
            )

            if root_response.status_code >= 400:
                snippet = root_response.text[:400].replace("\n", " ")
                error_message = (
                    "Root query failed for account "
                    f"{account_uuid}: HTTP {root_response.status_code}"
                )
                if snippet:
                    error_message = f"{error_message} | {snippet}"
                break

            root_payload = root_response.json()
            root_ids = extract_root_brand_ids(root_payload)

            if (
                sample_account_uuid
                and account_uuid == sample_account_uuid
                and iteration == 1
            ):
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

            sub_query = build_sub_query(
                account_uuid, start_date, end_date, root_ids, sub_size
            )
            sub_url = url
            if args.routing:
                sub_url = f"{url}&routing={account_uuid}"
            sub_wall_ms, sub_response = run_query(
                session, sub_url, sub_query, args.timeout
            )

            if sub_response.status_code >= 400:
                snippet = sub_response.text[:400].replace("\n", " ")
                error_message = (
                    "Sub query failed for account "
                    f"{account_uuid}: HTTP {sub_response.status_code}"
                )
                if snippet:
                    error_message = f"{error_message} | {snippet}"
                break

            sub_payload = sub_response.json()
            total_wall_ms = (time.perf_counter() - total_start) * 1000.0

            result = IterationResult(
                account_uuid=account_uuid,
                iteration=iteration,
                root_wall_ms=root_wall_ms,
                root_es_took_ms=root_payload.get("took"),
                root_hits=hit_count(root_payload),
                root_brand_ids=len(root_ids),
                sub_wall_ms=sub_wall_ms,
                sub_es_took_ms=sub_payload.get("took"),
                sub_hits=hit_count(sub_payload),
                total_wall_ms=total_wall_ms,
            )

            account_results.append(result)
            all_results.append(result)

            log(
                f"{account_uuid} | run {iteration:02d} | "
                f"root wall={root_wall_ms:8.2f} ms | "
                f"root took={str(result.root_es_took_ms):>4} ms | "
                f"root hits={result.root_hits:>4} | "
                f"root ids={result.root_brand_ids:>3} | "
                f"sub wall={sub_wall_ms:8.2f} ms | "
                f"sub took={str(result.sub_es_took_ms):>4} ms | "
                f"sub hits={result.sub_hits:>4} | "
                f"total={total_wall_ms:8.2f} ms"
            )

        if error_message:
            break

    if args.report_md is not None:
        report_path = Path(args.report_md)
    else:
        report_filename = f"es_performance_report_{range_value}_root{args.root_size}.md"
        report_path = Path("reports") / report_filename
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
            all_results,
            sample_root_query,
            sample_sub_query,
            error_message,
        )
        report_path.write_text(report_content, encoding="utf-8")
        print(f"Report written: {report_path}")

    return 1 if error_message else 0


if __name__ == "__main__":
    sys.exit(main())
