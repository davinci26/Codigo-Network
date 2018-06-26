import unittest
import time
import sys
sys.path.append("lib/")
from Contract import *
from bc_admin import *
from Developer import *
from User import *

import logging
logging.basicConfig(filename='./logs/example.log',level=logging.DEBUG)

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
device_t = 1

class TestFwRepo(unittest.TestCase):
    
    '''
    Test Case 1 (Correct Compilation & Deployment)
    '''
    def test_compile_deploy(self):
        # Initialize and deploy contract
        contract = Contract('contracts/firmware_repo.sol','FirmwareRepo',m_web3,verbose=False)
        tx_hash = contract.publish(blockchain_admin.get_account(0))
        value = contract.get_def_instance().functions.get_version().call()
        self.assertEqual(value,2)

    '''
    Test Case 2 (Basic interaction with contract)
    Set new version Get new version of the Contract
    '''
    def test_basic_interaction(self):
        # Initialize and deploy contract
        contract = Contract('contracts/firmware_repo.sol','FirmwareRepo',m_web3,verbose=False)
        tx_hash = contract.publish(blockchain_admin.get_account(0))
        print("Contract deployed with tx hash: {}".format(tx_hash))
        # Set the contract version to 10
        tx_hash = contract.get_def_instance().functions.set_version(10).transact()
        print("Contract returned: {} value is {}".format(tx_hash,blockchain_admin.get_account(0)))
        #m_web3.eth.waitForTransactionReceipt(tx_hash)
        # Get contract version
        value = contract.get_def_instance().functions.get_version().call()
        print("New contract version {}".format(value))
        self.assertEqual(value,10)

    '''
    Test Case 3 (Basic interaction with contract)
    Set new version Get new version of the Trust Contract
    '''
    def test_nested_contract(self):
        # Initialize and deploy contract
        contract = Contract('contracts/firmware_repo.sol','FirmwareRepo',m_web3,verbose=False)
        contract.publish(blockchain_admin.get_account(0))
        #Set the trust contract version to 10
        tx_hash = contract.get_def_instance().functions.set_trust_version(10).transact()
        print("Tx Hash: {}".format(tx_hash))
        m_web3.eth.waitForTransactionReceipt(tx_hash)
        #Get the trust contract version
        value = contract.get_def_instance().functions.get_trust_version().call()
        print("New contract version {}".format(value))
        self.assertEqual(value,10)

    '''
    Test Case 4 ( Push - Pull Firmware)
    Upload a firmware to the blockchain and then retrieve it back.
    '''
    def test_get_specific(self):
        # Deploy Contract
        cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
        cc.publish(blockchain_admin.get_account(0))
        # Create Developer node with PK(1)
        developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
        # Push Firmware
        developer_node.add_firmware()
        print("Pushed - Fw description: {}".format(developer_node.fw.description[:10]))
        # Create User node with PK(0)
        user_node = User_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
        # Pull Firmware - Specific
        fw_hash,fw_ipfs,fw_descr,fw_block = user_node.get_specific_fw(blockchain_admin.get_account(0))
        #val = user_node.get_specific_fw(blockchain_admin.get_account(0))
        print("Pulled - Fw description: {}".format(fw_descr[:10]))
        self.assertEqual(fw_descr,developer_node.fw.description)

    '''
    Test Case 5 ( - Pull Firmware)
    Retrieve a firmware that does not exist
    '''
    def test_get_specific_fail(self):
        # Deploy Contract
        cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
        cc.publish(blockchain_admin.get_account(0))
        # Create User node with PK(0)
        user_node = User_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
        # Pull Firmware - Specific
        flag = False
        try:
            fw_hash,fw_ipfs,fw_descr,fw_block = user_node.get_specific_fw(blockchain_admin.get_account(0))
        except:
            print("Transaction failure caught successfully")
            flag = True
        self.assertTrue(flag)


    '''
    Test Case 5 ( Push - Trust - Pull Firmware)
    Upload a firmware to the blockchain, trust the developer tha upload it
    and then retrieve it back from most trusted.
    '''
    def test_most_trusted(self):
        # Deploy Contract
        cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
        cc.publish(blockchain_admin.get_account(0))
        # Get web of trust address
        web_of_trust_addr = cc.get_def_instance().functions.trust_address().call()
        print("Web of Trust Address: {}".format(web_of_trust_addr))
        # Initialize web of trust contract
        web_of_trust = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False, address_ = web_of_trust_addr)
        # Test that web of trust works
        print("Web of Trust Version: {} ".format(web_of_trust.get_def_instance().functions.get_version().call()))
        # Create Developer node with PK(1)
        developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(1), device_t)
        # Push Firmware
        developer_node.add_firmware()
        print("Pushed - Fw description: {}".format(developer_node.fw.description[:10]))
        # Create User node with PK(0)
        user_node = User_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
        # Trust Developer PK(1)
        user_node.endorse_developer(web_of_trust, blockchain_admin.get_account(1))
        # Pull Firmware - Most Trusted
        fw_hash,fw_ipfs,fw_descr,fw_block,fw_dev,trust = user_node.get_most_trusted_fw()
        print("Pulled - Fw description: {} with trust {}".format(fw_descr[:10],trust))
        self.assertEqual(fw_descr,developer_node.fw.description)
    
    '''
    Test Case 6 ( Push - No Trust - Pull Firmware)
    Upload a firmware to the blockchain and retrieve most trusted.
    '''
    def test_most_trusted_fail(self):
        # Deploy Contract
        cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
        cc.publish(blockchain_admin.get_account(0))
        # Create Developer node with PK(1)
        developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(1), device_t)
        # Push Firmware
        developer_node.add_firmware()
        print("Pushed - Fw description: {}".format(developer_node.fw.description[:10]))
        # Create User node with PK(0)
        user_node = User_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
        # Pull Firmware - Most Trusted
        try:
            fw_hash,fw_ipfs,fw_descr,fw_block,fw_dev,trust = user_node.get_most_trusted_fw()
        except:
            print("Transaction failure caught successfully")
            flag = True
        self.assertTrue(flag)

    def test_multiple_trusted(self):
        # Deploy Contract
        cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
        cc.publish(blockchain_admin.get_account(0))
        # Get web of trust address
        web_of_trust_addr = cc.get_def_instance().functions.trust_address().call()
        print("Web of Trust Address: {}".format(web_of_trust_addr))
        # Initialize web of trust contract
        web_of_trust = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False, address_ = web_of_trust_addr)
        # Test that web of trust works
        print("Web of Trust Version: {} ".format(web_of_trust.get_def_instance().functions.get_version().call()))
        # Create User node with PK(0)
        user_node = User_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
        fw_dictionary = {}
        # Create 7 developers, let them push fw and then trust them
        for i in range(1,8):
            # Create Developer node with PK(1)
            developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(i), device_t)
            # Push Firmware
            developer_node.add_firmware()
            print("Pushed - Fw description: {} from dev {}".format(developer_node.fw.description[:10],blockchain_admin.get_account(i)))
            # Store Firmware locally
            fw_dictionary[developer_node.fw.description] = False
            # Endore developer
            user_node.endorse_developer(web_of_trust,blockchain_admin.get_account(i))
            logging.info("User {} endorsed {}".format(blockchain_admin.get_account(0),blockchain_admin.get_account(i)))   
        # Pull contracts
        fw_list = user_node.get_mult_trusted_fw_local(web_of_trust)
        for fw in fw_list:
            #unpack fw
            fw_hash,fw_ipfs,fw_descr,fw_block,fw_dev,trust = fw
            #Set to True
            fw_dictionary[fw_descr] = True

        # Print Everything for debuging
        for key, value in fw_dictionary.items():
            print("Value {} Found: {}".format(key[:10],value))

        # Calculate that everything is found
        flag = True
        for _, value in fw_dictionary.items():
            flag = flag and value
        
        self.assertTrue(flag)

if __name__ == '__main__':
    unittest.main()