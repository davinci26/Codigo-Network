from Abstract_Contract import *
from web3.contract import ConciseContract
import json

class Compact_Contract(Abstract_Contract):

    def __init__(self, abi_directory, contract_name_, m_web3, address_,verbose = True):
        try:
            super(Compact_Contract, self).__init__(contract_name_,m_web3,verbose)     
        except ValueError:
            raise ValueError("Received uninitialized Web3 instance")
        self.address = address_
        try:
            with open(abi_directory, 'r') as contract_abi:
                self.abi = json.load(contract_abi)
        except IOError:
             raise IOError("Contract ABI file was not found")