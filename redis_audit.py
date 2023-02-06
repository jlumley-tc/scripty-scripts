#!/usr/bin/env python3

import argparse

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('port', type=str)
parser.add_argument('password', type=str)
args = parser.parse_args()

key_namespaces = dict()

startup_nodes = [Node(args.host, args.port)]
client = Redis(
        startup_nodes=startup_nodes
)
# authenticate with the cluster
client.auth(args.password)

all_keys = client.keys()

for key in all_keys:
    namespace = key.split(":")[0]  
    if namespace not in key_namespaces.keys():
        key_namespaces[namespace] = list()
    
    dbg = client.debug_object(key)
    print(dbg)
    raise




