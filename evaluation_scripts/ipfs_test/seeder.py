import argparse
import os
import time
import datetime
import json

parser = argparse.ArgumentParser(description='Command Line Interface')
parser.add_argument('--node_index', type=int, nargs='?',
                    help='IPFS Node index')

parser.add_argument('--api_port', type=int, nargs='?',
                    help='IPFS API port')

parser.add_argument('--nodes', type=int, nargs='?',
                    help='Number of Nodes')

parser.add_argument('--file_hash', type=str, nargs='?',
                    help='File IPFS link')

if __name__ == '__main__':
    # Parse arguments
    args = parser.parse_args()
    # Point to the correct ipfs daemon
    os.environ['IPFS_PATH'] = '~/.ipfs_' +  str(args.node_index)
    print("===========Running node {} ==============".format(args.node_index))
    # Set up a temp dir to store the file and the results. This avoids collisions
    now = datetime.datetime.now()
    directory =  "evaluation_scripts/ipfs_test/temp_{}_{}".format(args.node_index,now.strftime("%Y-%m-%d_%H%M%S"))
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Import IPFS, download the file, and make store it in the temp dir
    import ipfsapi
    try:
        api = ipfsapi.connect('127.0.0.1', args.api_port)
    except:
         time.sleep(5)
         api = ipfsapi.connect('127.0.0.1', args.api_port)

    print("Connected to IPFS Deamon with port {}".format(args.api_port))
    print("Retrieving file {} started at time {}".format(args.file_hash, now.strftime("%Y-%m-%d_%H%M%S")))
    start = time.time()
    try:
        api.get(args.file_hash, filepath = directory)
    except:
        time.sleep(5)
        start = time.time()
        api.get(args.file_hash, filepath = directory)
        
    end = time.time()
    # Print and save results
    print("Node {} downladed the file in {}".format(args.node_index,end-start))
    result_json = { 'Date-time': now.strftime("%Y-%m-%d %H%M"),
                    'Users': args.nodes,
                    'Used Id': str(args.node_index),
                    'Time': str(end-start)}

    with open("evaluation_scripts/ipfs_test/ipfs_nodes_{}_result.txt".format(args.node_index), 'a+') as dataf:
        json.dump(result_json, dataf)
        dataf.write('\n')
 
    print("Run Completed!")



