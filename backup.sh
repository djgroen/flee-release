mkdir -p output/$1
sh plot.sh > output/$1/error.txt
cp -r out300 output/$1/
cp -r outcar output/$1/
cp -r outbur output/$1/
cp flee/*.py output/$1/
cp *.py output/$1/
