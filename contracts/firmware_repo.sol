pragma solidity ^0.4.23;
pragma experimental ABIEncoderV2;

import "./webTrust.sol";
import "./PQ.sol";

contract FirmwareRepo{

    // Firmware struct
    struct Firmware {
        // address developer;
        bytes32 firmware_hash;
        string IPFS_link;
        string description;
        uint256 block_number;
        // string device_type;
    }
    // Firmware Infor struct
    struct Firmware_Info {
        Firmware fw;
        address developer;
        int256 trust;
    }
    uint256 cv = 1;
    Web_Of_Trust web_trust;
    address web_trust_addr;

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
        require(developed_firmware[device_type][developer][0].firmware_hash[0] != 0 ||
            developed_firmware[device_type][developer][1].firmware_hash[0] != 0);
        _; 
    }

    constructor() public {
        web_trust_addr = new Web_Of_Trust();
        web_trust = Web_Of_Trust(web_trust_addr);
        cv = 2;
    }

    /* Generic Interface (Setters/Getters) *
    ************************************/
    // Get Web of Trust Contract Address
    function trust_address() public view returns (address) {
        return web_trust_addr;
    }

    /** Interface Target for Developers *
    ************************************/

    /**
        * @dev Called by developers to add a new firmware to the contract.
        * @param firmware_hash_ Hash of the firmware using SHA-3
        * @param IPFS_link_ IPFS link to download the firmware
        * @param description_  Firmware description
        * @param device_type_  Device Type (E.g. Raspberry pi)
        * @param stable       Firmware type: LTS or Latest Version
    */
    function add_firmware(bytes32 firmware_hash_, string IPFS_link_,
        string description_, string device_type_, bool stable) public {
        require(firmware_hash_ != 0);
        require(!is_empty(IPFS_link_));
        require(!is_empty(description_));
        require(!is_empty(device_type_));
        uint8 firmware_index = (stable) ? 0 : 1;

        // If I have no firmware from that dev, then add him to the list
        if (developed_firmware[device_type_][msg.sender][0].firmware_hash[0] == 0 &&
            developed_firmware[device_type_][msg.sender][1].firmware_hash[0] == 0 ){
            uint256 prv_length = device_developers[device_type_].length;
            device_developers[device_type_].length++;
            device_developers[device_type_][prv_length] = msg.sender;
            device_developer_index[device_type_][msg.sender] = prv_length;
        }
        developed_firmware[device_type_][msg.sender][firmware_index] = 
            Firmware(firmware_hash_,IPFS_link_,description_,block.number);  
    }

    /**
        * @dev Called by developers to edit the description of an existing firmware.
        * @param description_ New firmware description
        * @param device_type  Device Type (E.g. Raspberry pi)
        * @param stable       Firmware type: LTS or Latest Version
    */

    function edit_description(string description_, string device_type, bool stable) public {
        //TODO: Add proper require()
        uint8 firmware_index = (stable) ? 0 : 1;
        developed_firmware[device_type][msg.sender][firmware_index].description = description_;
    }

    // /** Interface Target for Nodes *
    // ************************************/

      /**
        * @dev Called by nodes to get a specific firmware.
        * @param device_type  Device Type (E.g. Raspberry pi)
        * @param mf_address   Firmware Developer PK
        * @param stable       Firmware type: LTS or Latest Version
    */
    function get_firmware(string device_type, address mf_address, bool stable)
              hasFirmware(device_type)
              isValidDeveloper(device_type,mf_address)
             public view returns (bytes32, string, string, uint256){
        uint8 firmware_index = (stable) ? 0 : 1;
        Firmware memory fw = developed_firmware[device_type][mf_address][firmware_index];
        return (fw.firmware_hash, fw.IPFS_link, fw.description, fw.block_number);
    }

    function get_developer(string device_type, uint256 i)
             hasFirmware(device_type)
             public view returns (address) {
        return device_developers[device_type][i];
    }

      /**
        * @dev Called by nodes to get a firmware from the most trusted developer.
        * @param device_type  Device Type (E.g. Raspberry pi)
        * @param stable       Firmware type: LTS or Latest Version
    */
    function get_most_trusted_firmware(string device_type, bool stable) hasFirmware(device_type)
             public view returns (bytes32, string, string, uint256,address,int256) {
        address most_trusted_dev;
        int256  max_trust = -1;
        for (uint256 i = 0; i < device_developers[device_type].length; i++ ){
                                                        // Target                        ,Origin
            int256 curr_trust = web_trust.hop_to_target(device_developers[device_type][i], msg.sender);
            if (curr_trust > max_trust){
                max_trust = curr_trust;
                most_trusted_dev = device_developers[device_type][i];
            }
        }
        // Require to trust the developer
        require(max_trust != -1, "No trusted developer found :(");
        return fw_info_to_tuple(device_type,stable,most_trusted_dev,max_trust);
    }
    // /**
    //     * @dev Called by nodes to get a firmware from the 7 most trusted developers.
    //     * @param device_type  Device Type (E.g. Raspberry pi)
    //     * @param stable       Firmware type: LTS or Latest Version
    //       Requires transaction
    // */  
    // function get_top_firmwares(string device_type, bool stable)
    //     public returns (Firmware_Info[7]){
    //     uint8 firmware_index = (stable) ? 0 : 1;
    //     //address pq_address = new PQ();
    //     PQ pq;//= PQ(pq_address);
    //     for (uint256 i = 0; i < device_developers[device_type].length; i++ ){
    //         int256 curr_trust = web_trust.hop_to_target(device_developers[device_type][i]);
    //         pq.insert(curr_trust,device_developers[device_type][i]);
    //     }
    //     Firmware_Info[7] firmware_list;
    //     for (uint8 k = 0;  i < 7; i++){
    //         PQ.Node memory tmp = pq.get_specific_node(k);
    //         firmware_list[i] = Firmware_Info(developed_firmware[device_type][tmp.value][firmware_index],tmp.value,tmp.key);
    //     }
    //     return firmware_list;
    // }

    function fw_info_to_tuple(string device_type, bool stable, address most_trusted_dev, int256 trust)
        internal view  returns (bytes32, string, string, uint256, address, int256) {
        uint8 firmware_index = (stable) ? 0 : 1;
        return (developed_firmware[device_type][most_trusted_dev][firmware_index].firmware_hash,
            developed_firmware[device_type][most_trusted_dev][firmware_index].IPFS_link, 
            developed_firmware[device_type][most_trusted_dev][firmware_index].description,
            developed_firmware[device_type][most_trusted_dev][firmware_index].block_number,
            most_trusted_dev,
            trust);
    }

    /**
        * @dev Called internally to check if a string is empty
        * @param str  String to check
    */
    function is_empty(string str) internal pure returns (bool) {
        // Source: https://ethereum.stackexchange.com/questions/11039/how-can-you-check-if-a-string-is-empty-in-solidity
        bytes memory tempEmptyStringTest = bytes(str); // Uses memory
        return (tempEmptyStringTest.length == 0);
    }


    // Priority Q //
    struct Node {
        int256 key;
        address value;
    }    


    //====== Debug Functions & Debug State ======//

    function set_version(uint256 v) public returns (address) {
        cv = v;
        return msg.sender;
    }

    function get_version() public view returns (uint256) {
        return cv;
    }

    function set_trust_version(uint256 v) public {
        web_trust.set_version(v);   
    }

    function get_trust_version() public view returns (uint256){
        return web_trust.get_version();
    }
    //===================================//
}