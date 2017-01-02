#!/bin/bash

#automatic installation of the server and its dependencies.
#Application will be containerized in the future.

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python-pip -y
sudo pip install --upgrade pip
sudo apt-get install mysql-server -y
sudo apt-get intall libmysqlclient-dev -y

echo "We are now going to secure mysql."
echo "Please ensure that your root password matches the msql connection string in 'database.py' and all other files"

#waiting for user to see our prompt
sleep 3

sudo mysql_secure_installation
sudo pip install -r requirements.txt

#instructions for final setup
echo Run the following command to create the default database
echo "mysql -u root -e 'CREATE DATABASE hustle' -p"
echo "Then run "sudo python database.py" to create the database tables"
