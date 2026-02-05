#!/usr/bin/env python3
import argparse
import re
from collections import OrderedDict, defaultdict

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node

parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument("host", type=str)
parser.add_argument("password", type=str)
parser.add_argument("--percentage", "-p", type=float, default=100)
parser.add_argument("--port", type=int, default=6379)
parser.add_argument(
    "--max-draws-multiplier",
    type=int,
    default=20,
    help="Max randomkey draws = sample_size * multiplier (to avoid infinite loops)",
)
args = parser.parse_args()

sample = args.percentage / 100.0
namespace_regex = re.compile(r"^(?:[^:]*:){2}")


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def key_namespace(key: str) -> str:
    m = namespace_regex.search(key)
    return m.group(0) if m else "(no-namespace)"


def audit_redis(client, keys):
    totals = defaultdict(int)
    totals["total"] = 0
    ns_key_counts = defaultdict(int)
    ns_max_size = defaultdict(int)
    ns_total_size = defaultdict(int)

    for key in keys:
        ns = key_namespace(key)
        ns_key_counts[ns] += 1
        try:
            bytes_used = client.memory_usage(key)
            if bytes_used is None:
                continue
            totals["total"] += bytes_used
            totals[ns] += bytes_used
            ns_total_size[ns] += bytes_used
            if bytes_used > ns_max_size[ns]:
                ns_max_size[ns] = bytes_used
        except Exception:
            # If you want visibility, log the exception + key
            continue

    # Compute average size per namespace (from sampled keys)
    ns_avg_size = {}
    for ns in ns_key_counts:
        count = ns_key_counts[ns]
        ns_avg_size[ns] = ns_total_size[ns] / count if count > 0 else 0

    return dict(totals), dict(ns_key_counts), dict(ns_avg_size), dict(ns_max_size)


def print_summary(data, ns_key_counts, db_size, ns_avg_size, ns_max_size):
    if data.get("total", 0) == 0:
        print("No memory usage data collected (total=0).")
        return

    scaled_total = data["total"] * (1 / sample)
    # sort descending by bytes
    od = OrderedDict(sorted(data.items(), key=lambda kv: kv[1], reverse=True))

    print(
        f"{'Namespace':<30} | {'Size':<12} | {'%':<7} | {'Est. # Keys':<12} | {'Avg Size':<12} | {'Max Size':<12}"
    )
    print("-" * 110)
    for namespace, raw_bytes in od.items():
        if namespace == "total" or re.search("de-dupe", namespace):
            continue

        # Totals should be scaled (we only sampled a fraction of keys)
        namespace_size = raw_bytes * (1 / sample)
        pct = round(100 * namespace_size / scaled_total, 2)

        # Estimated number of keys in this namespace (scale sampled count)
        sampled_keys = ns_key_counts.get(namespace, 0)
        est_keys = int(round(sampled_keys * (1 / sample)))

        # Averages should NOT be scaled; ns_avg_size is already per-key
        avg_size = ns_avg_size.get(namespace, 0)

        # Max is the max observed in the sample (do not scale)
        max_size = ns_max_size.get(namespace, 0)

        print(
            f"{namespace:<80} | {sizeof_fmt(namespace_size):<12} | {pct:<7}% | {est_keys:<12} | {sizeof_fmt(avg_size):<12} | {sizeof_fmt(max_size):<12}"
        )

    print()
    print(f"Total: {sizeof_fmt(scaled_total)}")
    print(f"Estimated total keys: {db_size}")


def main():
    startup_nodes = [Node(args.host, args.port)]
    client = Redis(startup_nodes=startup_nodes, password=args.password)

    db_size = client.dbsize(target_nodes=Redis.ALL_NODES)
    sample_size = max(int(db_size * sample), 1)

    keys = set()
    max_draws = sample_size * args.max_draws_multiplier
    draws = 0

    while len(keys) < sample_size and draws < max_draws:
        k = client.randomkey()
        draws += 1
        if not k:
            continue
        keys.add(k.decode("utf-8"))

    namespace_data, ns_key_counts, ns_avg_size, ns_max_size = audit_redis(
        client, list(keys)
    )

    print(f"sampled {len(keys)} unique keys (drew {draws}) of {db_size}")
    print_summary(namespace_data, ns_key_counts, db_size, ns_avg_size, ns_max_size)


if __name__ == "__main__":
    main()
