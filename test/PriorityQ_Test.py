import unittest
import time
import sys
sys.path.append("lib/")
from Contract import *
from bc_admin import *

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()

class TestPriorityQ(unittest.TestCase):
    
    '''
    Test Case 1 (Correct Add)
    '''
    def test_q_insert(self):
        # Initialize and deploy contract
        contract = Contract('contracts/PQ.sol','PQ',m_web3,verbose=False)
        contract.publish_contract(m_web3, blockchain_admin.get_account(0))
        tx_hash = contract.get_contract_instance().insert(1,blockchain_admin.get_account(0), transact={'from': blockchain_admin.get_account(0)})
        m_web3.eth.waitForTransactionReceipt(tx_hash)
        self.assertEqual(contract.get_contract_instance().get_min_key(), 1)
    
    '''
    Test Case 2 (Add Multiple values)
    The q size is 7 at max
    Add 12 values and check if the correct ones are there
    '''
    def test_q_multiple_insert(self):    
        values_to_add = {1:False, 2:False, 3:False, 10:False, 11:False, 6:False,
                        7:False, 8:False, 9:False, 4:False, 5:False, 12:False}
        # Initialize and deploy contract
        contract = Contract('contracts/PQ.sol','PQ',m_web3,verbose=False)
        contract.publish_contract(m_web3, blockchain_admin.get_account(0))

        # Add values to the contract
        for key, _ in values_to_add.items():
            print("Added value: {}".format(key))
            tx_hash = contract.get_contract_instance().insert(key,blockchain_admin.get_account(0), transact={'from': blockchain_admin.get_account(0)})
            m_web3.eth.waitForTransactionReceipt(tx_hash)

        # Get values from the contract
        values_to_check = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False}
        
        # Get all values from the contract
        store_vals = {}
        for i in range(0,7):
            val = contract.get_contract_instance().get_specific_key(i)
            if val in values_to_check.keys():
                values_to_check[val] = True
            store_vals[val] = " "
        
        # Print the values found in the contract
        # Mostly for debbuging
        for key, value in values_to_check.items():
            print("Value {} Found: {}".format(key,value))

        # Calculate for Unit Test
        flag = True
        for _, value in values_to_check.items():
            flag = flag and value
        
        self.assertTrue(flag)

    '''
    Test Case 3 (Add Multiple values all negative)
    The q size is 7 at max
    Add 12 values and check if the correct ones are there
    '''
    def test_q_multiple_neg_insert(self):    
        values_to_add = {-1:False, -2:False, -3:False, -10:False, -11:False, -6:False,
                        -7:False, -8:False, -9:False, -4:False, -5:False, -12:False}
        # Initialize and deploy contract
        contract = Contract('contracts/PQ.sol','PQ',m_web3,verbose=False)
        contract.publish_contract(m_web3, blockchain_admin.get_account(0))

        # Add values to the contract
        for key, _ in values_to_add.items():
            print("Added value: {}".format(key))
            tx_hash = contract.get_contract_instance().insert(key,blockchain_admin.get_account(0), transact={'from': blockchain_admin.get_account(0)})
            m_web3.eth.waitForTransactionReceipt(tx_hash)

        # Get values from the contract
        values_to_check = {-12:False, -11:False, -10:False, -9:False, -8:False, -7:False, -6:False}
        
        # Get all values from the contract
        store_vals = {}
        for i in range(0,7):
            val = contract.get_contract_instance().get_specific_key(i)
            if val in values_to_check.keys():
                values_to_check[val] = True
            store_vals[val] = " "
        
        # Print the values found in the contract
        # Mostly for debbuging
        for key, value in values_to_check.items():
            print("Value {} Found: {}".format(key,value))

        # Calculate for Unit Test
        flag = True
        for _, value in values_to_check.items():
            flag = flag and value
        
        self.assertTrue(flag)
               
if __name__ == '__main__':
    unittest.main()