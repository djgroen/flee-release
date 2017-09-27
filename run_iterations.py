import os

end_iter = 5

os.system("python3 itermali.py 250 -r > output/mali1/out-retrofitted.csv")
os.system("mv arrivals.txt output/mali1/")
os.system("mv debug-log.txt output/mali1/")

for i in range(2, end_iter):
  os.system("mkdir -p output/mali%s" % (i))
  os.system("python3 maliv2.py 250 > output/mali%s/out.csv" % (i))
  os.system("python3 itermali.py 250 output/mali%s/arrivals.txt > output/mali%s/out-retrofitted.csv" % (i, i))
  os.system("mv arrivals.txt output/mali%s/" % (i))
  os.system("mv debug-log.txt output/mali%s/" % (i))

for i in range(1, end_iter):
  os.system("python3 plot-flee-output.py output/mali%s -r" % (i))
  os.system("cp output/mali%s/error-retrofitted.png summary/error%s.png" % (i,i))
  os.system("cp output/mali%s/time_evolution.png summary/time_evolution%s.png" % (i,i))
