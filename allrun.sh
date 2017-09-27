python3 maliv2.py 250 > out300/out.csv &
python3 car.py 500 > outcar/out.csv &
python3 burundi.py 250 > outbur/out.csv &
#wait
#echo "completed normal sims"
python3 burundi.py 250 -r > outbur/out-retrofitted.csv &
python3 maliv2.py 250 -r > out300/out-retrofitted.csv &
python3 car.py 500 -r > outcar/out-retrofitted.csv &
wait
echo "completed time retrofitted sims"
python3 plot-flee-output.py outcar &
python3 plot-flee-output.py out300 &
python3 plot-flee-output.py outbur &
wait
python3 plot-flee-output.py outcar -r&
python3 plot-flee-output.py out300 -r&
python3 plot-flee-output.py outbur -r&
wait
