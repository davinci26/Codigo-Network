from web3.contract import ConciseContract
from solc import compile_files
from Abstract_Contract import *

class Contract(Abstract_Contract):

    def __init__(self, directory_, contract_name_, m_web3,address_ = None,verbose = True):
        """ Initializes a Contract Instance. The main difference between Contract and Compact Contract
            is the dependencies. This class is used mostly for debugging and deploys the contract as well.    
        Arguments:
            directory_ {String} -- Smart contract file directory
            contract_name_ {String} -- Name of the contract
            m_web3 {Web3} -- Web3 instance
        
        Keyword Arguments:
            address_ {Web3 Address} -- If the contract is already deployed. Use Compact contract in that case
                                       (default: {None})
            verbose {bool} -- Print on terminal (default: {True})
        
        Raises:
            ValueError -- Received uninitialized Web3 instance
        """
        try:
            super(Contract, self).__init__(contract_name_,m_web3,verbose)     
        except ValueError:
            raise ValueError("Received uninitialized Web3 instance")
        self.address = address_
        self.name = contract_name_
        self.directory = directory_
        self.id = self.directory + ':' + self.name
        self.deployment_cost = 0
    

    def publish(self, account_address):
        """Publish Contract to the blockchain
        Arguments:
            account_address {Ethereum Address} -- Contract deployer
        Raises:
            ValueError -- Raises value error if the contract is already deployed
        Returns:
            [Address] -- Contract address
        """
        if self.address != None:
            raise ValueError("Contract already published to the blockchain")
        compile_sol = compile_files([self.directory], evm_version='homestead')
        self.abi = compile_sol[self.id]['abi']
        my_contract = self.m_web3.eth.contract(
            abi = self.abi,
            bytecode = compile_sol[self.id]['bin'], 
            bytecode_runtime = compile_sol[self.id]['bin-runtime']
        )
        trans_hash = my_contract.constructor().transact(transaction={'from':account_address})
        self.m_web3.eth.waitForTransactionReceipt(trans_hash)
        txn_receipt = self.m_web3.eth.getTransactionReceipt(trans_hash)
        self.address = txn_receipt['contractAddress']
        self.deployment_cost = txn_receipt['cumulativeGasUsed']
        self.published = True
        if self.verbose:
            print("========== Contract Deployed Successfully ==========")
            print("Transaction Hash: {}".format(trans_hash))
            print("Transaction Receipt:\n{}".format(txn_receipt))
            print("Contract Address: {}".format(self.address))
        return self.address

    def save_abi(self,abi_directory):
        import json
        """Save Contract ABI
        Arguments:
            abi_directory {String/Directory} -- Where to save the contract ABI
        Raises:
            ValueError -- If the contract is not compiled/published yet then it throws
        """
        if self.address == None:
            raise ValueError("Contract is not compiled yet.")

        with open(abi_directory, 'w') as contract_abi:
            json.dump(self.abi, contract_abi)