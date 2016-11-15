#!/bin/bash

# Tester for item create endpoint

#invalid case
#curl -H "Content-Type: application/json" -X POST -d '{"user_id":"1","name":"test item","description":"an item for testing db and server endpoints","negotiable":"Flase"}' http://localhost:80/v1.0/items

#valid case
curl -H "Content-Type: application/json" -X POST -d '{"user_id":"2","name":"test item","description":"an item for testing db and server endpoints","price":"12.99","negotiable":"Flase"}' http://localhost:80/v1.0/items
