# Pharma Reports

Pharma reports can be grouped into two general categories: 
1. nAMD reports that focus on traditional treatment statistics.
2. DME reports which are subject to dirtier and more heteregeneous data.

List of files:
| File                | Description                                     |
|---------------------|-------------------------------------------------|
| `dme.ipynb`          | The exploratory analysis of the DME (extra ML). |
| `DMEAudit.ipynb`      | Generates DMEAudit report.                      |
| `DoctorAudit.ipynb`   | Generated nAMD report (basic statistics).       |
| `automated_plots.R`   | Generates plots for both nAMD and DME reports.  |
| `clients_secret.json` | Stores the OAuth credentials for PyDrive.       |

## nAMD reports
The process for generating an nAMD audit report for a doctor is:
1. Open up the script written in [DoctorAudit.](pharma_reports/DoctorAudit.ipynb)
2. Use the OAuth to authenticate the connection to PyDrive (should be given as a link on import). This will allow you to write and push files to Macuject's Google Drive.
3. Insert the appropriate path to the doctor's CSV file (at the moment, this is clumsily done by changing the path in the `DataSeparator` class itself).
4. Generate the report by calling `generate_audit('dr_name')`.
5. Run the R-script that pulls down the CSV files just created and pushed to drive, and creates and pushes the plots to the same folder. This R-script is in [automated_plots.R.](pharma_reports/automated_plots.R)

## DME reports
The process for DME is almost identical to above. At the moment, the same R script is used, except without the ANCHOR plot function at the end (it will throw an error).
