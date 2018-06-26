pragma solidity ^0.4.23;
pragma experimental ABIEncoderV2;


contract state {
    uint256 contract_version = 1;
    uint8 pp = 0;
    function set_version(uint256 cv_n) public {
        contract_version = cv_n;
    }
    function get_version() public returns (uint256) {
        pp += 1;
        return contract_version;
    }
}

contract complicated {
    state st;
    uint8 tt = 0;
    constructor() public {
        address st_address = new state();
        st = state(st_address);
    }
    
    function set_version(uint256 cv_n) public {
        st.set_version(cv_n);
    }

    function get_version() public returns (uint256) {
        tt += 1;
        return st.get_version();
    }
}