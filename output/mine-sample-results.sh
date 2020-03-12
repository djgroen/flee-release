#!/bin/bash

rm tmp.txt

for i in {1..50}
do
  echo $i >> tmp.txt
  cat sample${i}-aw1-speed200/error.txt | grep "error" | grep "outbur" | awk '{print $6}' >> tmp.txt
  cat sample${i}-aw1-speed200/error.txt | grep "error" | grep "outcar" | awk '{print $6}' >> tmp.txt
  cat sample${i}-aw1-speed200/error.txt | grep "error" | grep "out300" | awk '{print $6}' >> tmp.txt
  cat sample${i}-aw1-speed200/error.txt | grep "error" | grep "outbur" | awk '{print $9}' >> tmp.txt
  cat sample${i}-aw1-speed200/error.txt | grep "error" | grep "outcar" | awk '{print $9}' >> tmp.txt
  cat sample${i}-aw1-speed200/error.txt | grep "error" | grep "out300" | awk '{print $9}' >> tmp.txt
done

echo "#sample,bur-normal,car-normal,mali-normal,bur-rescaled,car-rescaled,mali-rescaled"
sed 'N;N;N;N;N;N;s/\n/,/g' tmp.txt
