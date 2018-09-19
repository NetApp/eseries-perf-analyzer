#!/bin/bash

#This is the classic port used for the plaintext format by carbon
PORT=2003
SERVER=localhost

for i in `seq 1 100`;
do
    echo "test.out $i `date +%s`" | nc  $SERVER $PORT
    sleep 5
done
