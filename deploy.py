from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os
load_dotenv()
with open("./SimpleStorage.sol", "r") as file:
    Simple_Storage_file = file.read()
    
    #compile our solidity
    print("Installing....")
    install_solc('0.8.15')

    compiled_sol = compile_standard(
    {
    "language":"Solidity",
    "sources":{"SimpleStorage.sol":{"content": Simple_Storage_file}},
    "settings":{
        "outputSelection":{
            "*":{"*" : ["abi","metadata","evm.bytecode","evm.sourceMap"]}
        }
    },
    },
    solc_version="0.8.15",
  )  

# bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to ganache

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x99629653e3FFc4d307Ac88b953270C44aB2C5bb1"
private_key = os.getenv("PRIVATE_KEY")

# CREATE CONTRACT in python
SimpleStorage = w3.eth.contract(abi = abi,bytecode= bytecode)
#get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)



transaction  = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from":my_address,"nonce": nonce}

)

signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)
#send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


#working with contract 
#contract ABI
#contract address

simple_storage = w3.eth.contract(address = tx_receipt.contractAddress,abi=abi)
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId":chain_id, "from":my_address,"nonce":nonce +1}

)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction,private_key = private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())
