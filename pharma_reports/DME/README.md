# DME Audit

# Outputs
The script outputs several CSV files, most of which are taken by the automated R script to generate new plots. These files are:
| File                | Description                                     |
|---------------------|-------------------------------------------------|
| `initialmetrics.csv`| Initial metrics such as length and size of dataset. |
| `visual_metrics.csv`| Visual metrics (PVI, TPVI, VLP, OVC).               |
| `interval_metrics.csv`| Interval metrics (extension, reduction).      |
| `drug_int_metrics.csv`| Interval lengths and 95% CIs for different drugs.  |
| `ut_plot.png` | Longitudinal utilisation plot.     |
| `drug_distribution.csv` | Dataframe of average VAs for each patient, segmented by drug. |
| `drug_dist_table.csv` | Basic statistics for distribution of VA, segmented by drug. |
