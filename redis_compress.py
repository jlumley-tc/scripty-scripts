#!/usr/bin/env python3

import argparse 
import gzip
import math
import re
import sys
import time

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('password', type=str)
parser.add_argument('--regex', type=str, help='keys to compress')
parser.add_argument('--ttl', type=int, help='add ttl to the new keys (in ms)')
args = parser.parse_args()

compressed_keys_log = 'compressed_keys_file.log'
de_dupe_regex = re.compile("de-dupe")
filter_regex = re.compile(f"^{args.regex}")


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


def verify_compressed(client, key):
    
    data = client.get(key)
    if not is_compressed(data):
        raise Exception(f"Found uncompressed key {key}")
    

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
    compressed_keys=set([key.strip() for key in keys_file.readlines()])
    start_time = time.time()
    num_keys = 0
    for key in client.scan_iter():
        key = key.decode("utf-8")
        num_keys +=1
        # print out keys/min stats
        if num_keys % 10000 == 0:
            stat = num_keys*60/(time.time()-start_time)
            print(f"Compressing {round(stat,2)} keys/min", end="\r")

        # skip deduplication keys
        if de_dupe_regex.search(key):
            continue

        # skip keys that don't match the regex
        if not filter_regex.search(key):
            continue

        # skip keys that have already been compressed
        if key in compressed_keys:
            continue
        
        compress_redis_data(client, key) 
        keys_file.write(key+"\n")

            


if __name__ == "__main__":
    main()
