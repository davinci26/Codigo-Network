import sys
from web3 import Web3
sys.path.append("lib/")
from bc_admin import *
from ipfs_admin import *
from Compact_Contract import *
from User import *
from user_variables import *
import argparse

user_variables = User_Variables()
parser = argparse.ArgumentParser(description='Command Line Interface')
parser.add_argument('--cli', action='store_true', default = False,
                    help='Use CLI instead of GUI')

user_node = None
m_web3 = None
blockchain_admin = None
cc = None
web_of_trust = None
fw_ipfs = None

def init_user():
    global user_node
    global m_web3
    global blockchain_admin
    global cc
    global web_of_trust
    blockchain_admin = Blockchain_admin(local= user_variables.Local_BC)
    m_web3 = blockchain_admin.getWeb3()
    # Initialize communication with IPFS
    ipfs_admin = IPFS_Admin(local = user_variables.Local_IPFS)
    # Get Contract
    cc = Compact_Contract('working_dir/fw_repo_abi','FirmwareRepo',
                          m_web3, address_=user_variables.Contract_Address,
                          verbose=False)
    # Get web of trust address
    web_of_trust_addr = cc.get_def_instance().functions.trust_address().call()
    # Initialize web of trust contract
    web_of_trust = Compact_Contract('working_dir/web_trust_abi','Web_Of_Trust',
                                    m_web3, address_ = web_of_trust_addr,
                                    verbose=False)
    # Create User node with PK(0)
    user_node = User_Node(m_web3, cc, blockchain_admin.get_account(user_variables.PK_index), user_variables.device_t, ipfs_admin)


