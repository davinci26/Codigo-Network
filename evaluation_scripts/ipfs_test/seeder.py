import argparse
import os
import time
parser = argparse.ArgumentParser(description='Command Line Interface')
parser.add_argument('--node_index', type=int, nargs='?',
                    help='IPFS Node index')

parser.add_argument('--api_port', type=int, nargs='?',
                    help='IPFS API port')

parser.add_argument('--file_hash', type=str, nargs='?',
                    help='File IPFS link')

if __name__ == '__main__':
    args = parser.parse_args()
    os.environ['IPFS_PATH'] = '~/.ipfs_' +  str(args.node_index)
    import ipfsapi
    api = ipfsapi.connect('127.0.0.1', api_port)
    start = time.time()
    api.get(args.hash)
    end = time.time()
    now = datetime.datetime.now()
    print("Node {} downladed the file in {}".format(args.node_index,end-now))
    result_json = { 'Date-time': now.strftime("%Y-%m-%d %H%M"),
                    'Used Id': str(args.node_index)
                    'Time': str(end-now)}

    with open("./evaluation_scripts/ipfs_node_{}_result.txt".format(args.node_index), 'a+') as dataf:
        json.dump(result_json, dataf)
        dataf.write('\n')
 
    



