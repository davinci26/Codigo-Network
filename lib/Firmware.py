import sys
sys.path.append("lib/")
import traceback
import util as u

class Firmware:

    def __init__(self,firmware_id,firmware_stable = True, firmware_file = None, firmware_description = None):
       
        """ Initializes an instance of a firmware object
        
        Arguments:
            firmware_id {[string/int]} -- Target device: e.g. Rasberry pi
        
        Keyword Arguments:
            firmware_stable {Bool} -- Is this last version(False) or LTS(True) version (default: {True})
            firmware_file {Directory} -- Firmware directory,
                                         if none random string will be generated instead
                                         for debbuging purposes (default: {None})
        """
        self.device_type = str(firmware_id)
        self.stable = firmware_stable
        self.description = firmware_description
        if firmware_file:
            self.__init_from_file(firmware_file)
        else:
            self.__init_random()
        self.tx_cost = "Not determined"
        self.block = "Not on the blockchain"
    
    # To string for debbug printing
    def __str__(self):
        rep = "========== Firmware Object ===========\n"
        rep += "Firmware Directory:" + str(self.firmware_dir) + "\n"
        rep += "Code: " + self.firmware_str[:10] + "\n"
        rep += "Hash: " +  u.hash_to_utf8(self.firmware_hash) + "\n"
        rep += "IPFS Link: " + self.IPFS_link + "\n"
        rep += "Description: " + self.description[:10] + "\n"
        rep += "Target Device: " + self.device_type + "\n"
        rep += "LTS Version: " + str(self.stable) + "\n"
        rep += "Cumulative Gas Cost: " + str(self.tx_cost) + "\n"
        rep += "Included in Block: " + str(self.block) + "\n"
        rep += "=======================================\n"
        return rep
    

    def __init_from_file(self,firmware_file_):
        """ Load firmware from file and initialize the object
        Arguments:
            firmware_file_ {Directory} -- Firmware directory
            Throws EnvironmentError if the file is not found
        """
        try:
            with open(firmware_file_, 'r') as firmware_file:
                self.firmware_str = firmware_file.read()
            self.firmware_dir = firmware_file_
            self.__initialize(self.firmware_str)
        except EnvironmentError:
            traceback.print_exc()
            print("The file provided to CLASS FIRMWARE could not be read\nApplication will exit now.")

    def __init_random(self):
        """
        Initialize a firmware as a random string
        """
        self.firmware_str = u.generate_random_txt()
        self.__initialize(self.firmware_str)
        self.firmware_dir = "./logs/" +self.firmware_str[:5]
        self.save_local(self.firmware_dir)
        if not self.description:
            self.description = u.generate_random_txt()
        
    def __initialize(self,firmware_str):
        """
        Initialize firmware based on the binary file
        Arguments:
            firmware_str {String} -- Firmware binary file as string
        """
        self.firmware_hash = u.hash(firmware_str)
        self.IPFS_link = "TBD"
        if self.description == None:
            self.description = "No description was specified"

    def set_ipfs_link(self, link):
        self.IPFS_link = link

    def save_local(self, file_name):
        with open(file_name, "w") as text_file:
            print("{}".format(self.firmware_str), file=text_file)


