#!/usr/bin/env bash
rm -rf ~/.ipfs_* # Kill leftovers from previous run that did not terminate succesfully
rm -rf ./evaluation_scripts/ipfs_test/temp_*
truncate -s 0 ./evaluation_scripts/ipfs_test/result.txt
kill $(pgrep -f 'ipfs daemon')
while pgrep ipfs > /dev/null; do sleep 1; done
# Spawn master IPFS node
ipfs daemon &
for k in `seq $2 $3 $4`
# For k IPFS nodes in range(1, step = $2, end = $3)
do
    for i in `seq 1 $k`
    # Spawn K fresh IPFS Nodes
    do
        IPFS_PATH=~/.ipfs_$i ipfs init
        python3 evaluation_scripts/ipfs_test/config_editor.py --node_index $i
        IPFS_PATH=~/.ipfs_$i ipfs daemon &
        echo "============================= Initalizing User: $i / $k ==================================="
    done
    
    while ! curl --silent localhost:`expr 5008 + $k`
    # Wait for the last deamon to be fully initialized
    # Hack from go-ipfs issue #862
    do
        echo "I wait"
        sleep 1
    done

    for l in `seq 1 $k`
    do
        IPFS_PATH=~/.ipfs_$l time ipfs cat QmeVELMStAfb6aWQD9zZSEDqJjo84Ht2T1Kkede1D54cj5
        echo "============================= Warm up Node: $l / $k ==================================="
    done

    # Download IPFS Nodes
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

# ========================================= HOW TO USE =========================================
# To Run: evaluation_scripts/ipfs_test/simulation_core.sh QmNRcwA5oY1uyxYLimKneFLkrUjSJonrZ3V6nPBn2adFgB 1 2
# Large: QmPZdXfEBLLogD8UZ4Ld9QSh2Q3P8jCQyPzrUCNtknFcNw
# Small: QmNRcwA5oY1uyxYLimKneFLkrUjSJonrZ3V6nPBn2adFgB
# Warm up: QmeVELMStAfb6aWQD9zZSEDqJjo84Ht2T1Kkede1D54cj5
# Clean up in case of leftovers
