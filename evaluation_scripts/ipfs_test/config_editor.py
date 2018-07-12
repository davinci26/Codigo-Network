import json
import argparse
import os
parser = argparse.ArgumentParser(description='Command Line Interface')
parser.add_argument('--node_index', type=str, nargs='?',
                    help='IPFS Node index')

if __name__ == '__main__':
    args = parser.parse_args()
    ipfs_config_dir = os.path.expanduser('~/.ipfs_' +  str(args.node_index) + "/config")
    with open (ipfs_config_dir, "r") as inputf:
        config = json.load(inputf)
    
    print(args.node_index)

    gateway_port = 9000 + int(args.node_index)
    swarm_port = 4002 + int(args.node_index)
    api_port = 5008 + int(args.node_index)
    config['Addresses']['Gateway'] =  '/ip4/127.0.0.1/tcp/' + str(gateway_port)
    config['Addresses']['Swarm'][0] = '/ip4/0.0.0.0/tcp/' + str(swarm_port)
    config['Addresses']['Swarm'][1] = '/ip6/::/tcp/' + str(swarm_port)
    config['Addresses']['API'] =      '/ip4/127.0.0.1/tcp/' + str(api_port)
    with open (ipfs_config_dir, "w") as myfile:
        json.dump(config,myfile)