#!/bin/bash

rules=`ls *.json | grep -v 'default'`
for eachfile in $rules
do
   checksum=$(cat $eachfile | md5sum | cut -d ' ' -f1)
   echo '   "'$checksum'": {
           "filename": "'$eachfile'",
           "active": true
       },'
done
