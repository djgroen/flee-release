# Flee

Flee is an agent-based modelling toolkit which is purpose-built for simulating
the movement of individuals across geographical locations. Flee is currently
used primarily for modelling the movements of refugees and internally displaces
persons (IDPs).

Flee is released under a BSD 3-clause license. The GitHub repository with the
latest source can be found at http://www.github.com/djgroen/flee-release.

If you use Flee for your research publications, you can give us credit
by citing our Scientific Reports paper: http://dx.doi.org/10.1038/s41598-017-13828-9.

* Diana Suleimenova, David Bell, and Derek Groen. "A generalized simulation development approach for predicting refugee destinations.", Scientific Reports 7, Article number: 13377 (2017). 

## Simple Test for Flee

Try a toy example of Flee using:

python3 test_flee.py


## Main source files

| file name                  | what it does                                |
| -------------------------- | -------------------------------------------:| 
| flee/flee.py               | Main ABM kernel                             |
| flee/SimulationSettings.py | Data structure for global sim parameters.   |
| analysis.py                | Library with statistical analysis routines. |
| DataTable.py               | Data Handling kernel for csv data.          |


## Testing Flee

Flee consists of a range of testing scripts. These are:

| script name          | what it does                         |
| -------------------- | ------------------------------------:| 
| test\_datatable.py   | Test data loading from CSV           |
| test\_flee.py        | Test simple simulation of Mali       |
| test\_removelink.py  | Test link removal                    |
| test\_toy\_escape.py | Test toy escape scenario             |

All tests can be run with Python 3, no arguments need to be specified.

## Active simulations


| script name         | what it does                         |
| ------------------- | ------------------------------------:| 
| maliv2.py           | Mali simulation                      |
| burundi.py          | Burundi simulation                   |
| car.py              | CAR simulation                       |


