#!/bin/bash

# Unit Test for update user endpoint

# invalid case
#curl -H "Content-Type: application/json" -X PUT -d '{"fname":"Shane","contact":"18687230782"}' http://localhost:80/v1.0/users

# Valid case
curl -H "Content-Type: application/json" -X PUT -d '{"id":"2","name":"updated item","description":"we just updated the item","negotiable":"no","price":"19.95"}' http://localhost:80/v1.0/items
