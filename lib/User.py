import sys
sys.path.append("lib/")
from Contract import *
from Node import *
import heapq
from heapq import heappush, heappop

capacity = 7
def custom_push(h,value,key):
    if len(h) < capacity:
        heapq.heappush(h, (value,key))
    else:
        heapq.heappushpop(h, (value,key))

class User_Node(Node):

    def __init__(self, m_web3, contract, pk, device_type,ipfs_instance):
        """ User Node inherits from Node
        Arguments:
            m_web3 {Web 3} -- Web 3 instance
            contract {Contract} -- An instance of the deployed contract
            pk {Web 3 account} -- The address (public key) of the Node,
            device_type {String} -- Target IoT device
            ipfs_instance {IPFS Object} -- Open IPFS connection with a deamon
        """
        Node.__init__(self,m_web3, contract, pk, device_type,ipfs_instance)

    def get_specific_fw(self, dev_address, stable = True):
        fw = self.contract.get_def_instance().functions.get_firmware(self.device_type,dev_address,stable).call()
        return fw

    def get_most_trusted_fw(self, stable = True):
        """Retrieve the metadata for the most trusted firmware
        Keyword Arguments:
            firmware_stable {bool} -- LTS (True) or Latest Commit (default: {True})
        Returns:
            Web3 tx receipt -- All the information for the tx including Gas Cost
        """
        fw = self.contract.get_def_instance().functions.get_most_trusted_firmware(self.device_type,stable).call()
        return fw
    
    def get_mult_trusted_fw_local(self, web_trust_contract, stable = True):
        """Retrieve the metadata for the 7 most trusted firmware.
        
        Arguments:
            web_trust_contract {Contract} -- An instance of web of trust contract

        Keyword Arguments:
             firmware_stable {bool} -- LTS (True) or Latest Commit (default: {True})
        
        Returns:
            [Array[6]] -- Contains the following fw_hash,fw_ipfs,fw_descr,fw_block,fw_dev,trust 
        """
        PQ = []
        flag = True
        i = 0
        # In solidity we cant return dynamically allocated arrays from contracts
        # We access specific index of the array until we get an exception
        # Probably not the best idea :( but it works
        while (flag):
            try:
                temp_addr = self.contract.get_def_instance().functions.get_developer(self.device_type,i).call()
                i += 1
            except:
                print("Number of developers: {}".format(i))
                flag = False
                continue
            # Calculate how much we trust the developer temp_addr
            trust = web_trust_contract.get_def_instance().functions.hop_to_target(temp_addr,self.node_pk).call()
            print('Trust to developer {} is {}'.format(temp_addr,trust))
            if trust != -1:
                custom_push(PQ,int(trust),temp_addr)
        
        # Now we empty the Q and populate the firmware list
        fw = []
        while PQ:
            value_key = heappop(PQ)
            to_add = self.get_specific_fw(value_key[1],stable) + [value_key[1],value_key[0]]
            fw.append(to_add)
        return fw

    def get_mult_trusted_tx(self, stable = True):
        pass #TODO: Refactor contract to implement that without deploying a PQ
        #fw = self.contract.get_def_instance().functions.get_most_trusted_firmware(self.device_type,stable).call()
        #return fw
    
    def endorse_developer(self,trust_web,target_pk):
        """ Allocate trust to a developer
        
        Arguments:
            trust_web {Contract} -- Web of trust contract instance
            target_pk {PK} -- PK of the trusted developer
    
        Returns:
            Transaction receipt
        """
        tx_hash = trust_web.get_def_instance().functions.endorse_trust(target_pk).transact()
        tx_receipt = self.m_web3.eth.getTransactionReceipt(tx_hash)
        return tx_receipt

    def download_firmware(self,ipfs_link):
        self.ipfs.download_firmware(ipfs_link)
