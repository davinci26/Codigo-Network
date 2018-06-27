import sys
sys.path.append("lib/")
from bc_admin import *
from ipfs_admin import *
from Contract import *
from Developer import *
from User import *

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
ipfs_admin = IPFS_Admin(local = True)
device_t = 1
# Deploy Contract
cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
cc.publish(blockchain_admin.get_account(0))
# Create Developer node with PK(1)
developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(0), device_t,ipfs_admin)
# Push Firmware
developer_node.add_firmware()
print("Pushed - Fw description: {}".format(developer_node.fw.description[:10]))
# Create User node with PK(0)
user_node = User_Node(m_web3, cc, blockchain_admin.get_account(0), device_t,ipfs_admin)
# Pull Firmware - Specific
fw_hash,fw_ipfs,fw_descr,fw_block = user_node.get_specific_fw(blockchain_admin.get_account(0))
print("Pulled - Fw description: {}".format(fw_descr[:10]))
print("Pulled - Fw IPFS link: {}".format(fw_ipfs))
user_node.download_firmware(fw_ipfs)