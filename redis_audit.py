#!/usr/bin/env python3

import argparse 
import re

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('password', type=str)
parser.add_argument('--percentage','-p', type=float, default=100)
args = parser.parse_args()

startup_nodes = [Node(args.host, 6379)]

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def separate_namespaces(all_keys):
    namespace_regex = re.compile(".*:")
    sorted_keys = dict()

    for key in all_keys:
        namespace = namespace_regex.search(key).group(0)
        if namespace not in sorted_keys.keys():
            sorted_keys[namespace] = [key]
        else:
            sorted_keys[namespace].append(key)

    return list(sorted_keys.values())

def audit_redis(keys):

    namespace_regex = re.compile(".*:")
    namespace = namespace_regex.search(key).group(0)

    client = Redis(startup_nodes=startup_nodes, password=args.password)

    num_keys = len(keys)
    for i in range(num_keys):
        if (i%1000 == 0):
            print(f"working on key {i} of {num_keys}")
        key = keys[i].decode("utf-8")
        if namespace not in key_namespaces.keys():
            key_namespaces[namespace] = 0 
        
        bytes_used = client.memory_usage(key) 
        key_namespaces['total'] += bytes_used
        key_namespaces[namespace] += bytes_used


    for namespace in key_namespaces.keys():
        size = sizeof_fmt(key_namespaces[namespace])
        print(f"{namespace} | {size} | {round(100*key_namespaces[namespace]/key_namespaces['total'],2)}%")

    return key_namespaces


def main():

    client = Redis(startup_nodes=startup_nodes, password=args.password)
    
    db_size = client.dbsize()
    sample_size = int(db_size*args.percentage)
    keys = list()
    for i in range(sample_size):
        keys.append(str(client.randomkey()))

    print(keys)
    print(sample_size)

if __name__ == "__main__":
    main()
