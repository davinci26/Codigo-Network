import sys
sys.path.append("lib/")
from bc_admin import *
from ipfs_admin import *
from Developer import *
from dev_variables import *
import argparse

dev_variables = Dev_Variables()
parser = argparse.ArgumentParser(description='Command Line Interface')
parser.add_argument('--cli', action='store_true', default = False,
                    help='Use CLI instead of GUI')
parser.add_argument('--PK_index', type=int, nargs='?',default=0,
                    help='Web3 public key index')
parser.add_argument('--Device_Type', type=str, nargs='?',default="Raspberry pi",
                    help='The device that the firmware targets')
parser.add_argument('--Firmware', type=str, nargs='?',default = None,
                    help='Path to the firmware you wish to upload')
parser.add_argument('--FW_Stable', action='store_true', default = True,
                    help='Stable or LTS version of the firmware')
parser.add_argument('--description', type=str, nargs='?',default = None,
                    help='Firmware Description')
parser.add_argument('--Contract_Address', type=str, nargs='?',default=None,
                    help='Firmware Repository Address')
parser.add_argument('--Local_IPFS', action='store_true', default = False,
                    help='Use local IPFS deamon, or use Infura')
parser.add_argument('--Local_BC', action='store_true', default = True,
                    help='Use local blockchain')
blockchain_admin = None
m_web3 = None
ipfs_admin = None

def upload(dev_vars):
    # Initialize communication with blockchain
    global blockchain_admin
    global m_web3
    global ipfs_admin
    if blockchain_admin == None:
        blockchain_admin = Blockchain_admin(local= dev_vars.Local_BC)
    if m_web3 == None:
        m_web3 = blockchain_admin.getWeb3()
    # Initialize communication with IPFS
    if ipfs_admin == None:
        ipfs_admin = IPFS_Admin(local = dev_vars.Local_IPFS)
    # Deploy Contract
    if dev_vars.Contract_Address == None:
        from Contract import Contract
        cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, address_=dev_vars.Contract_Address,  verbose=False)
        try:
            firmware_repo_address = cc.publish(blockchain_admin.get_account(dev_vars.PK_index))
        except:
            firmware_repo_address = cc.address
    else:
        from Compact_Contract import Compact_Contract
        cc = Compact_Contract('working_dir/fw_repo_abi','FirmwareRepo',
                              m_web3, address_=user_variables.Contract_Address,
                              verbose=False)
        firmware_repo_address = cc.address
    # Get web of trust address
    web_of_trust_addr = cc.get_def_instance().functions.trust_address().call()
    # Create Developer node with PK
    developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(dev_vars.PK_index), dev_vars.device_t, ipfs_admin)
    # Push Firmware
    developer_node.add_firmware(firmware_stable = dev_vars.FW_Stable, firmware_file= dev_vars.fw_path, firmware_description = dev_vars.FW_description)
    print("Pushed - Fw description: {}".format(developer_node.fw.description[:10]))
    return developer_node.fw, firmware_repo_address,web_of_trust_addr

