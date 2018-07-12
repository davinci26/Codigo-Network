#!/usr/bin/env bash
rm -rf ~/.ipfs_*
kill $(pgrep -f 'ipfs daemon')
for k in `seq 1 $2 $3`
do
    for i in `seq 1 $k`
    do
        IPFS_PATH=~/.ipfs_$i ipfs init
        python3 evaluation_scripts/ipfs_test/config_editor.py --node_index $i
        IPFS_PATH=~/.ipfs_$i ipfs daemon &
    done
    sleep 10s
    echo "Initialized ipfs deamons"
    for j in `seq 1 $k`
    do
        python3 evaluation_scripts/ipfs_test/seeder.py --nodes $k --node_index $j --api_port `expr 5008 + $j` --file_hash $1 &
    done
    sleep 5s
    #Clean up processes
    kill $(pgrep -f 'ipfs daemon')
    rm -rf ~/.ipfs_*
done
rm -rf ./evaluation_scripts/ipfs_test/temp_*
#QmPZdXfEBLLogD8UZ4Ld9QSh2Q3P8jCQyPzrUCNtknFcNw
# Clean up in case of leftovers