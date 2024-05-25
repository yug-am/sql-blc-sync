// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;
contract RBMig {
 
bytes32 curr_hash ;
bytes32 prev_hash ;
struct Khatauni{
string kid;
string aadhar;
string pid;
bool struct_valid_check;
}
struct Plot{
string plotid;
string plotinfo;
bool struct_valid_check;
}
mapping(string => Khatauni) kidKhatauniMapping;
mapping(string => Plot) plotidPlotMapping;
mapping(string => Plot) plotidPlotFkMapping;
mapping(string => uint256) plotidPlotFkCtMapping;

function createKhatauniEntry(
string memory _kid, string memory _aadhar, string memory _pid, bool __uh) external {
require(kidKhatauniMapping[_kid].struct_valid_check == false, "PK not unique");
plotidPlotFkCtMapping[_pid] += 1;

kidKhatauniMapping[_kid]=Khatauni({kid: _kid,
aadhar: _aadhar,
pid: _pid,
struct_valid_check:true});

    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash,'_x_' ,_kid , '_x_' , _aadhar , '_x_' , _pid));
}

}

function createPlotEntry(
string memory _plotid, string memory _plotinfo, bool __uh) external {
require(plotidPlotMapping[_plotid].struct_valid_check == false, "PK not unique");

plotidPlotMapping[_plotid]=Plot({plotid: _plotid,
plotinfo: _plotinfo,
struct_valid_check:true});
plotidPlotFkMapping[_plotid]=plotidPlotMapping[_plotid];

    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash,'_x_' ,_plotid , '_x_' , _plotinfo));
}

}
function updateKhatauniKid(string memory _kid,string memory _kid_new, bool __uh) external {
require(kidKhatauniMapping[_kid].struct_valid_check == true, "PK not found");
require(kidKhatauniMapping[_kid_new].struct_valid_check == false, "new PK exists");
kidKhatauniMapping[_kid_new] = kidKhatauniMapping[_kid];
kidKhatauniMapping[_kid_new].kid = _kid_new;
kidKhatauniMapping[_kid].struct_valid_check = false;

    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash, '_x_', 'up_khatauni_kid','_x_' ,_kid , '_x_' , _kid_new));
}
}
function updateKhatauniAadhar(string memory _kid,string memory _aadhar, bool __uh) external {
require(kidKhatauniMapping[_kid].struct_valid_check == true, "Attrib not found");
kidKhatauniMapping[_kid].aadhar=_aadhar;
    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash, '_x_', 'up_khatauni_aadhar','_x_' ,_kid , '_x_' , _aadhar));
}
}
function updateKhatauniPid(string memory _kid,string memory _pid, bool __uh) external {
require(kidKhatauniMapping[_kid].struct_valid_check == true, "Attrib not found");
plotidPlotFkCtMapping[_pid] += 1;
plotidPlotFkCtMapping[kidKhatauniMapping[_kid].pid] -= 1;
kidKhatauniMapping[_kid].pid=_pid;
    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash, '_x_', 'up_khatauni_pid','_x_' ,_kid , '_x_' , _pid));
}
}

function updatePlotPlotid(string memory _plotid,string memory _plotid_new, bool __uh) external {
require(plotidPlotMapping[_plotid].struct_valid_check == true, "PK not found");
require(plotidPlotMapping[_plotid_new].struct_valid_check == false, "new PK exists");
require(plotidPlotFkCtMapping[_plotid] == 0, "FK dependency violation");
plotidPlotMapping[_plotid_new] = plotidPlotMapping[_plotid];
plotidPlotMapping[_plotid_new].plotid = _plotid_new;
plotidPlotMapping[_plotid].struct_valid_check = false;

    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash, '_x_', 'up_plot_plotid','_x_' ,_plotid , '_x_' , _plotid_new));
}
}
function updatePlotPlotinfo(string memory _plotid,string memory _plotinfo, bool __uh) external {
require(plotidPlotMapping[_plotid].struct_valid_check == true, "Attrib not found");
plotidPlotMapping[_plotid].plotinfo=_plotinfo;
    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash, '_x_', 'up_plot_plotinfo','_x_' ,_plotid , '_x_' , _plotinfo));
}
}

function viewKhatauniRecord(string memory _kid)external view returns(string memory kid, string memory aadhar, string memory pid){
require(kidKhatauniMapping[_kid].struct_valid_check == true, "PK not found");
kid=kidKhatauniMapping[_kid].kid;
aadhar=kidKhatauniMapping[_kid].aadhar;
pid=kidKhatauniMapping[_kid].pid;
}
function viewPlotRecord(string memory _plotid)external view returns(string memory plotid, string memory plotinfo){
require(plotidPlotMapping[_plotid].struct_valid_check == true, "PK not found");
plotid=plotidPlotMapping[_plotid].plotid;
plotinfo=plotidPlotMapping[_plotid].plotinfo;
}
function deleteKhatauniRecord(string memory _kid, bool __uh)external {
require(kidKhatauniMapping[_kid].struct_valid_check == true, "PK not found");
plotidPlotFkCtMapping[kidKhatauniMapping[_kid].pid] -= 1;
kidKhatauniMapping[_kid].struct_valid_check = false;

    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash, '_x_', 'del_khatauni',_kid));
}
}
function deletePlotRecord(string memory _plotid, bool __uh)external {
require(plotidPlotMapping[_plotid].struct_valid_check == true, "PK not found");
require(plotidPlotFkCtMapping[_plotid] == 0, "FK dependency violation");
plotidPlotMapping[_plotid].struct_valid_check = false;

    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash, '_x_', 'del_plot',_plotid));
}
}
function rollbackDeleteKhatauniRecord(string memory _kid)external {
plotidPlotFkCtMapping[kidKhatauniMapping[_kid].pid] += 1;
kidKhatauniMapping[_kid].struct_valid_check = true;
}
function rollbackDeletePlotRecord(string memory _plotid)external {
plotidPlotMapping[_plotid].struct_valid_check = true;
}
function revertHash()external {
     curr_hash = prev_hash;
}function getHash() public view returns (bytes32) {
return curr_hash;
    }
}

