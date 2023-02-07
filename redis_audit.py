#!/usr/bin/env python3

import argparse
import re

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('node_count', type=int)
parser.add_argument('port', type=str)
parser.add_argument('password', type=str)
args = parser.parse_args()

startup_nodes = list()
key_namespaces = dict()
total_memory_used = 0


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

for node in range(1, args.node_count+1):
    startup_nodes.append(Node(args.host+str(node).zfill(3), args.port))

client = Redis(startup_nodes=startup_nodes, password=args.password)

all_keys = client.keys()
num_keys = len(all_keys)
for i in range(num_keys):
    if (i%1000 == 10):
        break
        print(f"working on key {i} of {num_keys}")
    key = all_keys[i].decode("utf-8")
    print(re.search('.*:', key).match(0))
    namespace = key.split(":")[0] 
    if namespace not in key_namespaces.keys():
        key_namespaces[namespace] = 0 
    
    bytes_used = client.memory_usage(key) 
    total_memory_used += bytes_used
    key_namespaces[namespace] += bytes_used


for namespace in key_namespaces.keys():
    size = sizeof_fmt(key_namespaces[namespace])
    print(f"{namespace} | {size} | {key_namespaces[namespace]/total_memory_used}%")

print()
print(f"total bytes used: {sizeof_fmt(total_memory_used)}")



