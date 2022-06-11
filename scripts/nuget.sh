#!/bin/bash
while read -r line
do
  curl -s "$line" > page.html
  PKG=$(echo $line | cut -d '/' -f5)
  ATOM=$line"atom.xml"
  curl -s "$line"atom.xml > atom.xml
  LICENSE=$(cat page.html | grep 'license' | cut -d '>' -f2 | cut -d '<' -f1)
  DOWN=$(cat page.html | grep 'outbound-manual-download' | cut -d '"' -f2)
  echo $PKG [$LICENSE]
done < "./nuget_urls.txt"
