from web3 import Web3, HTTPProvider
import os
import json

# from web3.providers.eth_tester import EthereumTesterProvider
# from solc import compile_source

host = 'http://127.0.0.1:7545'
provider = HTTPProvider(host)
web3 = Web3(provider)

print('Connected to {} : {}'.format(host, web3.isConnected()))

