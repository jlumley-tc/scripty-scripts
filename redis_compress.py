#!/usr/bin/env python3

import argparse 
import gzip
import re

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('password', type=str)
parser.add_argument('--regex', type=str, help='keys to compress')
args = parser.parse_args()

compressed_keys_log = 'compressed_keys_file.log'

def compress_redis_data(client, key):

    data = client.get(key)

def print_summary(data):
    od = OrderedDict(sorted(data.items(), key=lambda d:d[1]))
    for namespace in od.keys():
        if namespace == 'total' or re.search('de-dupe', namespace):
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
    
    keys_file = open(compressed_keys_log, 'r')
    compressed_keys=set(keys_file.readlines())

    for key in client.scan(match=args.regex):
        key = key.decode("utf-8")

        if key in compressed_keys:
            continue
        else:
           compress_redis_data(key) 
           compressed_keys.add(key)
           keys_file.write(key)
        

    print(f"compressed {len(compressed_keys)} keys")


if __name__ == "__main__":
    main()
