from DataSeparator import *
import math
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class Anchor(DataSeparator):

    def __init__(self, csv_name, subset, interval):
        super().__init__(subset, csv_name)
        self.interval = interval
        self.csv_name = csv_name
        self.data_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/data/DME'
        self.doctor_path = self.data_path + self.csv_name
        self.general_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/DME'


    def month_column(self, pdf, interval):
        """
        Appends month since starting as a column to patient df.
        Interval is the grouping of months i.e. 3 = 3 month intervals.
        Interval = 12 --> yearly intervals.
        """
        pdf.sort_values(by=['admission_date'], inplace=True)
        initial_date = pdf.admission_date.iloc[0]
        months_list = [0]
        for i in range(len(pdf)-1):
            months = round((pdf.admission_date.iloc[i] - initial_date).days / 28)
            months_list.append(math.floor(months/interval))
        pdf['period_since_start'] = months_list
        return pdf

    def vision_month(self, period, interval):
        """
        Produces average vision at a certain visit after initiation.
        Input: dataframe, number of visits after initiation (int)
        Output: mean visual acuity of all patients at that visit
        """
        pdf_list = DataSeparator.patient_dataframes(self, drop_drug_na=True)
        lst = []
        for pdf in pdf_list:
            pdf.admisssion_date = pd.to_datetime(pdf.admission_date, dayfirst=True)
            pdf.sort_values(by=['admission_date'], inplace=True)
            if len(pdf) > 0:
                pdf = self.month_column(pdf, interval)
                visions = pdf['visual_acuity'].to_list()
                for i in range(len(pdf)):
                    if pdf.period_since_start.iloc[i] == period:
                        if pdf.visual_acuity.iloc[i] > 0:
                            lst.append(visions[i] - visions[0])
        return np.round(np.mean(lst), 2), np.round(np.std(lst), 2), len(lst)

    def anchor(self, num_periods, vision=True):
        """
        Produces a dataframe of mean vision over the first year, including trial results.
        Also produces the standard ANCHOR figures for the same period.
        Input: Pandas dataframe (all patients), num_periods.
        Output: Pandas dataframe.
        """
        df_list = DataSeparator.get_dataframes(self)
        df = df_list[-1]
        anchor_list = [0]
        std_list = [0]
        length_list = [0]
        months = [x for x in range(num_periods+1)]
        for i in range(num_periods):
            if vision: mean, std, length = self.vision_month(i, self.interval)
            else: mean, std, length = self.interval_month(i, self.interval)
            anchor_list.append(mean)
            std_list.append(std)
            length_list.append(length)
        period_string = str(self.interval)
        dict = {'Period('+period_string+'monthInts)': months, 'Doctor_Mean': anchor_list,
                'StdDeviation': std_list, 'No.Visits': length_list}
        df = pd.DataFrame(dict)
        df.set_index('Period('+period_string+'monthInts)', inplace=True)
        return df

    def interval_month(self, period, interval):
        pdf_list = DataSeparator.patient_dataframes(self, drop_drug_na=True)
        lst = []
        for pdf in pdf_list:
            pdf.admisssion_date = pd.to_datetime(pdf.admission_date, dayfirst=True)
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['NextInt'], inplace=True)
            pdf = pdf[pdf.NextInt != '?']
            pdf.NextInt = pd.to_numeric(pdf.NextInt)
            if len(pdf) > 0:
                pdf = self.month_column(pdf, interval)
                for i in range(len(pdf)):
                    if pdf.period_since_start.iloc[i] == period:
                        if pdf.NextInt.iloc[i] > 0:
                            lst.append(pdf.NextInt.iloc[i])
        return np.round(np.mean(lst), 2), np.round(np.std(lst), 2), len(lst)

    def upload_results_table(self, num_periods):
        dataframe = self.anchor(num_periods, vision=False)
        dataframe.to_csv(self.general_path + '/brendanvote_interval.csv')

if __name__ == "__main__":
    obj = Anchor('/brendanvote.csv', 'all', 1)
    obj.upload_results_table(24)