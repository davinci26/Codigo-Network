#!/usr/bin/env bash

if ! pgrep -f "node /usr/local/bin/ganache-cli" >> /dev/null
then
    echo "Error: You need to have a ganache-cli instance up to run the tests"
    exit -1
fi

if ! pgrep -f "ipfs daemon" >> /dev/null
then
    echo "Error: You need to have an ipfs daemon instance up to run the tests"
    exit -1
fi

# Run tests 
python3 test/web_trust_test.py -v
python3 test/PriorityQ_Test.py -v
python3 test/fw_repo_test.py -v
# Clear temporary files
./clear_logs.sh
