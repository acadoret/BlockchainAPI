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

# Install on server 

### On google platform
install all dependencies 
sudo apt install python git apache2 -y && mkdir documents && mkdir documents/BlockchainAPI/ && git clone https://github.com/acadoret/BlockchainAPI.git && cd BlockchainAPI && sudo apt-get -y install python3-pip && pip3 install -r requirements.txt && sudo echo "LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so
Listen 80
<VirtualHost *:80>
        ServerName 34.89.25.174
        ProxyPass / http://127.0.0.1:5000/
        ProxyPassReverse / http://127.0.0.1:5000/
        <Directory /documents/BlockchainAPI/BlockchainAPI/>
                Order deny,allow
                Allow from all
        </Directory>
        <Proxy *>
                Order deny,allow
                Allow from all
        </Proxy>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
" > /etc/apache2/sites-available/000-default.conf && sudo systemctl reload apache2
