#!/usr/bin/env python3
import argparse
from collections import defaultdict

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


def two_part_namespace(key: str) -> str:
    parts = key.split(":", 2)
    return ":".join(parts[:2]) + ":" if len(parts) >= 2 else "(no-namespace)"


def ttl_bucket(ttl_seconds: int) -> str:
    # Redis TTL: -2 missing, -1 no-expire, >=0 seconds
    if ttl_seconds == -2:
        return "missing(-2)"
    if ttl_seconds == -1:
        return "no-ttl(-1)"
    if ttl_seconds < 1 * 86400:
        return "<1d"
    if ttl_seconds < 7 * 86400:
        return "<7d"
    if ttl_seconds < 30 * 86400:
        return "<30d"
    if ttl_seconds < 90 * 86400:
        return "<90d"
    return ">=90d"


def decode_key(x):
    if isinstance(x, (bytes, bytearray)):
        return x.decode("utf-8", errors="replace")
    return str(x)


def get_masters(client):
    masters = [
        n for n in client.get_nodes() if getattr(n, "server_type", None) == "master"
    ]
    if masters:
        return masters
    # fallback for older redis-py-cluster
    try:
        return client.get_primaries()
    except Exception:
        return [Redis.ALL_NODES]  # last resort


def main():
    p = argparse.ArgumentParser(
        description="Investigate Redis Cluster keyspace: counts + TTL health + expiry signals"
    )
    p.add_argument("host", type=str, help="Redis cluster hostname or IP address")
    p.add_argument("password", type=str, help="Password for Redis authentication")
    p.add_argument(
        "--port", type=int, default=6379, help="Redis server port (default: 6379)"
    )
    p.add_argument(
        "--match", type=str, default="*", help="Pattern to match keys (default: '*')"
    )
    p.add_argument(
        "--count",
        type=int,
        default=1000,
        help="Number of keys to scan per iteration (default: 1000)",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=1000000,
        help="Stop after visiting N keys total (0 = no limit)",
    )
    p.add_argument(
        "--top-ns",
        type=int,
        default=30,
        help="Number of top key namespaces to display (default: 30)",
    )
    args = p.parse_args()

    client = Redis(startup_nodes=[Node(args.host, args.port)], password=args.password)

    masters = get_masters(client)

    ns_counts = defaultdict(int)
    ttl_counts = defaultdict(int)

    total = 0
    missing = 0
    ttl_errors = 0

    info_before = []
    for node in masters:
        try:
            info_before.append(client.info(section="stats", target_nodes=node))
        except Exception:
            pass

    for node in masters:
        cursor = 0
        while True:
            cursor, keys = client.scan(
                cursor=cursor, match=args.match, count=args.count, target_nodes=node
            )

            for k in keys:
                key = decode_key(k)
                ns = two_part_namespace(key)
                ns_counts[ns] += 1
                total += 1

                # TTL
                try:
                    ttl = client.ttl(key)
                    b = ttl_bucket(ttl)
                    ttl_counts[b] += 1
                    if ttl == -2:
                        missing += 1
                except Exception:
                    ttl_errors += 1
                    ttl_counts["(ttl-error)"] += 1

                if args.limit and total >= args.limit:
                    break

            if args.limit and total >= args.limit:
                break
            if cursor == 0:
                break

    # --- Snapshot INFO stats after scan ---
    info_after = []
    for node in masters:
        try:
            info_after.append(client.info(section="stats", target_nodes=node))
        except Exception:
            pass

    def sum_stat(infos, field):
        s = 0
        for blob in infos:
            # redis-py cluster can return dict keyed by node name -> dict
            if isinstance(blob, dict) and any(
                isinstance(v, dict) for v in blob.values()
            ):
                for v in blob.values():
                    if isinstance(v, dict) and field in v:
                        s += int(v[field])
            elif isinstance(blob, dict) and field in blob:
                s += int(blob[field])
        return s

    expired_before = sum_stat(info_before, "expired_keys")
    expired_after = sum_stat(info_after, "expired_keys")
    evicted_before = sum_stat(info_before, "evicted_keys")
    evicted_after = sum_stat(info_after, "evicted_keys")
    keyspace_hits_b = sum_stat(info_before, "keyspace_hits")
    keyspace_hits_a = sum_stat(info_after, "keyspace_hits")
    keyspace_miss_b = sum_stat(info_before, "keyspace_misses")
    keyspace_miss_a = sum_stat(info_after, "keyspace_misses")

    print(f"\nVisited keys: {total}")
    if args.match != "*":
        print(f"Match: {args.match}")
    if args.limit:
        print(f"(Stopped early at --limit {args.limit})")

    print("\nTTL buckets:")
    for b, c in sorted(ttl_counts.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{b:>10}: {c}")

    print(f"Keys missing during scan (ttl=-2): {missing}")

    print("\nTop namespaces by COUNT:")
    for ns, c in sorted(ns_counts.items(), key=lambda kv: kv[1], reverse=True)[
        : args.top_ns
    ]:
        print(f"{ns} {c}")

    print("\nExpiry/eviction signals (INFO stats delta during scan):")
    print(
        f"expired_keys:  {expired_before} -> {expired_after}  (Δ {expired_after-expired_before})"
    )
    print(
        f"evicted_keys:  {evicted_before} -> {evicted_after}  (Δ {evicted_after-evicted_before})"
    )
    print(
        f"hits:          {keyspace_hits_b} -> {keyspace_hits_a} (Δ {keyspace_hits_a-keyspace_hits_b})"
    )
    print(
        f"misses:        {keyspace_miss_b} -> {keyspace_miss_a} (Δ {keyspace_miss_a-keyspace_miss_b})"
    )


if __name__ == "__main__":
    main()
