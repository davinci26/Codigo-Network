import sys
sys.path.append("lib/")
from Contract import *
from bc_admin import *
import unittest
import time

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()

class TestTrust(unittest.TestCase):

    '''
    Utility functions for testing the smart-contract
    add_rand_addresses: Node alice (tx_origin) trusts n random(number) nodes
    add_all_known: Add all nodes provided by the testRPC to trust each other
    In all cases -> denotes trust. E.g. if Alice trusts Bob we write Alice -> Bob
    '''
    def add_single_address(self,origin,target,contract):
        tx_hash =contract.get_consice_instance().endorse_trust(target, transact={'from': origin})
        # Wait for transaction to be mined...
        m_web3.eth.waitForTransactionReceipt(tx_hash)
    
    '''
    Test Case 0 (Correct Deployment)

    '''
    def test_connection(self):
        # Initialize and deploy contract
        contract = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False)
        contract.publish(blockchain_admin.get_account(0))
        # Set Version
        tx_hash = contract.get_consice_instance().set_version(10, transact={'from': blockchain_admin.get_account(0)})
        # Get Version
        m_web3.eth.waitForTransactionReceipt(tx_hash)
        value = contract.get_consice_instance().get_version()
        print("Contract was set to Version 10 and received {}".format(value))
        self.assertEqual(10,value)


    '''
    Test Case 1 (Single Hop)
        Acc0 -> Acc1
        Trust(Acc1,Acc2) == 1
    '''
    def test_calculate_trust_normal_case(self):
        # Initialize and deploy contract
        contract = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False)
        contract.publish(blockchain_admin.get_account(0))
        # Add addresses
        self.add_single_address(blockchain_admin.get_account(0),blockchain_admin.get_account(1),contract)
        # Calculate Trust
        trust = contract.get_consice_instance().hop_to_target(blockchain_admin.get_account(1))
        self.assertEqual(trust, 1)

    '''
    Test Case 2 (Normal Case)
        Acc0 -> Acc1 -> Acc2
        Trust(Acc0,Acc2) == 2
    '''
    def test_trust_multiple_hop(self):
        # Initialize and deploy contract
        contract = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False)
        contract.publish(blockchain_admin.get_account(0))
        # Add addresses
        self.add_single_address(blockchain_admin.get_account(0),blockchain_admin.get_account(1), contract)
        self.add_single_address(blockchain_admin.get_account(1),blockchain_admin.get_account(2),contract)
        # Calculate Trust
        trust = contract.get_consice_instance().hop_to_target(blockchain_admin.get_account(2))
        self.assertEqual(trust, 2)

    '''
    Test Case 3 (Cyclical Case)
        Acc1 -> Acc2
        Acc2 -> Acc1
        Trust(Acc1,Acc3) == -1
    '''
    def test_calculate_trust_cyclical_case(self):
        # Initialize and deploy contract
        contract = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False)
        contract.publish(blockchain_admin.get_account(0))
        # Add addresses
        self.add_single_address(blockchain_admin.get_account(0),blockchain_admin.get_account(1), contract)
        self.add_single_address(blockchain_admin.get_account(1),blockchain_admin.get_account(0), contract)
        # Calculate Trust
        trust = contract.get_consice_instance().hop_to_target(blockchain_admin.get_account(2))
        self.assertEqual(trust, -1)
    
    '''
    Test Case 4 (Competing connections)
    Acc0 -> Acc1 -> Acc2 -> Acc3 -> Acc4 -> Acc5
    Acc1 -> Acc5
    Trust(Acc0,Acc5) == 3
    '''
    def test_calculate_trust_competing_conn(self):
        # Initialize and deploy contract
        contract = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False)
        contract.publish(blockchain_admin.get_account(0))
        # Add addresses
        for i in range(0,5):
            self.add_single_address(blockchain_admin.get_account(i),blockchain_admin.get_account(i+1),contract)
        self.add_single_address(blockchain_admin.get_account(2),blockchain_admin.get_account(5),contract)
        # Calculate Trust
        trust = contract.get_consice_instance().hop_to_target(blockchain_admin.get_account(5))
        self.assertEqual(trust, 3)

def test():
    unittest.main()

if __name__ == '__main__':
    unittest.main()