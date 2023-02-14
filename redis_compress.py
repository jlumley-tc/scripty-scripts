#!/usr/bin/env python3

import argparse 
import gzip
import json
import math
import os
import random
import re
import sys
import time

from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode as Node


parser = argparse.ArgumentParser(description="Audit memory usage of Redis Cluster")
parser.add_argument('host', type=str)
parser.add_argument('password', type=str)
parser.add_argument('--verbose', '-v', action='store_true')
args = parser.parse_args()

if not os.path.exists('compressed_keys_file.log'):
    compressed_keys_log = open('compressed_keys_file.log', 'w+')
else:
    compressed_keys_log = open('compressed_keys_file.log', 'r+')

error_log = open('errors.log', 'a')
de_dupe_regex = re.compile("de-dupe")


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

def generate_ttl_data():

    with open('ttl_data.json', 'r') as json_file:
        ttl_data = json.loads(json_file.read())

    for d in ttl_data:
        d['compiled_regex'] = re.compile(d['regex'])

    return ttl_data

def get_ttl(key, ttl_data):
    max_ttl = 0

    for namespace in ttl_data:
        if namespace['compiled_regex'].match(key):
            max_ttl = max(max_ttl, namespace['ttl_ms'])

    if max_ttl == 0:
        max_ttl = 1000 * 60 * 60 * 24 * 365
        error_log.write(f"Could not match {key} to ttl setting ttl to one year\n")

    return max_ttl


def verify_compressed(client, key):
    
    data = client.get(key)
    if not is_compressed(data):
        raise Exception(f"Found uncompressed key {key}")
    

def compress_redis_data(client, key, ttl_data):

    data = client.get(key)
    ttl = get_ttl(key, ttl_data)

    compressed_string = gzip.compress(data)

    if args.verbose:
        if random.randint(1,10000) == 1234:
            print(f"{key}")
            print('original data: ', convert_size(sys.getsizeof(data)))
            print('compressed data: ', convert_size(sys.getsizeof(compressed_string)))
            print('compression ratio: ', round(sys.getsizeof(compressed_string)/sys.getsizeof(data),2))

    if not is_compressed(data):
        client.set(key, compressed_string, px=ttl)


def main():

    startup_nodes = [Node(args.host, 6379)]
    client = Redis(startup_nodes=startup_nodes, password=args.password)
    
    compressed_keys=set([key.strip() for key in compressed_keys_log.readlines()])
    ttl_data = generate_ttl_data()

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

        # skip keys that have already been compressed
        if key in compressed_keys:
            continue
        
        compress_redis_data(client, key, ttl_data)
        compressed_keys_log.write(key+"\n")


if __name__ == "__main__":
    main()
