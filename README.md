# RDBMS Chain Bridge
## Description

RDBMS Chain Bridge is a blockchain and RDBMS live synchronization framework. The Framework is written in Python and has three sub-modules Blockchain To SQL (BTS), SQL To Blockchain(STB), and Smart contract generator. Blockchain-based solutions are being readily accepted and incorporated but to fully switch to these solution data in existing systems is required and therefore will require data synchronization from old systems like RDBMS to Blockchain.

### Smart Contract Generator(SCG)

It connects to the mySQL server, reads table schema, and generates a solidity smart contract that enforces RDBMS data constraints and relationships. Relevant business rules can be added to the generated for a smart contract with domain rules and also upholding RDBMS constraints.

### Blockchain To SQL (BTS) 

It takes smart contract function calls as input, synchronizes it across the mySQL server and configures Blockchain to mySQL server. It ensures that before the smart contract call operation is in the same state, the equivalent operation is executed in both after the operation both are in the same state.

### SQL To Blockchain (STB) 

It takes SQL statements as input, synchronizes it across the mySQL server and configures Blockchain to the mySQL server. It ensures that before the smart contract call operation is in the same state, the equivalent operation is executed in both after the operation both are in the same state.



## Table of Contents 

Quickly navigate across this README
- [Installation](#installation)
- [Usage](#usage)
- [Test🧪](#test)
- [Contribute](#contribute)
- [License📄](#license)

## Installation

Git clone this project and directly run from terminal

#### Prerequisites
- Python
- MySQL Connector Python library [link](https://dev.mysql.com/doc/connector-python/en/)
- Web3 Python library [link](https://web3py.readthedocs.io/en/stable/)
    

## Usage

- Configure chain and mySQL configurations in programs and run by navigating to main files in relevant sub module folders 
| Module                   | Main python file           | Configuration  file |
|------------------------------- |----------------------|------------------|
| Smart Contract Generator (SCG) | smart_contract_baker |schema_extract    |            
| Blockchain To SQL (BTS)        | sync_live_sql_blc    |sync_live_sql_blc |
| SQL To Blockchain (STB)        | sync_live_blc_sql    |sync_live_blc_sql |

In the case of SCG first configure and run schema_extract then run smart_contract_baker to get the solidity code with RDBMS constraints.
Other modules can be run directly with the respective main file as specified in the Module file table. 
Also, for bootstrap testing, the modules read SQL commands or Blockchain smart contract calls from a text file in `./input_sync_sql_blc`.
Only works with string data type because web3 encoding library output is not the same as EVM output.

## Test

The Framework is tested with [Truffule](https://trufflesuite.com/) and [mySQL](https://www.mysql.com/).

<img src="https://trufflesuite.com/img/truffle-logo-dark.svg" width="200">


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)

## Contribute
Contribution in documentation, examples and extension would be delightful.

## License

[MIT License](LICENSE)





