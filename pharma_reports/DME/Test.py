from DataSeparator import *
import numpy as np
import pandas as pd
from datetime import date
import statistics
import warnings
warnings.filterwarnings('ignore')
import statsmodels.stats.api as sms

if __name__ == "__main__":
    obj = DataSeparator('all', '/devchau.csv')
    pdf_list = obj.patient_dataframes()
    print(len(pdf_list))