from web3 import Web3, HTTPProvider,TestRPCProvider
from Contract import *

'''
Class @Blockchain_admin
============== Constructor ==============
    __init__(local, chainIP, Online_Acc_Addr, Online_Acc_Pwd)
        - local: Boolean if the blockchain is local using ganache
        - chain_ip: If not local, then provide IP of the blockchain node (including port)
        - Online_Acc_Addr: If not local, then provide the pk of the node interacting with bc
        - Online_Acc_Pwd: if not local, then provide the pwd to unlock the node interacting with bc

============== Methods ==============
    @get_account(self,id) returns the Eth acc used in the constructor

    @getWeb3(self): returns an instance of web3

    @__unlock_account(self,duration) Private: Unlocks an Eth account for 10000ms
'''
class Blockchain_admin:

    def __init__(self,local, chain_ip = None, Online_Acc_Addr  = None, Online_Acc_Pwd = None):
        self.local = local
        if local:
            self.m_web3 = Web3(TestRPCProvider())
        else:
            if chain_ip == None or Online_Acc_Addr == None or Online_Acc_Addr == None:
                raise ValueError("One of the variables passed to the constructor is None")
            self.m_web3 = Web3(HTTPProvider(chain_ip))
            self.Online_Acc_Addr  = Online_Acc_Addr
            self.Online_Acc_Pwd = Online_Acc_Pwd
            self.__unlock_account()
        self.m_web3.eth.defaultAccount = self.m_web3.eth.accounts[0]

    def get_all_accounts(self):
        if not self.local:
            raise ValueError("Cannot use this function for non local Web3")
        return self.m_web3.eth.accounts

    def get_account(self,id = 0):
        if self.local:
            return self.m_web3.eth.accounts[id]
        else:
            return self.Online_Acc_Addr

    def getWeb3(self):
        return self.m_web3

    def __unlock_account(self,duration=10000):
        self.m_web3.personal.unlockAccount(self.Online_Acc_Addr,self.Online_Acc_Pwd,duration)


