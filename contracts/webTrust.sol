contract Web_Of_Trust {
    
    // Avoid storing duplicates in the list
    mapping (address => mapping(address => bool)) trust_lookup;
    // Trust graph core
    mapping(address => address[]) trust_graph;

    // Hack to pass mapping as function argument
    struct map_struct {
        mapping(address => bool) visited;
    }

    // Senders trusts a target address
    function endorse_trust(address trusted_address) public {
        require(!trust_lookup[msg.sender][trusted_address]);
        require(msg.sender != trusted_address);
        trust_lookup[msg.sender][trusted_address] = true;
        trust_graph[msg.sender].length++;
        trust_graph[msg.sender][trust_graph[msg.sender].length - 1] = trusted_address; 
    }

    function hop_to_target(address target, address origin /*uint8 threshold*/) public returns (int256){
        map_struct storage ss;
        bool found;
        int256 hops;
        (hops,found) = hop_internal_rec(origin,target,ss);
        if (found)
            return hops;
        else
            return -1;
    }

    // TODO: Calculate Big O notation for the algorithm and write documentation :)

    function hop_internal_rec(address origin, address target, map_struct storage ss /*uint8 threshold*/)
            internal returns (int256,bool){
        ss.visited[origin] = true;
        if (origin == target)
            return (0,true);
        
        if (trust_lookup[origin][target])
            return (1,true);
        bool found = false;
        int256 hops = 10;
        for (uint256 i = 0; i < trust_graph[origin].length; i++){
            int256 curr_hops = 1;
            address nxt_node = trust_graph[origin][i];
            if (!ss.visited[nxt_node]){
                int256 req_hops;
                (req_hops,found) = hop_internal_rec(nxt_node,target,ss /*threshold*/);
                curr_hops += req_hops;
            }
            if (curr_hops < hops){
                hops = curr_hops;
            }
        }
        return (hops,found);
    }

    //====== Debug Functions & State ======//
    uint256 contract_version = 1;

    function set_version(uint256 cv_n) public {
        contract_version = cv_n;
    }

    function get_version() public view returns (uint256) {
        return contract_version;
    }

    function addr_to_string(address x) internal returns (string) {
        bytes memory b = new bytes(20);
        for (uint i = 0; i < 20; i++)
            b[i] = byte(uint8(uint(x) / (2**(8*(19 - i)))));
        return string(b);
    }

    function get_from_mapping(address t) public view returns (address){
        return trust_graph[t][0];
    }

    //===================================//
}



