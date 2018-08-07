#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import argparse

save_dir = './evaluation_scripts/Plots/'

def parse_single_line(line, filepath, prv_users):
    d = json.loads(line)
    users = int(d['Users'])
    if prv_users and users - prv_users < 4:
        return
    if users > 110:
        return

    return d['Users'], d['Avg_Time'],d['Std_Time'], np.max(d['Results']),np.min(d['Results']),d['Results']

def parse_file(filepath):
    user_no = []
    delay_avg = []
    delay_std = []
    delay_max = []
    delay_min = []
    results = []
    prv_users = None
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            res = parse_single_line(line,filepath,prv_users)
            if res is not None:
                prv_users = res[0]
                user_no.append(res[0])
                delay_avg.append(res[1])
                delay_std.append(res[2])
                delay_max.append(res[3])
                delay_min.append(res[4])
                results.append(res[5])
            line = fp.readline()
    print(user_no)
    return user_no, delay_avg, delay_std, delay_max, delay_min, results

def plot(filepath,label,colour_,limit):
    user_no, delay_avg, delay_std, delay_max, delay_min,_ = parse_file(filepath)
    plt.plot(user_no[:limit], delay_avg[:limit],'o--', color=colour_, label=label + " Average delay",ms=3) #, yerr = delay_std, fmt='o' )
    plt.plot(user_no[:limit], delay_max[:limit],'--', color=colour_,  label=label + " Max delay",alpha=0.3) 
    plt.plot(user_no[:limit], delay_min[:limit],'--', color=colour_,label=label + " Min delay",alpha=0.3) 
    plt.fill_between(user_no[:limit],
                     delay_max[:limit],
                     delay_min[:limit],
                     color =colour_,
                     alpha=0.2 )
    plt.locator_params(nbins=14)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Average delay[sec]')
    plt.xlim(0,limit)


def statistics(filepath):
    results = parse_file(filepath)
    for results_row in results[5]:
        print(stats.describe(results_row))
        print("==========================================")


ipfs_path = './evaluation_scripts/datasets/ipfs_results.json'
server_path = './evaluation_scripts/datasets/server_results_new.json'
bittorent_path = './evaluation_scripts/datasets/bittorent_results.json'

# USAGE: ./evaluation_scripts/results_parser.py -o ipfs-vs-BitTorrent -IPFS -BitTorrent -save
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Line Interface')
    parser.add_argument('-o', type=str, nargs='?',
                        help="Save output to the specified directory")
    parser.add_argument('-IPFS', action='store_true', default = False,
                    help='Show IPFS performance')
    parser.add_argument('-user_limit', type=int, nargs='?', default = 120,
                    help='Limit number of users')
    parser.add_argument('-BitTorrent', action='store_true', default = False,
                    help='Show BitTorrent performance') 
    parser.add_argument('-client_server', action='store_true', default = False,
                    help='Show Client Server performance')   
    parser.add_argument('-statistics', action='store_true', default = False,
                    help='Print statistics')
    args = parser.parse_args()
    fig, ax1 = plt.subplots()

    if args.IPFS:
        plot(ipfs_path, "IPFS",'blue',args.user_limit)
        if args.statistics:
            statistics(ipfs_path)
    if args.BitTorrent:
        plot(bittorent_path,"BitTorrent",'orange',args.user_limit)
        if args.statistics:
            statistics(bittorent_path)
    if args.client_server:
        plot(server_path,"Client Server",'red',args.user_limit)

    plt.legend()
    if args.o != None:
        fig.savefig(save_dir + args.o +'.png',bbox_inches='tight') 
    else:
        plt.show()


