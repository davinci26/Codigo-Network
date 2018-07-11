#!/usr/bin/env bash
rm -rf ~/.ipfs_*

for k in `seq 1 $2 $3`;
    do
        ./evaluation_scripts/simulation_core.sh 
    done
    for i in {1..$k}
    do
        IPFS_PATH=~/.ipfs_$i ipfs init
        python3 evaluation_scripts/ipfs_test/config_editor.py --node_index $i
        IPFS_PATH=~/.ipfs_$i ipfs daemon &
    done

    for i in {1..$k}
    do
        python3 evaluation_scripts/ipfs_test/seeder.py --nodes $k --node_index $i --api_port `expr 5002 + $i` --file_hash $1 &
    done

    #Clean up processes
    pkill -f ipfs*
done
