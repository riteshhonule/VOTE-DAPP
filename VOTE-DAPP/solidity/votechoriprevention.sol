// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

contract VoteChoriPrevention {
    struct Party {
        string name;
        uint256 votes;
    }

    mapping(address => bool) public hasVoted;
    Party[] public parties;
    address public owner;

    event VoteCasted(address indexed voter, string partyName);

    constructor() {
        owner = msg.sender;
        parties.push(Party("BJP", 0));
        parties.push(Party("Congress", 0));
        parties.push(Party("Aam Aadmi Party", 0));
    }

    modifier onlyOnce() {
        require(!hasVoted[msg.sender], "You have already voted!");
        _;
    }

    function vote(uint256 _partyIndex) external onlyOnce {
        require(_partyIndex < parties.length, "Invalid party index");
        parties[_partyIndex].votes += 1;
        hasVoted[msg.sender] = true;
        emit VoteCasted(msg.sender, parties[_partyIndex].name);
    }

    function getAllVotes() external view returns (Party[] memory) {
        return parties;
    }

    function getPartyCount() external view returns (uint256) {
        return parties.length;
    }

    function getParty(uint256 index) external view returns (string memory, uint256) {
        require(index < parties.length, "Invalid index");
        Party memory p = parties[index];
        return (p.name, p.votes);
    }
}
        