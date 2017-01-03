#!/bin/bash

#automatic installation of the server and its dependencies.
#Application will be containerized in the future.

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python-pip -y
sudo pip install --upgrade pip
sudo apt-get install mysql-server -y
sudo apt-get install libmysqlclient-dev -y

echo ...
echo ...
echo ...
echo "We are now going to secure mysql."
echo "Please ensure that your root password matches the msql connection string in 'database.py' and all other files"
echo ...
echo ...
echo ...

#waiting for user to see our prompt
sleep 3

sudo mysql_secure_installation
sudo pip install -r requirements.txt

#instructions for final setup
echo ...
echo ...
echo !!!IMPORTANT INSTRUCTIONS!!!
echo Run the following command to create the default database
echo "mysql -u root -e 'CREATE DATABASE hustle' -p"
echo "Then run "sudo python database.py" to create the database tables"
echo ...
sleep 3
