import numpy as np
from DataSeparator import *
import pandas as pd
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import date
import statistics
import warnings
warnings.filterwarnings('ignore')


class InitialMetrics(DataSeparator):

    def __init__(self, df_list):
        self.df_list = df_list

    def study_period(self, df):
        """
        Returns the study period in question.
        Input: Pandas dataframe.
        Output: datetime object x 2.
        """
        dates = df['admission_date']
        return dates.min(), dates.max()

    def num_patients(self, df):
        """
        Returns the number of patients treated.
        """
        return len(df['id'].unique())

    def total_visits(self, df):
        """
        Returns the number of total visits.
        """
        return len(df)

    def initiation_drug(self, df):
        '''
        Input: Pandas dataframe of all patients.
        Output: mean initiation drugs.
        '''
        id_list = df['id'].unique()
        lst, names = [], ['Lucentis', 'Eylea', 'Avastin']
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['Drug'], inplace=True)
            df = df[df['Drug'] != 'nil']
            df = df[df['Drug'] != 'None']
            if len(pdf['Drug']) != 0 and pdf['Drug'].iloc[0] in names:
                lst.append(pdf['Drug'].iloc[0])
        luc_int = np.round(lst.count('Lucentis') / len(lst), 3)
        eyl_int = np.round(lst.count('Eylea') / len(lst), 3)
        av_int = np.round(lst.count('Avastin') / len(lst), 3)
        return luc_int, eyl_int, av_int

    def patient_drugs(self):
        """
        Returns a percentage of patients on Lucentis, Eylea and multiple drugs.
        """
        df_list = DataSeparator.get_dataframes(self)
        luc_count = len(df_list[0].id.unique())
        eyl_count = len(df_list[1].id.unique())
        mult_count = len(df_list[2].id.unique())
        total = luc_count + eyl_count + mult_count
        return np.round((luc_count / total) * 100), np.round((eyl_count / total) * 100), np.round(
            (mult_count / total) * 100)

    def results_table(self):
        """
        Returns a dataframe of results for all initial metrics.
        Input: self.
        Output: Pandas dataframe.
        """
        df = DataSeparator.get_df(self)
        earliest, latest = self.study_period(df)
        luc_int, eyl_int, av_int = self.initiation_drug(df)
        luc_count, eyl_count, mult_count = self.patient_drugs()
        dict = {'Start': earliest, 'End': latest, 'Num_Patients': self.num_patients(df),
                'TotalVisits': self.total_visits(df), 'LucentisInit%': luc_int * 100, 'EyleaInit%': eyl_int * 100,
                'AvastinInit%': av_int * 100, 'Lucentis%': luc_count, 'Eylea%': eyl_count, 'Mult%': mult_count}
        return pd.DataFrame(dict, index=[0])

    def upload_results_table(self):
        dataframe = self.results_table()
        dataframe.to_csv(general_path + '/initialmetrics.csv')
