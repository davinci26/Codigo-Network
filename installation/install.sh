#!/usr/bin/env bash
if [ "$(uname)" == "Darwin" ]; then
    brew install node
    brew install python3 
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    apt install python3-pip
    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
    apt-get install -y nodejs
fi
# Install IPFS
curl -X GET https://dist.ipfs.io/go-ipfs/v0.4.16/go-ipfs_v0.4.16_darwin-amd64.tar.gz > ipfs.tar.gz
tar xvfz ipfs.tar.gz
cd go-ipfs
./install.sh
cd ../
rm -rf go-ipfs/
rm ipfs.tar.gz
# Install Pip dependencies
pip3 install numpy matplolib web3 ipfsapi pyqt5
pip3 install py-solc
# Install Ganache
npm install -g ganache-cli