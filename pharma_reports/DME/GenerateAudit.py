from DataSeparator import *
from InitialMetrics import *
from Utilisation import *
from Interval import *
from Vision import *
from Anchor import *
from Upload import *


def generate_audit(dr_name, folder='pharma_reports', file_list='all', df_list='all'):
    initialmetrics = InitialMetrics(df_list)
    initialmetrics.upload_results_table()
    interval = Interval('all')
    interval.upload_results_table()
    vision = Vision('all')
    vision.upload_results_table()
    plot = Utilisation('all')
    plot.plot_ut()
    anchor = Anchor('all', 3)
    anchor.upload_results_table()
    to_upload = Upload(folder, dr_name, file_list)
    to_upload.upload_files()
    to_delete = to_upload.retrieve_files()
    for file in to_delete:
        os.remove(file)
    print("The upload is complete.")


if __name__ == "__main__":
    generate_audit('Loz')
