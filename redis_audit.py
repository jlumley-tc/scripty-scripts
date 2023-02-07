#!/usr/bin/env python3

import argparse 
import re

from multiprocessing import Process
from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('node_count', type=int)
parser.add_argument('port', type=str)
parser.add_argument('password', type=str)
args = parser.parse_args()

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def audit_redis(keys):

    startup_nodes = list()
    key_namespaces = dict(total=0)
    namespace_regex = re.compile(".*:")

    for node in range(1, args.node_count+1):
        startup_nodes.append(Node(args.host+str(node).zfill(3), args.port))

    client = Redis(startup_nodes=startup_nodes, password=args.password)

    num_keys = len(keys)
    for i in range(num_keys):
        if (i%1000 == 0):
            print(f"working on key {i} of {num_keys}")
        key = keys[i].decode("utf-8")
        namespace = namespace_regex.search(key).group(0)
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

    startup_nodes = list()
    pids = list()

    for node in range(1, args.node_count+1):
        startup_nodes.append(Node(args.host+str(node).zfill(3), args.port))

    client = Redis(startup_nodes=startup_nodes, password=args.password)
    all_keys = client.keys()

    list_of_keys = divide_chunks(all_keys, 10)
    for key_set in list_of_keys:
        p = Process(target=audit_redis, args=(list_of_keys,))
        p.start()
        pids.append(p)

    for p in pids:
        p.join()

if __name__ == "__main__":
    main()
