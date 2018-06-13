from solc import compile_files
from web3.contract import ConciseContract


class Contract:

    def __init__(self, directory_, contract_name_,m_web3,address_ = None, verbose = True):
        if verbose:
            print("========== Initializing {} ==========".format(contract_name_))
        if m_web3 == None:
            print("========== Failed to initialize  ==========")
            raise ValueError("Received uninitialized Web3 instance")
        self.address = address_
        self.directory = directory_
        self.name = contract_name_
        self.id = self.directory + ':' + self.name
        self.abi = self.__contract_abi()
        self.verbose = verbose
        self.m_web3 = m_web3
    
    def publish_contract(self, web3, account_address):
        compile_sol = compile_files([self.directory])
        my_contract = web3.eth.contract(
            abi = self.abi,
            bytecode = compile_sol[self.id]['bin'], 
            bytecode_runtime = compile_sol[self.id]['bin-runtime']
        )
        trans_hash = my_contract.deploy(transaction={'from':account_address})
        txn_receipt = web3.eth.getTransactionReceipt(trans_hash)
        contract_address = txn_receipt['contractAddress']
        self.address = contract_address
        if self.verbose:
            print("========== Contract Deployed Successfully ==========")
            print("Transaction Hash: {}".format(trans_hash))
            print("Transaction Receipt:\n{}".format(txn_receipt))
            print("Contract Address: {}".format(contract_address))
        return contract_address

    def __contract_abi(self):
        compile_sol = compile_files([self.directory])
        return compile_sol[self.id]['abi']

    def get_contract_instance(self):
        return self.m_web3.eth.contract(address=self.address, abi=self.abi,ContractFactoryClass=ConciseContract)