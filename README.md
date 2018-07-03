# Código Network #
A firmware distribution framework using blockchain Technology & IPFS
## Project Abstract ##

With the number of Internet of Things (IoT) devices exponentially increasing, distributing firmware updates through the network becomes a necessity in the IoT ecosystem. This project implements a mechanism for efficient distributed firmware updates for IoT devices. In this project, the feasibility of using blockchain technology for distributing firmware updates will be evaluated experimentally. At minimum a firmware distribution scheme must implement two basic features. First, end-devices should be able to check whether their firmware version is up-to-date. Second, in case they are not, they should be able to find the address and establish connection with other end-devices that are willing to share the newest firmware. Decentralized software updates for IoT devices have many merits, they reduces update time, enable open source development and ensure devices can be maintained by the community even if the vendor goes bankrupt. In this project, these high level aims are broken down and translated into specific objectives. These objectives include researching available clients (blockchains and distributed file systems) suitable for IoT devices and implementing a smart contract that will be used as a firmware repository and a distributed file system client for downloading the firmware. Finally, a methodology is implemented for translating these objectives into a prototype firmware distribution scheme. To evaluate the framework, various metrics are suggested. More specifically, the smart contract will be analyzed in terms of static security and computational performance. Finally, the client interacting with the distributed file system will be analyzed in terms of download latency and scalability.

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
