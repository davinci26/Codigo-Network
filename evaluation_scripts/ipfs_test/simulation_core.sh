#!/usr/bin/env bash
rm -rf ~/.ipfs_*
rm -rf ./evaluation_scripts/ipfs_test/temp_*
kill $(pgrep -f 'ipfs daemon')
while pgrep ipfs > /dev/null; do sleep 1; done
ipfs daemon &
for k in `seq 1 $2 $3`
do
    for i in `seq 1 $k`
    do
        IPFS_PATH=~/.ipfs_$i ipfs init
        python3 evaluation_scripts/ipfs_test/config_editor.py --node_index $i
        IPFS_PATH=~/.ipfs_$i ipfs daemon &
        echo "============================= Initalizing User: $i / $k ==================================="
    done
    sleep 10s
    echo "Initialized all ipfs deamons"
    for j in `seq 1 $k`
    do
        python3 evaluation_scripts/ipfs_test/seeder.py --nodes $k --node_index $j --api_port `expr 5008 + $j` --file_hash $1
        echo "=============================  Seeder: $j / $k ==================================="
    done
    while pgrep python > /dev/null; do sleep 1; done
    #merge temp files
    python3 evaluation_scripts/ipfs_test/merger.py --nodes $k
    #Clean up processes
    for i in `seq 1 $k`
    do
        IPFS_PATH=~/.ipfs_$i ipfs shutdown
        IPFS_PATH=~/.ipfs_$i ipfs shutdown
    done
    rm -rf ~/.ipfs_*
    rm ./evaluation_scripts/ipfs_test/ipfs_nodes_*
    echo "============================= Finished Iteration: $l / $3 ==================================="
done
rm -rf ./evaluation_scripts/ipfs_test/temp_*
# Large: QmPZdXfEBLLogD8UZ4Ld9QSh2Q3P8jCQyPzrUCNtknFcNw
# Small: QmNRcwA5oY1uyxYLimKneFLkrUjSJonrZ3V6nPBn2adFgB
# Clean up in case of leftovers