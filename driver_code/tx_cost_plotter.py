import matplotlib.pyplot as plt
from Contract import *
from bc_admin import *
import utility as u

Mode_SHOW = 0
experiment_size = 10

blockchain_admin = Blockchain_admin(local=True)
m_web3 = blockchain_admin.getWeb3()
primary_acc = blockchain_admin.get_account(0)

# Initialize and deploy contract
contract = Contract('contracts/webTrust.sol','web_of_trust',m_web3)
contract.publish_contract(m_web3, primary_acc)

def plt_endorse_trust(mode):
    trusted_addr = u.generate_eth_pk(experiment_size)
    tx_gas = []
    for pk in trusted_addr:
        tx_hash = contract.get_contract_instance().endorse_trust(pk, transact={'from': primary_acc})
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
        fig.savefig('endorse_trust.png', dpi=fig.dpi)
