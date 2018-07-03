from web3.contract import ConciseContract


class Abstract_Contract:

    def __init__(self, contract_name_, m_web3,verbose = True):
        """ Abstract Contract constructor
        Arguments:
            contract_name_ {String} -- Contract name
            m_web3 {web3} -- Web3 instance
        Keyword Arguments:
            verbose {bool} -- Print on console (default: {True})
        Raises:
            ValueError -- Throws a value error if Web3 instance is None
        """
        if verbose:
            print("========== Initializing {} ==========".format(contract_name_))
        if m_web3 == None:
            print("========== Failed to initialize  ==========")
            raise ValueError("Received uninitialized Web3 instance")
        self.m_web3 = m_web3
        self.verbose = verbose
        # Values that need to be initialized by base class #
        self.abi = None
        self.address = None
    
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