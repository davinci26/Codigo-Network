import sys
sys.path.append("lib/")
from Firmware import *
import ipfsapi

#res = api.get('Qmbds4EKV5wEoXL9bXnxbFbTa9EzYmAkKcTTTYfKWq6PH6')
#print(res)

class IPFS_Admin:

    def __init__(self,local,verbose = False):
        if local:
            self.connect(verbose,local,'127.0.0.1')
        else:
            self.connect(verbose,local,'https://ipfs.infura.io',)

    def connect(self, verbose, local, ip, port = 5001):
        #TODO: Handle exceptions gracefully
        try:
            self.api = ipfsapi.connect(ip,port)
        except:
            print("Could not connect to IPFS Deamon :(")
        # except VersionMismatch:
        #     pass
        # except ErrorResponse:
        #     pass
        # except ConnectionError:
        #     pass
        # except StatusError:
        #     pass
        # except TimeoutError:
        #     pass
        # except:
        #     pass

    def upload_firmware(self,firmware):
        res = self.api.add(firmware.firmware_dir) #pin_add to pin the file as well
        return res

    def download_firmware(self,ipfs_link):
        res = self.api.get(ipfs_link)    
    