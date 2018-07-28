curl -X GET https://dist.ipfs.io/go-ipfs/v0.4.16/go-ipfs_v0.4.16_darwin-amd64.tar.gz > ipfs.tar.gz
tar xvfz ipfs.tar.gz
cd go-ipfs
./install.sh
cd ../
rm -rf go-ipfs/
rm ipfs.tar.gz
pip3 install numpy matplolib web3 ipfsapi pyqt5
npm install -g ganache-cli