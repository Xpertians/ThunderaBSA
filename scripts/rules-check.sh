#!/bin/bash
rules=`ls thundera/rules/*.json | grep -v 'default'`
for eachfile in $rules
do
  echo $eachfile
  cat $eachfile | python -c "import sys,json;json.loads(sys.stdin.read());print 'OK'"
done
