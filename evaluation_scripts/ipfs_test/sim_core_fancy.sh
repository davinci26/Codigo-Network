#!/usr/bin/env bash
truncate -s 0 ./evaluation_scripts/ipfs_test/result.txt
kill $(pgrep -f 'ipfs')
#for k in `seq $1 $2 $3`
# For k IPFS nodes in range(1, step = $2, end = $3)
#do
    iptb init -n $1 -f --port 5008
    # TODO: Select UDP and MDNS
    iptb start -wait
    # Add file to first node
    head -c $2 </dev/urandom > file.txt
    file =$(iptb run 0 ipfs add -Q file.txt)
    rm file.txt
    for i in `seq 1 $1`
    do
        ipfs shell i
        python3 evaluation_scripts/ipfs_test/seeder.py --node_index $i --nodes 2 --file_hash $file
        exit
    done
    iptb stop
#done
kill $(pgrep -f 'ipfs')

# ========================================= HOW TO USE =========================================
# To Run: 
# $1 Nodes Start
# $2 Nodes Increment
# $3 Nodes End
# $4 File Size

