# import sys
# sys.path.append("lib/")
# from bc_admin import *
# from ipfs_admin import *
# from Contract import *
# from Developer import *
# import argparse

# def main():
#     # Handle Command Line arguments 
#     parser = argparse.ArgumentParser(description='Command Line Interface')
#     parser.add_argument('--PK_index', type=int, nargs='?',
#                         help='Web3 public key index')
#     parser.add_argument('--Device_Type', type=str, nargs='?',default="Raspberry pi",
#                         help='The device that the firmware targets')
#     parser.add_argument('--Firmware', type=str, nargs='?',default = None,
#                         help='Path to the firmware you wish to upload')
#     parser.add_argument('--FW_Stable', action='store_true', default = True,
#                         help='Stable or LTS version of the firmware')
#     parser.add_argument('--Contract_Address', type=str, nargs='?',default=None,
#                         help='Firmware Repository Address')
#     parser.add_argument('--Local_IPFS', action='store_true', default = False,
#                         help='Use local IPFS deamon, or use Infura')
#     parser.add_argument('--Local_BC', action='store_true', default = True,
#                         help='Use local blockchain')
#     args = parser.parse_args()
    
    
    
#     # Initialize communication with blockchain
#     blockchain_admin = Blockchain_admin(local=args.Local_BC)
#     m_web3 = blockchain_admin.getWeb3()
#     # Initialize communication with IPFS
#     ipfs_admin = IPFS_Admin(local = args.Local_IPFS)    
#     device_t = args.Device_Type
#     # Create user node
#     user_node = User_Node(m_web3, cc, blockchain_admin.get_account(args.PK_index), device_t,ipfs_admin)

# if __name__ == '__main__':
#     main()
