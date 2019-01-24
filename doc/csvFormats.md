This document provides formats of csv files for loading initial graph. Each conflict has three main csv files:

 ## 1. locations.csv
 
    |name| region| country| lat| lon| location_type| conflict_date| pop/cap              |
    |----|-------|--------|----|----|--------------|--------------|----------------------|
    |    |       |        |    |    | -conflict    |              |-population for cities|
    |    |       |        |    |    | -town        |              |                      |
    |    |       |        |    |    | -camp        |              |-capacities for camps |
 
 conflict_data is given as an integer, counting the number of days after the simulation start. The value of -1 indicates the end of the simulation, while 0 indicates the start.

 ## 2. routes.csv

    |name1| name2| distance|forced_redirection|
    |-----|------|---------|------------------|
    |     |      |         |                  |


 ## 3. closures.csv  (Border closure events at country or location levels)
   
    |closure_type| name1| name2| closure_start| closure_end|
    |------------|------|------|--------------|------------|
    | -country   |      |      |              |            |
    | -location  |      |      |              |            |
    
    closure_start and closure_end are given as integers, counting the number of days after the simulation start. The value of -1 indicates the end of the simulation.
