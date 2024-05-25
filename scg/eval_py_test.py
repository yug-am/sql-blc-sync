from web3 import Web3

def createKhatauniEntry(_kid, _aadhar, _pid):
    hash = b'\x00' * 32
    delimiter = "_x_"
    concatenated_bytes = hash + delimiter.encode('utf-8') + _kid.encode('utf-8') + delimiter.encode('utf-8')
    concatenated_bytes += _aadhar.encode('utf-8') + delimiter.encode('utf-8') + _pid.encode('utf-8')
    new_hash = Web3.solidity_keccak(['bytes'], [concatenated_bytes])
    return new_hash

def createPlotEntry(_plotid, _plotinfo):
    hash = b'\x00' * 32
    delimiter = "_x_"
    concatenated_bytes = hash + delimiter.encode('utf-8') + _plotid.encode('utf-8') + delimiter.encode('utf-8') + _plotinfo.encode('utf-8')
    new_hash = Web3.solidity_keccak(['bytes'], [concatenated_bytes])
    #print(new_hash.hex())
    return new_hash.hex()

if __name__ == "__main__":
    test_str = "createPlotEntry('1', 'kl_clt_01')"
    res = eval(test_str)
    print(res)
    # pass
