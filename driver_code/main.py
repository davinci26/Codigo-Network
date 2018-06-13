from bc_admin import *
from Contract import *
from Firmware import *

# Establish connection with BC

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
primary_acc = blockchain_admin.get_account(0)

# Initialize and deploy contract
contract = Contract('contracts/firmware_repo.sol','FirmwareRepo',m_web3)
contract.publish_contract(m_web3, primary_acc)
#contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
print('Contract version: {}'.format(contract.get_contract_instance().get_version()))


