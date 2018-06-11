

class Firmware:

    def __init__(self,file = None):
        self.firmware_hash = None
        self.firmware_signature = self.sign_firmware()
        self.IPFS_link = None
        self.description = None
        self.device_type = None
    
    def sign_firmware(self):
        #TODO: Implement a function that signs the firmware hash
        pass

    def _generate_random(self):
        #TODO: Implement a function that generates a random firmware
        pass