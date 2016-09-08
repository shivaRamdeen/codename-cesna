#!/bin/bash

# Unit test - exercise the create user API endpoint
#

curl -H "Content-Type: application/json" -X POST -d '{"fname": "Shiva","lname":"Ramdeen","email":"shiva.ramdeen@outlook.com","contact":"8687741432","password":"password"}' http://localhost:80/v1.0/users
