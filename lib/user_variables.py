
# User operations
get_specific = 1
get_most_trusted = 2
get_multiple_trusted = 3
endorse_developer = 4

class User_Variables:
    def __init__(self):
        # Default Values
        self.PK_index = 1
        self.Contract_Address = None
        self.Local_IPFS = True
        self.Local_BC = True
        self.device_t = "Raspberry pi"
        self.FW_description = "None"
        self.operation = 0
        self.web_of_trust_addr = None