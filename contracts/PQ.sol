pragma solidity ^0.4.23;
pragma experimental ABIEncoderV2;

contract PQ {

    struct Node {
        int256 key;
        address value;
    }    
    /* 
     *  Storage
     */
    Node[7] private heapKeyValue;
    uint8 private current_size = 0;
    function insert(int256 key, address addr) public {

        if (current_size == 7) {
            uint8 indx;
            bool inserted;
            (inserted,indx) = find_replace_max(key,addr);
            if (inserted)
                heapify(indx);
        } else {
            heapKeyValue[current_size] = Node(key,addr);
            heapify(current_size);
            current_size += 1;
        }
    }

    function get_specific_key(uint8 i) public view returns (int256){
        require(i<=6);
        return heapKeyValue[i].key;
    }

    function get_specific_node(uint8 i) public view returns (Node){
        require(i<=6);
        return heapKeyValue[i];
    }

    function get_min_node() public view returns (Node) {
        return heapKeyValue[0];
    }

    function get_min_key() public view returns (int256){
        return heapKeyValue[0].key;
    }

    function heapify(uint8 idx) internal {
        if (idx == 0) return;
        uint8 curr_idx = idx;
        uint8 par_idx = curr_idx/2;
        while (heapKeyValue[curr_idx].key < heapKeyValue[par_idx].key ) {
            swap_values(curr_idx,par_idx);
            curr_idx = par_idx;
            par_idx = curr_idx/2; 
        }
    }

    function find_replace_max(int256 target_key, address addr) internal returns (bool,uint8) {
        uint8 max_pos = 8;
        int256 max_value = -10;
        for (uint8 i = 3; i < 7; i++){
            if (heapKeyValue[i].key > max_value){
                max_pos = i;
                max_value = heapKeyValue[i].key;
            }
        }
        if (target_key < max_value) {
            heapKeyValue[max_pos].key = target_key;
            heapKeyValue[max_pos].value = addr;
            return (true,max_pos);
        }
        return (false,max_pos);
    }

    function swap_values(uint8 lhs, uint8 rhs) internal {
        Node memory tmp = heapKeyValue[lhs];
        heapKeyValue[lhs] = heapKeyValue[rhs];
        heapKeyValue[rhs] = tmp;
    }

}