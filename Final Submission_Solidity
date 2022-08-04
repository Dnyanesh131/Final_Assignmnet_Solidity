// SPDX-License-Identifier: MIT

pragma solidity ^0.8.15;
contract SimpleStorage{
    uint anyNumber;

    struct People{
        uint256 anyNumber;
        string name;

    }
    People[] public  people;
   mapping(string=>uint256) public nameToAnyNumber;
    function store(uint256 _anyNumber) public returns(uint256){
        anyNumber= _anyNumber;
        return _anyNumber;

    }

    function retrieve() public view returns(uint256){
        return anyNumber;
    }

    function addPerson(string memory _name,uint256 _anyNumber)public {
        people.push(People(_anyNumber,_name));
        nameToAnyNumber[_name]=_anyNumber;

    }
}
