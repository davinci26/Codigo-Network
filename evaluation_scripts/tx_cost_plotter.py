import sys
import numpy as np
from web3 import Web3
sys.path.append("lib/")
import matplotlib.pyplot as plt
from Contract import *
from Compact_Contract import *
from bc_admin import *
from ipfs_admin import *
from Developer import *
from User import *
import util as u

save_dir = './evaluation_scripts/Plots/'

Mode_SHOW = 0
Mode_SAVE = 1
experiment_size = 50

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
primary_acc = blockchain_admin.get_account(0)
ipfs_admin = IPFS_Admin(local = True)

# Initialize and deploy contract
contract = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3)
contract.publish(primary_acc)

def plt_endorse_trust(mode):
    trusted_addr = u.generate_eth_pk(experiment_size)
    tx_gas = []
    for pk in trusted_addr:
        tx_hash = contract.get_consice_instance().endorse_trust(pk, transact={'from': primary_acc})
        txn_receipt = m_web3.eth.getTransactionReceipt(tx_hash)
        tx_gas.append(txn_receipt['cumulativeGasUsed'])
    fig = plt.figure()   
    plt.plot(tx_gas)
    plt.title('Gas cost for allocating trust to a user')
    plt.xlabel('Number of Trusted addresses')
    plt.ylabel('Cumulative Gas Cost')
    if mode == Mode_SHOW:
        plt.show()
    else:
        fig.savefig(save_dir + 'endorse_trust.png', dpi=fig.dpi)

def plt_revoke_trust(mode):
    trusted_addr = u.generate_eth_pk(experiment_size)
    for pk in trusted_addr:
        tx_hash = contract.get_consice_instance().endorse_trust(pk, transact={'from': primary_acc})
        txn_receipt = m_web3.eth.getTransactionReceipt(tx_hash)

    tx_gas = []
    x_axis = []
    ii = 0
    for pk in reversed(trusted_addr):
        tx_hash = contract.get_consice_instance().revoke_trust(pk, transact={'from': primary_acc})
        txn_receipt = m_web3.eth.getTransactionReceipt(tx_hash)
        tx_gas.append(txn_receipt['cumulativeGasUsed'])
        x_axis.append(experiment_size - ii)
        ii += 1
    
    fig = plt.figure()   
    plt.scatter(x_axis,tx_gas)
    plt.title('Gas cost to revoke trust to a user')
    plt.xlabel('Number of Trusted addresses')
    plt.ylabel('Cumulative Gas Cost')
    if mode == Mode_SHOW:
        plt.show()
    else:
        fig.savefig(save_dir + 'revoke_trust.png', dpi=fig.dpi)



def plt_hops_vs_gas(mode):
    # Initialize and deploy contract
    contract = Contract('contracts/webTrust.sol','Web_Of_Trust',m_web3,verbose=False)
    contract.publish(blockchain_admin.get_account(0))
    # Add addresses
    tx_hash =contract.get_consice_instance().endorse_trust(blockchain_admin.get_account(1), transact={'from': blockchain_admin.get_account(0)})
    # Wait for transaction to be mined...
    m_web3.eth.waitForTransactionReceipt(tx_hash)
    # Calculate Trust
    tt = contract.get_consice_instance().hop_to_target(blockchain_admin.get_account(1),
                                                       blockchain_admin.get_account(0))
    print(tt) 

def add_firmware_cost(mode):
    cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
    cc.publish(blockchain_admin.get_account(0))
    # Create Developer node with PK(1)
    developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(0), "Test", ipfs_admin)
    # Push Firmware
    tx_gas = []
    for i in range(0,experiment_size):
        receipt = developer_node.add_firmware(firmware_stable = True, firmware_file= None, firmware_description = None)
        tx_gas.append(receipt['cumulativeGasUsed'])
    print("Pushed - Fw description: {}".format(developer_node.fw.description[:10]))
    fig = plt.figure()   
    plt.plot(tx_gas)
    plt.title('Gas cost for adding a new firmware')
    plt.xlabel('Number of Firmware')
    plt.ylabel('Cumulative Gas Cost')
    if mode == Mode_SHOW:
        plt.show()
    else:
        fig.savefig(save_dir + 'add_firmware.png', dpi=fig.dpi)


def add_firmware_variable_description(mode):
    cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
    cc.publish(blockchain_admin.get_account(0))
    # Create Developer node with PK(1)
    developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(0), "Test", ipfs_admin)
    # Push Firmware
    tx_gas = []
    length = []
    for i in range(0,experiment_size):
        receipt = developer_node.add_firmware(firmware_stable = True, firmware_file= None,
                                              firmware_description = u.generate_random_txt(i*100))
        tx_gas.append(receipt['cumulativeGasUsed'])
        length.append(i*100)
    print("Pushed Firmware {}/{}".format(i,experiment_size))
    fig = plt.figure()   
    plt.scatter(length,tx_gas)
    plt.title('Gas cost for adding a new firmware with variable description length')
    plt.xlabel('Description Length')
    plt.ylabel('Cumulative Gas Cost')
    if mode == Mode_SHOW:
        plt.show()
    else:
        fig.savefig(save_dir + 'add_firmware.png', dpi=fig.dpi)


#plt_revoke_trust(Mode_SAVE)
print("Web of Trust Deployment Gas Cost: {}".format(contract.deployment_cost))