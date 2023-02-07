#!/usr/bin/env python3

import argparse 
import re

from collections import OrderedDict
from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('password', type=str)
parser.add_argument('--percentage','-p', type=float, default=100)
args = parser.parse_args()

sample = args.percentage/100

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def audit_redis(client, keys):

    namespace_regex = re.compile(".*:")
    key_namespaces = dict(total=0)

    for key in keys:
        namespace = namespace_regex.search(key).group(0)
        if namespace not in key_namespaces.keys():
            key_namespaces[namespace] = 0 
        
        bytes_used = client.memory_usage(key) 
        key_namespaces['total'] += bytes_used
        key_namespaces[namespace] += bytes_used


    return key_namespaces


def print_summary(data):
    od = OrderedDict(sorted(data.items(), key=lambda d:d[1]))
    for namespace in od.keys():
        if namespace == 'total':
            continue 
        namespace_size = data[namespace]*(1/sample)
        total_size = data['total']*(1/sample)
        size_str = sizeof_fmt(namespace_size)
        percentage_str = round(100*namespace_size/total_size,2)

        print(f"{namespace} | {size_str} | {percentage_str}%")
    
    print()
    print(f"Total: {sizeof_fmt(data['total']*(1/sample))}")


def main():

    startup_nodes = [Node(args.host, 6379)]
    client = Redis(startup_nodes=startup_nodes, password=args.password)
    
    db_size = client.dbsize(target_nodes=Redis.ALL_NODES)
    sample_size = max(int(db_size*sample),1)
    keys = list()

    for i in range(sample_size):
        keys.append(client.randomkey().decode("utf-8"))

    namespace_data = audit_redis(client, keys)


    print(f"sampled {sample_size} keys of {db_size}")

    print_summary(namespace_data)

if __name__ == "__main__":
    main()
