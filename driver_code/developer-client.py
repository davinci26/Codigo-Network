import sys
sys.path.append("lib/")
from bc_admin import *
from ipfs_admin import *
from Contract import *
from Developer import *
import argparse

# Default Values
PK_index = 1
Contract_Address = None
Local_IPFS = True
Local_BC = True
device_t = "Raspberry pi"
fw_path = None
FW_Stable = True
FW_description = "None"

def upload():
    # Initialize communication with blockchain
    blockchain_admin = Blockchain_admin(local=Local_BC)
    m_web3 = blockchain_admin.getWeb3()
    # Initialize communication with IPFS
    ipfs_admin = IPFS_Admin(local = Local_IPFS)
    # Deploy Contract
    cc = Contract('contracts/firmware_repo.sol','FirmwareRepo', m_web3, address_=Contract_Address,  verbose=False)
    cc.publish(blockchain_admin.get_account(0))
    # Create Developer node with PK(1)
    developer_node = Developer_Node(m_web3, cc, blockchain_admin.get_account(PK_index), device_t, ipfs_admin)
    # Push Firmware
    developer_node.add_firmware(firmware_stable = FW_Stable, firmware_file= fw_path)
    print("Pushed - Fw description: {}".format(developer_node.fw.description[:10]))
    return developer_node.fw

def main_cli():
    parser = argparse.ArgumentParser(description='Command Line Interface')
    parser.add_argument('--PK_index', type=int, nargs='?',
                        help='Web3 public key index')
    parser.add_argument('--Device_Type', type=str, nargs='?',default="Raspberry pi",
                        help='The device that the firmware targets')
    parser.add_argument('--Firmware', type=str, nargs='?',default = None,
                        help='Path to the firmware you wish to upload')
    parser.add_argument('--FW_Stable', action='store_true', default = True,
                        help='Stable or LTS version of the firmware')
    parser.add_argument('--Contract_Address', type=str, nargs='?',default=None,
                        help='Firmware Repository Address')
    parser.add_argument('--Local_IPFS', action='store_true', default = False,
                        help='Use local IPFS deamon, or use Infura')
    parser.add_argument('--Local_BC', action='store_true', default = True,
                        help='Use local blockchain')
    args = parser.parse_args()
    PK_index = args.PK_index
    Contract_Address = args.Contract_Address
    Local_IPFS = args.Local_IPFS
    Local_BC = args.Local_BC
    device_t = args.Device_Type
    fw_path = args.Firmware
    FW_Stable = args.FW_Stable
    FW_description = "None"
    upload()


def main_qt():
    from PyQt5.QtWidgets import (QApplication, QWidget,QLabel,QCheckBox, QFormLayout,
    QLineEdit, QComboBox,QGroupBox, QGridLayout,QTextEdit,QPushButton, QFileDialog, QSpinBox)
    from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

    @pyqtSlot(int)
    def enable_selection(v):
        locate_fw_wdgt.setEnabled(v)
        fw_description_wdgt.setEnabled(v)

    @pyqtSlot(int)
    def set_developer_pk(dev_pl):
        PK_index = dev_pl

    @pyqtSlot(str)
    def set_contract_address(add):
        Contract_Address = add

    @pyqtSlot(str)
    def set_ipfs_type(ipfs_type):
        Local_IPFS = True
        if ipfs_type == "Infura":
            Local_IPFS = False
        
    @pyqtSlot(str)
    def set_bc_type(Bc_type):
        #TODO: Implement on non local bc
        Local_BC = True

    @pyqtSlot(str)
    def set_target_device(dev_type):
        device_t = dev_type

    @pyqtSlot(str)
    def set_description(desc):
        FW_description = desc

    @pyqtSlot()
    def locate_fw():
        fw_path = QFileDialog().getOpenFileName(caption = "Locate Firmware")

    @pyqtSlot(int)
    def set_stable(stable):
        FW_Stable = bool(stable)

    @pyqtSlot()
    def upload_fw():
        uploaded_fw = upload()
        Info.setText("Pushed the following to IPFS and Ethereum \n" + uploaded_fw.__str__())

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
    # Contract Address
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
    firmware_wdgt_lay.addWidget(QLabel("Generate Dummy Firmware"),2,0)
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
    main_qt()
        