def main_qt():
    from PyQt5.QtWidgets import (QApplication, QWidget,QLabel,QCheckBox, QFormLayout,
    QLineEdit, QComboBox,QGroupBox, QGridLayout,QTextEdit,QPushButton, QFileDialog, QSpinBox)
    from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
    from PyQt5.QtGui import QPixmap

    @pyqtSlot(int)
    def enable_selection(v):
        locate_fw_wdgt.setEnabled(v)
        fw_description_wdgt.setEnabled(v)

    @pyqtSlot(int)
    def set_developer_pk(dev_pl):
        dev_variables.PK_index = dev_pl

    @pyqtSlot(str)
    def set_contract_address(add):
        dev_variables.Contract_Address = add

    @pyqtSlot(str)
    def set_ipfs_type(ipfs_type):
        dev_variables.Local_IPFS = True
        if ipfs_type == "Infura":
            dev_variables.Local_IPFS = False
        
    @pyqtSlot(str)
    def set_bc_type(Bc_type):
        #TODO: Implement on non local bc
        dev_variables.Local_BC = True

    @pyqtSlot(str)
    def set_target_device(dev_type):
        dev_variables.device_t = dev_type

    @pyqtSlot()
    def set_description():
        dev_variables.FW_description = fw_description_wdgt.toPlainText()
    
    @pyqtSlot()
    def locate_fw():
        dev_variables.fw_path = QFileDialog.getOpenFileName(caption = "Locate Firmware")[0]
        Info.setText("Firmware loaded: " + dev_variables.fw_path)

    @pyqtSlot(int)
    def set_stable(stable):
        dev_variables.FW_Stable = bool(stable)

    @pyqtSlot()
    def upload_fw():
        uploaded_fw = upload(dev_variables)
        print(uploaded_fw[0])
        if uploaded_fw:
            Info.setText("Developer: {}\n".format(blockchain_admin.get_account(dev_variables.PK_index))+
                         "Web of Trust address: {}\n".format(uploaded_fw[2]) +
                         "Firmware Repository address: {} \n".format(uploaded_fw[1]) + 
                         "Pushed the following firmware to IPFS and Ethereum \n" + str(uploaded_fw[0]))

    app = QApplication(sys.argv)
    
    mainWdgt = QWidget()
    mainWdgt.setWindowTitle('Codigo Network Developer Client')
    
    network_wdgt = QGroupBox("Developer/Network Information")
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

    firmware_wdgt = QGroupBox("Firmware Information")
    firmware_wdgt_lay = QGridLayout(firmware_wdgt)
    # Target device
    dev_type_wdgt = QLineEdit()
    dev_type_wdgt.setText("Raspberry pi")
    dev_type_wdgt.textChanged.connect(set_target_device)
    firmware_wdgt_lay.addWidget(QLabel("Target Device"),0,0)
    firmware_wdgt_lay.addWidget(dev_type_wdgt,0,1)

    stable_fw_wdgt = QCheckBox()
    stable_fw_wdgt.setChecked(True)
    stable_fw_wdgt.stateChanged.connect(set_stable)
    firmware_wdgt_lay.addWidget(QLabel("Stable Version"),1,0)
    firmware_wdgt_lay.addWidget(stable_fw_wdgt,1,1)

    random_fw_wdgt = QCheckBox()
    random_fw_wdgt.stateChanged.connect(enable_selection)
    random_fw_wdgt.setToolTip("If not selected a random file will be uploaded")
    firmware_wdgt_lay.addWidget(QLabel("Upload file"),2,0)
    firmware_wdgt_lay.addWidget(random_fw_wdgt,2,1)
    locate_fw_wdgt = QPushButton("Locate Firmware")
    locate_fw_wdgt.setEnabled(False)
    locate_fw_wdgt.clicked.connect(locate_fw)
    firmware_wdgt_lay.addWidget(locate_fw_wdgt,3,0,1,-1)
    fw_description_wdgt = QTextEdit()
    fw_description_wdgt.setEnabled(False)
    fw_description_wdgt.textChanged.connect(set_description)
    firmware_wdgt_lay.addWidget(QLabel("Firmware Description:"),4,0)
    firmware_wdgt_lay.addWidget(fw_description_wdgt,5,0,1,-1)

    mainLayout = QGridLayout(mainWdgt)
    mainLayout.addWidget(network_wdgt,0,0)
    mainLayout.addWidget(firmware_wdgt,0,1)
    main_btn = QPushButton("Upload to network")
    main_btn.clicked.connect(upload_fw)
    mainLayout.addWidget(main_btn,1,0,1,-1)
    Info = QTextEdit("Uploaded Firmware: ....")
    mainLayout.addWidget(Info,2,0,1,-1)
    mainWdgt.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    args = parser.parse_args()
    if args.cli:
        dev_variables.PK_index = int(args.PK_index)
        dev_variables.Contract_Address = args.Contract_Address
        dev_variables.Local_IPFS = args.Local_IPFS
        dev_variables.Local_BC = args.Local_BC
        dev_variables.device_t = args.Device_Type
        dev_variables.fw_path = args.Firmware
        dev_variables.FW_Stable = args.FW_Stable
        dev_variables.FW_description = args.description
        fw = upload(dev_variables)
        print("Web of Trust address: {}".format(fw[2]))
        print("Firmware Repository address: {}".format(fw[1]))
        print("Uploaded to IPFS & Eth the following firmware:\n" + str(fw[0]))
    else:
        main_qt()