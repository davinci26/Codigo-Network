#!/usr/bin/env python3
import sys
import numpy as np
from web3 import Web3
sys.path.append("lib/")
import matplotlib 
import matplotlib.pyplot as plt
from Contract import *
from Compact_Contract import *
from bc_admin import *
from ipfs_admin import *
from Developer import *
from User import *
import util as u
import argparse

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

def eth_plotter_format(mode,tx_gas,x_ticks,x_label,filename):
    GAS_TO_ETH = 6/1000000000.
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x_ticks, tx_gas,'o')
    ax2.plot(x_ticks, np.array(tx_gas)*GAS_TO_ETH,'g-',alpha=0)
    ax1.set_xlabel(x_label)
    ax2.set_ylabel('Tx Cost[Eth]')
    ax1.set_ylabel('Cumulative Gas Cost')
    if mode == Mode_SHOW:
        plt.show()
    else:
        fig.savefig(save_dir + filename +'.png',bbox_inches='tight')


def pow_plotter(mode, difficulty,attempts,diff_err,attempts_error,exp_size):
    fig = plt.figure(1)
    plt.subplot(211)
    #plt.locator_params(nbins=12)
    x = np.arange(1,exp_size+1)
    plt.errorbar(x,attempts,yerr=attempts_error,fmt='o')
    plt.xticks(np.arange(1, 4, step=1))
    plt.xlabel('Firmware Added')
    plt.ylabel('Sha3 Computations')
    plt.subplot(212)
    plt.scatter(x,difficulty)
    plt.xticks(np.arange(1, 4, step=1))
    plt.xlabel('Firmware Added')
    plt.ylabel('PoW Target')
    if mode == Mode_SHOW:
        plt.show()
    else:
        fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        fig.savefig(save_dir + 'pow_cost' +'.png',bbox_inches='tight')


def plt_endorse_trust(mode):
    trusted_addr = u.generate_eth_pk(experiment_size)
    tx_gas = []
    ii = 0
    for pk in trusted_addr:
        if ii % 5 == 0 or ii==1: 
            tx_hash = contract.get_consice_instance().endorse_trust(pk, transact={'from': primary_acc})
            txn_receipt = m_web3.eth.getTransactionReceipt(tx_hash)
            tx_gas.append(txn_receipt['cumulativeGasUsed'])
        ii +=1
    x_ticks = np.arange(1,experiment_size+1,5)
    x_ticks = np.insert(x_ticks,1,2)
    eth_plotter_format(mode,tx_gas,x_ticks, x_label='Number of trusted addresses',filename='endorse_trust')


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
    eth_plotter_format(mode,tx_gas,x_axis, x_label='Number of trusted addresses',filename='revoke_trust')


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


def plt_pow_cost(mode):
    exp_size = 20
    attempts_per_exp = 3
    difficulty = np.zeros((exp_size,attempts_per_exp))
    attempts = np.zeros((exp_size,attempts_per_exp))
    for ii in range(0,exp_size+1):
        cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
        cc.publish(blockchain_admin.get_account(0))
        print("========= Experiment {}/{} =========".format(ii,exp_size))
        for i in range(0,attempts_per_exp+1):
            current_gas = 0
            pow_found = False
            nonce = 1
            while (not pow_found):
                try:
                    tx_hash = cc.get_def_instance().functions.proofOfWork(nonce).transact()
                    pow_found = True
                except:
                    pow_found = False
                    nonce += 1
            difficulty[ii][i] = cc.get_def_instance().functions.get_d().call()
            attempts[ii][i] = nonce
            print("Current dif {}, attempts {} iteration {}".format(cc.get_def_instance().functions.get_d().call(),nonce,i))
        
    pow_plotter(mode, np.mean(difficulty,axis=0),
                      np.mean(attempts,axis=0),
                      np.std(difficulty,axis=0),
                      np.std(attempts,axis=0),
                      attempts_per_exp)
        
def plt_add_firmware_cost(mode):
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
    x_ticks = np.arange(1,experiment_size+1)
    eth_plotter_format(mode,tx_gas,x_ticks, x_label='Number of Firmware',filename='add_firmware')


def plt_add_firmware_variable_description(mode):
    cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, verbose=False)
    cc.publish(blockchain_admin.get_account(0))
    # Create Developer node with PK(1)
    developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(0), "Test", ipfs_admin)
    # Push Firmware
    tx_gas = []
    length = []
    for i in range(1,experiment_size+1):
        receipt = developer_node.add_firmware(firmware_stable = True, firmware_file= None,
                                              firmware_description = u.generate_random_txt(i*100))
        tx_gas.append(receipt['cumulativeGasUsed'])
        length.append(i*100)
        print("Pushed Firmware {}/{}".format(i,experiment_size))
    eth_plotter_format(mode,tx_gas,length, x_label='Firmware Description Length',filename='firmware_descr')


# pow_cost(Mode_SHOW)
#print("Web of Trust Deployment Gas Cost: {}".format(contract.deployment_cost))
#pow_cost(Mode_SAVE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Line Interface')
    parser.add_argument('--function', type=str, nargs='?',
                        help="Specify the plot you want: 1. Endorse Trust\n"+
                             "2. Revoke Trust\n"+
                             "3. Add Firmware\n"+
                             "4. Add Firmware Description\n"+
                             "5. all")
    parser.add_argument('-s', action='store_true', default = False,
                    help='Use this to save the plots')
    args = parser.parse_args()

    mode = Mode_SHOW
    if args.s:
        mode = Mode_SAVE

    if args.function.lower() == "Endorse_Trust".lower():
        plt_endorse_trust(mode)
    elif args.function.lower() == "Revoke_Trust".lower():
        plt_revoke_trust(mode)
    elif args.function.lower() == "Add_Firmware".lower():
        plt_add_firmware_cost(mode)
    elif args.function.lower() == "Add_Firmware_Description".lower():
        plt_add_firmware_variable_description(mode)
    elif args.function.lower() == "POW".lower():
        plt_pow_cost(mode)
    elif args.function.lower() == "all".lower():
        plt_endorse_trust(mode)
        plt_revoke_trust(mode)
        plt_add_firmware_cost(mode)
        #plt_add_firmware_variable_description(mode)
    else:
        print("Wrong commanding line arguments provide --function should have one the following values:\n"+
             "1. Endorse Trust\n"+
             "2. Revoke Trust\n"+
             "3. Add Firmware\n"+
             "4. Add Firmware Description\n"+
             "5. all")