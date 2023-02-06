#!/usr/bin/env python3

import argparse

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

for node in range(1, args.node_count+1):
    startup_nodes.append(Node(args.host+str(node).zfill(3), args.port))

client = Redis(startup_nodes=startup_nodes, password=args.password)

all_keys = client.keys()

for key in all_keys:
    key = key.decode("utf-8")
    namespace = key.split(":")[0]  
    if namespace not in key_namespaces.keys():
        key_namespaces[namespace] = 0 
    
    bytes_used = client.memory_usage(key) 
    total_memory_used += bytes_used
    key_namespaces[namespace] = 0


for namespace in key_namespaces.keys():
    print(f"{namespace} : {key_namespaces[namespace]} bytes used")

print()
print(f"total bytes used: {total_memory_used}")



