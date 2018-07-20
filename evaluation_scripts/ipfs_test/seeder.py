import argparse
import os
import time
import datetime
import json

parser = argparse.ArgumentParser(description='Command Line Interface')
parser.add_argument('--node_index', type=int, nargs='?',
                    help='IPFS Node index')

parser.add_argument('--nodes', type=int, nargs='?',
                    help='Number of Nodes')

parser.add_argument('--file_hash', type=str, nargs='?',
                    help='File IPFS link')

if __name__ == '__main__':
    # Parse arguments
    args = parser.parse_args()
    print("===========Running node {} ==============".format(args.node_index))
    now = datetime.datetime.now()
    start = time.time()
    os.system("ipfs cat {} > /dev/null/".format(args.file_hash))
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



