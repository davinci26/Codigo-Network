import sys
sys.path.append("lib/")
from Firmware import *
from Node import *

class Developer_Node(Node):

    def __init__(self, m_web3, contract, pk, device_type, ipfs_instance):
        """ Developer Node inherits from Node
        Arguments:
            m_web3 {Web 3} -- Web 3 instance
            contract {Contract} -- An instance of the deployed contract
            pk {Web 3 account} -- The address (public key) of the Node,
            device_type {String} -- Target IoT device
            ipfs_instance {IPFS Object} -- Open IPFS connection with a deamon
        """
        Node.__init__(self,m_web3, contract, pk, device_type,ipfs_instance)
        self.fw = None

    def add_firmware(self, firmware_stable, firmware_file ,firmware_description = ""):
        """ The developer Node adds a firmware to the blockchain
        
        Keyword Arguments:
            firmware_stable {bool} -- LTS (True) or Latest Commit (default: {True})
            firmware_file {Directory} -- Firmware directory,
                                        if None then firmware
                                         is generated randomly (default: {None})
        
        Returns:
            Web3 tx receipt -- All the information for the tx including Gas Cost
        """
        #TODO: Exceptions, if this doesnt work for some reason it breaks.
        # Create/locate firmware
        self.fw = Firmware(self.device_type, firmware_stable, firmware_file , firmware_description)
        # Upload Firmware to IPFS
        res = self.ipfs.upload_firmware(self.fw)
        # Set up the firmware IPFS link
        self.fw.set_ipfs_link(res['Hash'])
        # Add it to blockchain
        print(self.fw)
        tx_hash = self.contract.get_consice_instance().add_firmware(self.fw.firmware_hash, self.fw.IPFS_link,
                                                           self.fw.description, self.fw.device_type,
                                                           self.fw.stable,transact={'from': self.node_pk})
        tx_receipt = self.m_web3.eth.getTransactionReceipt(tx_hash)
        self.fw.tx_cost = tx_receipt['cumulativeGasUsed']
        # Return tx receipt
        return tx_receipt

    def edit_firmware(self,description_):
        """ The developer node updates the description of a deployed
        Arguments:
            description_ {string} -- New description
        Raises:
            ValueError -- If the developer has not added a firmware to the blockchain
        Returns:
            Web3 tx receipt -- All the information for the tx including Gas Cost
        """
        if self.fw == None:
            raise ValueError("The developer has no firmware in the blockchain")
        tx_hash = self.contract.get_def_instance().functions.edit_description(description_,self.fw.device_type,self.fw.stable).transact()
        txn_receipt = self.m_web3.eth.getTransactionReceipt(tx_hash)
        return txn_receipt


"""
Driver Code to use the Class

from bc_admin import *
blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
cc.publish(blockchain_admin.get_account(0))
developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
developer_node.add_firmware()
val = cc.get_def_instance().functions.get_firmware(str(device_t),blockchain_admin.get_account(0),True).call()
print(val)

"""
