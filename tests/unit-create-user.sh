#!/bin/bash

# Unit test - exercise the create user API endpoint
#

printf "Unit testing Create User Endpoint With Valid Credentials \n"
curl -H "Content-Type: application/json" -X POST -d '{"fname": "Shiva","lname":"Ramdeen","email":"shiva.ramdeen@outlook.com","contact":"8687741432","password":"password"}' http://localhost:80/v1.0/users

printf "Unit testing Create user endpoint with Missing Credentials \n"
curl -H "Content-Type: application/json" -X POST -d '{"lname":"Ramdeen","email":"shiva.ramdeen@outlook.com","contact":"8687741432","password":"password"}' http://localhost:80/v1.0/users


