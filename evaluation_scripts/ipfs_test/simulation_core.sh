#!/usr/bin/env bash
rm -rf ~/.ipfs_*

for i in `seq 1 $1`;
do
    IPFS_PATH=~/.ipfs_$i ipfs init
    python3 evaluation_scripts/ipfs_test/config_editor.py --node_index $i
    IPFS_PATH=~/.ipfs_$i ipfs daemon &
done

for i in `seq 1 $1`;
do
    python3 evaluation_scripts/ipfs_test/seeder.py --node_index $i --api_port `expr 5002 + $i` --file_hash $2 &
done

#Clean up processes
pkill -f ipfs*
