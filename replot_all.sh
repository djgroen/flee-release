FILES=output/*
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  sh plot.sh $f/ > $f/error.txt
done
