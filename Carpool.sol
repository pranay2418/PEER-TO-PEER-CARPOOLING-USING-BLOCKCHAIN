pragma solidity >= 0.8.11 <= 0.8.11;
//carpool solidity code which contains functions to save and get data
contract Carpool {
    string public users;
    string public ride;
    string public passengers;
    string public ratings;
       
    //add user details to Blockchain memory	
    function addUser(string memory us) public {
       users = us;	
    }
   //get user details
    function getUser() public view returns (string memory) {
        return users;
    }
    //add ride details to Blockchain memory
    function setRide(string memory r) public {
       ride = r;	
    }

    function getRide() public view returns (string memory) {
        return ride;
    }

    //add passengers details to Blockchain memory
    function setPassengers(string memory p) public {
       passengers = p;	
    }

    function getPassengers() public view returns (string memory) {
        return passengers;
    }

    //add passengers details to Blockchain memory
    function setRatings(string memory r) public {
       ratings = r;	
    }

    function getRatings() public view returns (string memory) {
        return ratings;
    }

    constructor() public {
        users = "";
	ride ="";
	passengers = "";
	ratings = "";
    }
}