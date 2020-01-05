from web3 import Web3, HTTPProvider
import os
import json

# from web3.providers.eth_tester import EthereumTesterProvider
# from solc import compile_source

host = 'https://ropsten.infura.io/v3/bf3c5595597d42b3bf8ddb9a5fa08a26'
# host = 'http://127.0.0.1:7545'
provider = HTTPProvider(host)
web3 = Web3(provider)

print('Connected to {} : {}'.format(host, web3.isConnected()))

