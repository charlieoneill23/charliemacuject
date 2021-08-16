# DME Data Dictionary

## Doctors present
The doctors we currently have are:
| Doctor                        | CSV file        |
|-------------------------------|-----------------|
| Dr Devinder Chauhan           | devchau.csv     |
| Dr Devinder Chauhan (Boronia) | devchau_bor.csv |
| Dr Eric Mayer                 | ericmayer.csv   |
| Dr Brendan Vote (Launceston)  | brendanvote.csv |

This data consists of individual patient visits for each doctor. The data is thus longitudinal.

## Aggregated data
Each patient's longitudinal data can be aggregated into a single row of interesting statistics. 
For instance, we can measure the time to peak visual improvement (TPVI). This aggregated data is stored in:
* `/home/jupyter/charliemacuject/pharma_reports/data/DME/dme_features.csv`

