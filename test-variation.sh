#!/bin/bash

for i in {11..50}
do
  echo "sh normal-run.sh && sh backup.sh sample${i}-aw1-speed200"
  sh normal-run.sh && sh backup.sh sample${i}-aw1-speed200
done
