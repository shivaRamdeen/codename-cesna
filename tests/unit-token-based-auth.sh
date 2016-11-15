#!/bin/bash

#Invalid, without password/credentials
curl http://localhost:80/v1.0/test

# Valid with Password
curl -u shiva.ramdeen@outlook.com:password http://localhost:80/v1.0/token
