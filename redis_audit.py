#!/usr/bin/env python3

import argparse 
import re

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('node_count', type=int)
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


    for namespace in key_namespaces.keys():
        if namespace == 'total':
            continue 
        namespace_size = key_namespaces[namespace]*(1/sample)
        total_size = key_namespaces['total']*(1/sample)
        size_str = sizeof_fmt(namespace_size)
        percentage_str = round(100*namespace_size/total_size,2)

        print(f"{namespace} | {size_str} | {percentage_str}%")
    
    print()
    print(f"Total: {sizeof_fmt(key_namespaces['total']*(1/sample))}")

    return key_namespaces


def main():

    startup_nodes = list() 
    for i in range(args.node_count):
        startup_nodes.append(Node(args.host+str(i).zfill(3), 6379))

    client = Redis(startup_nodes=startup_nodes, password=args.password)
    
    db_size = client.dbsize()
    sample_size = int(db_size*sample)
    keys = list()
    for i in range(sample_size):
        keys.append(client.randomkey().decode("utf-8"))

    audit_redis(client, keys)

    print(f"sampled {sample_size} keys of {db_size}")

if __name__ == "__main__":
    main()
