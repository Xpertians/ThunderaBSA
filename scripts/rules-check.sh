#!/bin/bash
rules=`ls *.json | grep -v 'default'`
for eachfile in $rules
do
  echo $eachfile
  cat $eachfile | python -c "import sys,json;json.loads(sys.stdin.read());print 'OK'"
done
