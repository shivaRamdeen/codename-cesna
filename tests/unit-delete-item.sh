#!/bin/bash

#valid case
#printf "Testing delete endpoint with valid credentials \n"
curl -H "Content-Type: application/json" -X DELETE -d '{"id":"1", "user_id":"1"}' http://localhost:80/v1.0/items


#invalid case
