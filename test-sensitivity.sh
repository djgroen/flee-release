#!/bin/bash

CSVDIR=SimSettingCSVs

FILES=${CSVDIR}/*
for f in $FILES
do
  fname=$(echo $(basename $f) | cut -f 1 -d '.')
  echo "$f $fname"

  python3 maliv2.py $f > out300/out.csv &
  python3 car.py $f > outcar/out.csv &
  python3 burundi.py $f > outbur/out.csv &
  wait
  python3 plot-flee-output.py outcar &
  python3 plot-flee-output.py out300 &
  python3 plot-flee-output.py outbur &
  wait

  sh backup.sh sensitivity-${fname}
done