def main_qt():
    from PyQt5.QtWidgets import (QApplication, QWidget,QLabel,QCheckBox, QFormLayout,
    QLineEdit, QComboBox,QGroupBox, QGridLayout,QTextEdit,QPushButton, QFileDialog, QSpinBox)
    from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

    @pyqtSlot(int)
    def set_developer_pk(dev_pl):
        user_variables.PK_index = dev_pl

    @pyqtSlot(str)
    def set_contract_address(add):
        user_variables.Contract_Address = add

    @pyqtSlot(str)
    def set_ipfs_type(ipfs_type):
        user_variables.Local_IPFS = True
        if ipfs_type == "Infura":
            user_variables.Local_IPFS = False
        
    @pyqtSlot(str)
    def set_bc_type(Bc_type):
        #TODO: Implement on non local bc
        user_variables.Local_BC = True
    
    @pyqtSlot(str)
    def set_target_device(dev_type):
        user_variables.device_t = dev_type

    @pyqtSlot(int)
    def set_stable(stable):
        user_variables.FW_Stable = bool(stable)

    @pyqtSlot()
    def endorse_dev():
        # if not Web3.isAddress(user_variables.Contract_Address):
        #     Info.setText("{} is not a valid Ethereum Contract address".format(user_variables.Contract_Address))
        #     return
        if not Web3.isAddress(trust_dev_wdgt.text()):
            Info.setText("{} is not a valid Ethereum User address".format(trust_dev_wdgt.text()))
            return
        if user_node == None:
            init_user()
        val = user_node.endorse_developer(web_of_trust, Web3.toChecksumAddress(trust_dev_wdgt.text()))
        Info.setText("Transaction receipt:\n" + str(val))

    @pyqtSlot()
    def get_specific():
        if not Web3.isAddress(user_variables.Contract_Address):
            Info.setText("{} is not a valid Ethereum Contract address".format(user_variables.Contract_Address))
            return
        if not Web3.isAddress(specific_dev_wdgt.text()):
            Info.setText("{} is not a valid Ethereum User address".format(specific_dev_wdgt.text()))
            return
        if user_node == None:
            init_user()
        global fw_ipfs
        fw_hash,fw_ipfs,fw_descr,fw_block = user_node.get_specific_fw(Web3.toChecksumAddress(specific_dev_wdgt.text()))
        Info.setText("Firmware Specific:\n Description: {} \n IPFS Link: {}".format(fw_descr[:10],fw_ipfs))
        download_btn.setEnabled(True)

    @pyqtSlot()
    def get_most_trusted():
        if not Web3.isAddress(user_variables.Contract_Address):
            Info.setText("{} is not a valid Ethereum Contract address".format(user_variables.Contract_Address))
            return
        if user_node == None:
            init_user()
        global fw_ipfs
        fw_hash,fw_ipfs,fw_descr,fw_block,fw_dev,trust = user_node.get_most_trusted_fw()
        Info.setText("Firmware Preview:\n Description: {} \n IPFS Link: {} \n Trust: {}".format(fw_descr[:10],fw_ipfs,trust))
        download_btn.setEnabled(True)
    
    @pyqtSlot()
    def get_multiple():
        if not Web3.isAddress(user_variables.Contract_Address):
            Info.setText("{} is not a valid Ethereum Contract address".format(user_variables.Contract_Address))
            return
        fw_list = user_node.get_mult_trusted_fw_local(web_of_trust)
        text = "Firmware to preview"
        global fw_ipfs
        for fw in fw_list:
            #unpack fw
            fw_hash,fw_ipfs,fw_descr,fw_block,fw_dev,trust = fw
            text += "Firmware:\n Description: {} \n IPFS Link: {} \n Trust: {} \n".format(fw_descr[:10],fw_ipfs,trust)
            text += "============================================================\n"
        Info.setText(text)

    @pyqtSlot()
    def download_fw():
        print(fw_ipfs)
        user_node.download_firmware(fw_ipfs)
        Info.setText("Fw {} is downloaded successfully".format(fw_ipfs))

    app = QApplication(sys.argv)
    mainWdgt = QWidget()
    mainWdgt.setWindowTitle('Codigo Network User Client')
    
    network_wdgt = QGroupBox("User/Network Information")
    # Form Layout
    formLay = QFormLayout(network_wdgt)
    # Developer PK QLineEdit
    pk_line_edit = QSpinBox()
    pk_line_edit.valueChanged.connect(set_developer_pk)
    formLay.addRow("Developer PK index:",pk_line_edit)
    # Device Type
    fw_repo_wdgt = QLineEdit()
    fw_repo_wdgt.textChanged.connect(set_contract_address)
    formLay.addRow("Firmware Repository Address:",fw_repo_wdgt)

    # Blockchain Host IP
    bc_host_wdgt = QComboBox()
    bc_host_wdgt.addItem("Local")
    formLay.addRow("Ethereum Node:",bc_host_wdgt)
    # IPFS Host IP
    ipfs_node_wdgt = QComboBox()
    ipfs_node_wdgt.addItem("Local")
    ipfs_node_wdgt.addItem("Infura")
    ipfs_node_wdgt.currentIndexChanged.connect(set_ipfs_type)
    formLay.addRow("IPFS Host:",ipfs_node_wdgt)
    # Target Device
    dev_type_wdgt = QLineEdit()
    dev_type_wdgt.setText("Raspberry pi")
    dev_type_wdgt.textChanged.connect(set_target_device)
    formLay.addRow("Target Device:",dev_type_wdgt)
    # Stable
    stable_fw_wdgt = QCheckBox()
    stable_fw_wdgt.setChecked(True)
    stable_fw_wdgt.stateChanged.connect(set_stable)
    formLay.addRow("Stable Version:",stable_fw_wdgt)

    operation_wdgt = QGroupBox("Operation")
    operation_wdgt_lay = QGridLayout(operation_wdgt)

    trust_dev_wdgt = QLineEdit()
    trust_dev = QPushButton("Trust")
    trust_dev.clicked.connect(endorse_dev)
    operation_wdgt_lay.addWidget(QLabel("Trust Developer with PK"),0,0)
    operation_wdgt_lay.addWidget(trust_dev_wdgt,0,1)
    operation_wdgt_lay.addWidget(trust_dev,0,2)

    specific_dev_wdgt = QLineEdit()
    prv_specific = QPushButton("Preview")
    prv_specific.clicked.connect(get_specific)
    operation_wdgt_lay.addWidget(QLabel("Preview Firmware from PK"),1,0)
    operation_wdgt_lay.addWidget(specific_dev_wdgt,1,1)
    operation_wdgt_lay.addWidget(prv_specific,1,2)

    prv_most = QPushButton("Preview")
    prv_most.clicked.connect(get_most_trusted)
    operation_wdgt_lay.addWidget(QLabel("Preview most trusted firmware"),2,0,1,2)
    operation_wdgt_lay.addWidget(prv_most,2,2)
    
    prv_mult = QPushButton("Preview multiple")
    operation_wdgt_lay.addWidget(QLabel("Preview multiple trusted firmware"),3,0,1,2)
    operation_wdgt_lay.addWidget(prv_mult,3,2)

    mainLayout = QGridLayout(mainWdgt)
    mainLayout.addWidget(network_wdgt,0,0)
    mainLayout.addWidget(operation_wdgt,0,1)
    Info = QTextEdit("Log ....")
    #Info.setEnabled(False)
    mainLayout.addWidget(Info,1,0,1,-1)
    download_btn = QPushButton("Download Firmware")
    download_btn.setEnabled(False)
    download_btn.clicked.connect(download_fw)
    mainLayout.addWidget(download_btn,2,0,1,-1)
    mainWdgt.show()

    network_wdgt.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    args = parser.parse_args()
    if args.cli:
        pass
        # dev_variables.PK_index = int(args.PK_index)
        # dev_variables.Contract_Address = args.Contract_Address
        # dev_variables.Local_IPFS = args.Local_IPFS
        # dev_variables.Local_BC = args.Local_BC
        # dev_variables.device_t = args.Device_Type
        # dev_variables.fw_path = args.Firmware
        # dev_variables.FW_Stable = args.FW_Stable
        # dev_variables.FW_description = args.description
        # fw = upload(dev_variables)
        # print("Deployed contract to address: {}".format(fw[1]))
        # print("Uploaded to IPFS & Eth the following firmware:\n" + str(fw[0]))
    else:
        main_qt()