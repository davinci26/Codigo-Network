#!/usr/bin/env bash
rm -rf ~/.ipfs_* # Kill leftovers from previous run that did not terminate succesfully
rm -rf ./evaluation_scripts/ipfs_test/temp_*
kill $(pgrep -f 'ipfs daemon')
while pgrep ipfs > /dev/null; do sleep 1; done
# Spawn master IPFS node
ipfs daemon &
# For k IPFS nodes in range(1, step = $2, end = $3)
for k in `seq 1 $2 $3`
do
    # Spawn K fresh IPFS Nodes
    for i in `seq 1 $k`
    do
        IPFS_PATH=~/.ipfs_$i ipfs init
        python3 evaluation_scripts/ipfs_test/config_editor.py --node_index $i
        IPFS_PATH=~/.ipfs_$i ipfs daemon &
        echo "============================= Initalizing User: $i / $k ==================================="
    done
    echo "Initialized all ipfs deamons"
    inst=$(pgrep ipfs | wc -l)
    while ( $inst <  `expr 1 + $k`); do inst=$(pgrep ipfs | wc -l); sleep 1; done

    # Warm up the IPFS Nodes
    for i in `seq 1 $k`
    do
        IPFS_PATH=~/.ipfs_$i {time ipfs cat QmeVELMStAfb6aWQD9zZSEDqJjo84Ht2T1Kkede1D54cj5;} 2> time.txt
        echo "============================= Warm up Node: $i / $k ==================================="
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
    rm ./evaluation_scripts/ipfs_test/ipfs_node_*
    echo "============================= Finished Iteration: $l / $3 ==================================="
done
rm -rf ./evaluation_scripts/ipfs_test/temp_*

# ========================================= USAGE =========================================
# To Run: evaluation_scripts/ipfs_test/simulation_core.sh QmNRcwA5oY1uyxYLimKneFLkrUjSJonrZ3V6nPBn2adFgB 1 2
# Large: QmPZdXfEBLLogD8UZ4Ld9QSh2Q3P8jCQyPzrUCNtknFcNw
# Small: QmNRcwA5oY1uyxYLimKneFLkrUjSJonrZ3V6nPBn2adFgB
# Warm up: QmeVELMStAfb6aWQD9zZSEDqJjo84Ht2T1Kkede1D54cj5
# Clean up in case of leftovers
