#!/bin/bash

# unit test to check functionality of delete user endpoint

#invalid request
printf "Testing delete endpoint with invalid credentials \n"
curl -H "Content-Type: application/json" -X DELETE -d '{"idz":"1"}' http://localhost:80/v1.0/users

#valid request
printf "Testing delete endpoint with valid credentials \n"
curl -H "Content-Type: application/json" -X DELETE -d '{"user_id":"5"}' http://localhost:80/v1.0/users
