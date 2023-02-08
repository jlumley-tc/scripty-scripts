#!/usr/bin/env python3

import argparse 
import gzip
import math
import sys

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('password', type=str)
parser.add_argument('--regex', type=str, help='keys to compress')
parser.add_argument('--ttl', type=int, help='add ttl to the new keys (in ms)')
args = parser.parse_args()

compressed_keys_log = 'compressed_keys_file.log'


def is_compressed(data):
    return data[:2] == b'\x1f\x8b'

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def compress_redis_data(client, key):

    data = client.get(key)
    if (is_compressed(data)):
        print(f'{key} is already compressed')
        return
    
    compressed_string = gzip.compress(data)

    client.set(key, compressed_string, px=args.ttl)

    # print('original data: ', convert_size(sys.getsizeof(data)))
    # print('compressed data: ', convert_size(sys.getsizeof(compressed_string)))
    # print('compression ratio: ', round(sys.getsizeof(compressed_string)/sys.getsizeof(data),2))

def main():

    startup_nodes = [Node(args.host, 6379)]
    client = Redis(startup_nodes=startup_nodes, password=args.password)
    
    keys_file = open(compressed_keys_log, 'r+')
    compressed_keys=set(keys_file.readlines())

    for key in client.scan_iter(match=args.regex):
        key = key.decode("utf-8")

        if "de-dupe" in key:
            print("ignoring deduplication key")
            continue

        if key in compressed_keys:
            continue
        else:
           compress_redis_data(client, key) 
           compressed_keys.add(key)
           keys_file.write(key+"\n")
    

    print(f"compressed {len(compressed_keys)} keys")


if __name__ == "__main__":
    main()
