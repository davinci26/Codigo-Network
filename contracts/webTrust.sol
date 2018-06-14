contract webTrust {
    
    mapping(address => address[]) public trust_graph;
    
    function endorse_trust(address trusted_address) public {
        trust_graph[msg.sender].push(trusted_address);   
    }
    
}