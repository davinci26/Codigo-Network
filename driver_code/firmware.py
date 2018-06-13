import traceback
import utility as u
'''
Class @Firmware
============== Constructor ==============
    __init__(firmware_id,firmware_file)
        - firmware_id: Integer used to specify the target device
        - firmware_file: Directory of the firmware.
          If not specified a random string will be generated instead for debbuging purposes
============== Methods (Private) ==============
    @ __load_fw_from_file() Loads a firmware based on file
    @ __initialize_fw_random() Creates a firmware based on a random string
    @ __initialize(self,firmware_str): Creates a full Firmware Class instance
'''

class Firmware:

    def __init__(self,firmware_id,firmware_file = None):
        self.device_type = "d" + str(firmware_id)
        if firmware_file:
            self.__load_fw_from_file(firmware_file)
        else:
            self.__initialize_fw_random()
    
    def __str__(self):
        rep = "========== Firmware Object ===========\n"
        rep += "Code: " + self.firmware_str[:10] + "\n"
        rep += "Hash: " +  self.firmware_hash + "\n"
        rep += "Signature: " + self.firmware_signature + "\n"
        rep += "IPFS Link: " + self.IPFS_link + "\n"
        rep += "Description: " + self.description[:10] + "\n"
        rep += "Target Device: " + self.device_type + "\n"
        rep += "=======================================\n"
        return rep

    def __load_fw_from_file(self,firmware_file_):
        try:
            with open(firmware_file_, 'r') as firmware_file:
                self.firmware_str = firmware_file.read()
            self.__initialize(self.firmware_str)
        except EnvironmentError:
            traceback.print_exc()
            print("The file provided to CLASS FIRMWARE could not be read\nApplication will exit now.")
            exit(1)

    def __initialize_fw_random(self):
        self.firmware_str = u.__generate_random_txt()
        self.__initialize(self.firmware_str)

    def __initialize(self,firmware_str):
        #TODO: Correct IPFS link
        self.firmware_hash = u.__hash_utf8(firmware_str)
        self.firmware_signature = u.sign_firmware(self.firmware_hash)
        self.IPFS_link = "Not Implemented"
        self.description = u.__generate_random_txt()