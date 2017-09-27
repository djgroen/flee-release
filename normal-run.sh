python3 maliv2.py 300 > out300/out.csv &
python3 car.py 820 > outcar/out.csv &
python3 burundi.py 396 > outbur/out.csv &
wait
python3 plot-flee-output.py outcar &
python3 plot-flee-output.py out300 &
python3 plot-flee-output.py outbur &
wait
