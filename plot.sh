rm ${1}outcar/*.png
rm ${1}out300/*.png
rm ${1}outbur/*.png
python3 plot-flee-output.py ${1}outcar &
python3 plot-flee-output.py ${1}out300 &
python3 plot-flee-output.py ${1}outbur &
wait
#python3 plot-flee-output.py ${1}outcar -r&
#python3 plot-flee-output.py ${1}out300 -r&
#python3 plot-flee-output.py ${1}outbur -r&
#wait
