from web3.contract import ConciseContract


class Published_Contract:

    def __init__(self, abi_directory_, contract_name_, m_web3, address_,verbose = True):
        """ Contract constructor
        
        Arguments:
            directory_ {String/Directory} -- Contract directory
            contract_name_ {[type]} -- Contract name
            m_web3 {web3} -- Web3 instance

        Keyword Arguments:
            address_ {Ethereum Address} -- If the contract is already deployed (default: {None})
            verbose {bool} -- Print on console (default: {True})
        Raises:
            ValueError -- Throws a value error if Web3 instance is None
        """
        if verbose:
            print("========== Initializing {} ==========".format(contract_name_))
        if m_web3 == None:
            print("========== Failed to initialize  ==========")
            raise ValueError("Received uninitialized Web3 instance")
        self.address = address_
        self.directory = directory_ 
        self.name = contract_name_
        self.id = self.directory + ':' + self.name
        self.abi = self._contract_abi()
        self.verbose = verbose
        self.m_web3 = m_web3
    

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
        my_contract = self.m_web3.eth.contract(
            abi = self.abi,
            bytecode = compile_sol[self.id]['bin'], 
            bytecode_runtime = compile_sol[self.id]['bin-runtime']
        )
        trans_hash = my_contract.constructor().transact(transaction={'from':account_address})
        self.m_web3.eth.waitForTransactionReceipt(trans_hash)
        txn_receipt = self.m_web3.eth.getTransactionReceipt(trans_hash)
        self.address = txn_receipt['contractAddress']
        self.published = True
        if self.verbose:
            print("========== Contract Deployed Successfully ==========")
            print("Transaction Hash: {}".format(trans_hash))
            print("Transaction Receipt:\n{}".format(txn_receipt))
            print("Contract Address: {}".format(self.address))
        return self.address

    def _contract_abi(self):
        """ Compile contract and get the contract abi     
        Returns:
            [type] -- [description]
        """
        compile_sol = compile_files([self.directory])
        return compile_sol[self.id]['abi']

    def get_consice_instance(self):
        """ Return Consice Contract Instance (Look at web3py documentation)
        
        Raises:
            ValueError -- Raises a value error if the contract is not published to the blockchain
        
        Returns:
            [Web3 Contract] -- Web3 consice contract instance 
        """
        if self.address == None:
            raise ValueError("Contract not published to the blockchain")
        return self.m_web3.eth.contract(address=self.address, abi=self.abi, ContractFactoryClass=ConciseContract)
    
    def get_def_instance(self):
        """ Return Contract Instance (Look at web3py documentation)
        
        Raises:
            ValueError -- Raises a value error if the contract is not published to the blockchain
        
        Returns:
            [Web3 Contract] -- Web3 contract instance 
        """
        if self.address == None:
            raise ValueError("Contract not published to the blockchain")
        return self.m_web3.eth.contract(address=self.address, abi=self.abi)