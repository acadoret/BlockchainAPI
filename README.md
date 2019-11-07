### BlockchainAPI
**Work in Progress**

Python 3 API allow to manage users and Smart Contracts on Ethereum Blockchain.
Based on [Flask microframework](https://flask.palletsprojects.com/en/1.1.x/)

## Using

### Managing users
 - Create user:  `/users/create`
 - Get users: `/users`
 - Get user by address: `/users/<address>`
 - Update an existing user: `/users/update/<id>`

### Managing contracts
 - Create contract:  `/contracts/create`
 - Get contracts: `/contracts`
 - Get contract by id: `/contracts/<address>`
 
# Tips

### Refresh dependencies :
    pip freeze > requirements.txt
### Install dependencies from requirements :
    pip install -r requirements.txt
### Run venv : 
    sources /env/bin/activate
### Start server : 
    python manage.py run
### Init db : 
    python manage.py db init
### Make migration : 
    python manage.py db migrate --message 'put message here'
### Upgrade db :
    python manage.py db upgrade
### Run testing procedure :
    python manage.py test
### PUT CLI request : 
     $ curl -X PUT -H "Content-Type: application/json" -d '{"name":"mkyong","email":"abc@gmail.com"}' http://localhost:5000/users
