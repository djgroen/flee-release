# Flee

Flee is an agent-based modelling toolkit which is purpose-built for simulating the movement of individuals across geographical locations. Flee is currently used primarily for modelling the movements of refugees and internally displaces persons (IDPs).

Flee is currently closed-source, but will be released periodically under a BSD 3-clause license once the first journal paper is accepted.

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
| test\_retrofit.py    | Test time retrofitting functionality |
| test\_toy\_escape.py | Test toy escape scenario             |

All tests can be run with Python 3, no arguments need to be specified.

## Active simulations


| script name         | what it does                         |
| ------------------- | ------------------------------------:| 
| maliv2.py           | Mali simulation                      |
| burundi.py          | Burundi simulation                   |
| car.py              | CAR simulation                       |
| iraq-idp.py         | Iraq simulation (IDPs only)          |


