pragma solidity ^0.4.23;
pragma experimental ABIEncoderV2;

import "./webTrust.sol";

contract FirmwareRepo{
    Web_Of_Trust web_trust;

    struct Firmware {
        // address developer;
        bytes32 firmware_hash;
        string IPFS_link;
        string description;
        uint256 block_number;
        // string device_type;
    }

    struct Firmware_Info {
        Firmware fw;
        address developer;
        int256 trust;
    }
 
    mapping(string => mapping(address=>uint256)) device_developer_index;
    
    mapping(string => address[]) device_developers;
    
    // Each developer is allowed to have a stable version and a experimental version. Critical Assumption
    mapping(string => mapping(address => Firmware[2])) developed_firmware;


    // Modifiers
    // There exists firmware for the target device
    modifier hasFirmware(string device_type) {
        require(device_developers[device_type].length != 0);
        _; 
    }
    // The requested developer exists
    modifier isValidDeveloper(string device_type, address developer) {
        require(device_developer_index[device_type][developer]!=0 || device_developers[device_type].length == 1);
        _; 
    }

    /** Interface Target for Developers *
    - add_firmware
    - edit_discription
    ************************************/
    function add_firmware(bytes32 firmware_hash_, string IPFS_link_, string description_, string device_type_, bool stable) public {
        require(firmware_hash_ != 0);
        require(!is_empty(IPFS_link_));
        require(!is_empty(description_));
        require(!is_empty(device_type_));
        uint8 firmware_index = (stable) ? 0 : 1; 
        uint256 dev_index = device_developer_index[device_type_][msg.sender];
        // TODO: Whatif its actually 0 => its the manufacturer that wants to add a firmware
        if (dev_index == 0 && device_developers[device_type_].length != 0) {
            uint256 prv_length = device_developers[device_type_].length;
            device_developers[device_type_].length++;
            device_developers[device_type_][prv_length] = msg.sender;
            device_developer_index[device_type_][msg.sender] = prv_length;
        }
        developed_firmware[device_type_][msg.sender][firmware_index] = 
            Firmware(firmware_hash_,IPFS_link_,description_,block.number);  
    }

    function edit_description(string description_, string device_type, bool stable) public {
        //TODO: Add proper require()
        uint8 firmware_index = (stable) ? 0 : 1;
        developed_firmware[device_type][msg.sender][firmware_index].description = description_;
    }

    /** Interface Target for Nodes *
    - get_manafucturer_firmware()
    - get top 10 firmware()
    - get top firmware()
    ************************************/


    function get_firmware(string device_type, address mf_address, bool stable)
             hasFirmware(device_type) isValidDeveloper(device_type,mf_address) public view returns (Firmware){
        uint8 firmware_index = (stable) ? 0 : 1;
        return developed_firmware[device_type][mf_address][firmware_index];
    }

    function get_most_trusted_firmware(string device_type, bool stable) hasFirmware(device_type)
             public view returns (Firmware_Info) {
        uint8 firmware_index = (stable) ? 0 : 1;
        address most_trusted_dev;
        int256  max_trust = -10;
        for (uint256 i = 0; i < device_developers[device_type].length; i++ ){
            int256 curr_trust = web_trust.hop_to_target(device_developers[device_type][i]);
            if (curr_trust > max_trust){
                max_trust = curr_trust;
                most_trusted_dev = device_developers[device_type][i];
            }
        }
        return Firmware_Info(developed_firmware[device_type][most_trusted_dev][firmware_index],most_trusted_dev,max_trust);
    }

    function get_top_firmwares(string device_type, bool stable) public returns (Firmware_Info[10]){
        Firmware_Info[10] firmware_list;
        return firmware_list;
    }


    function is_empty(string str) internal pure returns (bool) {
        // Source: https://ethereum.stackexchange.com/questions/11039/how-can-you-check-if-a-string-is-empty-in-solidity
        bytes memory tempEmptyStringTest = bytes(str); // Uses memory
        return (tempEmptyStringTest.length == 0);
    }


    //====== Debug Functions & State ======//
    uint8 contract_version = 1;
    function get_version() public view returns (uint8) {
        return contract_version;
    }
    //===================================//
}