python3 maliv2.py 50 > out300/out.csv &
python3 maliv2.py 50 -r > out300/out-retrofitted.csv &
python3 car.py 50 > outcar/out.csv &
python3 car.py 50 -r > outcar/out-retrofitted.csv &
python3 burundi.py 50 > outbur/out.csv &
python3 burundi.py 50 -r > outbur/out-retrofitted.csv &
wait
python3 plot-flee-output.py outcar &
python3 plot-flee-output.py out300 &
python3 plot-flee-output.py outbur &
python3 plot-flee-output.py outcar -r&
python3 plot-flee-output.py out300 -r&
python3 plot-flee-output.py outbur -r&
wait
