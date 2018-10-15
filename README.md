# Código Network #
A firmware distribution framework using blockchain Technology & IPFS

## Project Motivation ##

For Código network, we set the following requirements: (i) no single point of failure, (ii) equivalent security with code signing, (iii) transparency of firmware updates and (iv) scalability. To fulfill the aforerementioned requirements, Código network is implemented on top of the Ethereum blockchain and the IPFS network. In our developed system, developers upload firmware to a  repository, implemented as a Ethereum decentralized application. In parallel, users can browse the repository for trusted firmware and download the firmware. To encapsulate trust in a decentralized network, we develop an open-source implementation of Web-of-Trust as an Ethereum smart-contract.


![ipfs-archi](https://user-images.githubusercontent.com/32749078/44346684-7af52e80-a48e-11e8-80f6-f65b46216289.png)

![repo-archi](https://user-images.githubusercontent.com/32749078/44346740-9e1fde00-a48e-11e8-846d-2c71c61c0033.png)


Código network architecture diagram. Users are arranged on a graph based on their trust relationship, which is formalized in the Web-of-Trust smart-contract. Firmware metadata are stored on the firmware repository smart-contract and updated using the Código clients. Firmware distribution is on the IPFS layer in which the Código client is uploading/downloading the firmware from the IPFS network.

## Project Structure ##

- Contracts: Smart contracts used to encapsulate the business logic of the project. The contracts include, a firmware    repository and a decentralized trust metric calculator.
- Driver code: Python scripts to emulate developers, IoT devices and seeders.
- Unit Testing: Pre-set experiments to model the performance of the system.

## Dependencies (TBD) ##
 - [Solidity](https://github.com/ethereum/solidity)
 - [IPFS](https://github.com/ipfs/ipfs)
 - [Web3Py](https://github.com/ethereum/web3.py)
 - [Truffle](https://github.com/trufflesuite/truffle-contract)
 - [Ganache-cli](https://github.com/trufflesuite/ganache-cli)
 - [PyQt5](https://github.com/pyqt) (Optional)
 
 Smart contract libraries used in the project will be added to the contracts folder.

 This project is merely a combination of existing solutions developed by the open source community. Thus it would be disrespectful not to thank the developing teams of the projects above for their help.

## How to contribute ##
Any comments/suggestions/improvements are highly appreciated. However, until the project is submitted for grading no pull requests will be accepted.

## Why is it called Codigo-Network ##
For the coolness factor of having a spanish name :) 

