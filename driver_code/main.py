import sys
sys.path.append("lib/")
from bc_admin import *
from Contract import *
from Developer import *
from User import *

device_t = 1

# Deploy BC
blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
# Deploy Contract
cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
cc.publish(blockchain_admin.get_account(0))
# Push Firmware
developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
developer_node.add_firmware()
# Pull Firmware
user_node = User_Node(m_web3, cc, blockchain_admin.get_account(0), device_t)
fw = user_node.get_specific_fw(blockchain_admin.get_account(0))
print(fw)