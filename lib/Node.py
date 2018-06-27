import sys
sys.path.append("lib/")
from Contract import *
from ipfs_admin import *

class Node:
    # Default Initializer for every Node
    def __init__(self, m_web3, contract, pk, device_type, ipfs_instance):
        """ Node default constractor
        Arguments:
            m_web3 {Web 3} -- Web 3 instance
            contract {Contract} -- An instance of the deployed contract
            pk {Web 3 account} -- The address (public key) of the Node,
            device_type {String} -- Target IoT device
            ipfs_instance {IPFS Object} -- Open IPFS connection with a deamon
        """
        self.m_web3 = m_web3
        self.contract = contract 
        self.node_pk = pk
        self.device_type = str(device_type)
        self.ipfs = ipfs_instance
