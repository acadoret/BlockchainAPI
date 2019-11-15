### BlockchainAPI
**Work in Progress**

Python 3 API allow to manage users and Smart Contracts on Ethereum Blockchain.
Based on [Flask microframework](https://flask.palletsprojects.com/en/1.1.x/)

## Using

### Managing users
 - Create user:  `/users/create`
 - Get all users: `/users`
 - Get a single user by address: `/users/<address>`
 - Update an existing user: `/users/update/<address>`

### Managing contracts
 - Create contract:  `/contracts/create`
 - Get all contracts: `/contracts`
 - Get a single contract by address: `/contracts/<address>`
 
# Tips

### Install dependencies from requirements:
    pip install -r requirements.txt
### Run venv: 
    sources /<path_to_env>/bin/activate
### Make migration: 
    python manage.py db migrate --message 'put message here'
### Upgrade db:
    python manage.py db upgrade
### Start server: 
    python manage.py run
### Run testing procedure:
    python manage.py test

