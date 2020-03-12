rm test-output/*
python3 test_csv.py > test-output/out.csv
python3 plot-flee-output.py test-output
