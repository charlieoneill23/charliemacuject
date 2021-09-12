from DataSeparator import *
import math
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class Anchor(DataSeparator):

    def __init__(self, subset, interval):
        super().__init__(subset)
        self.interval = interval


    def month_column(self, pdf, interval):
        """
        Appends month since starting as a column to patient df.
        Interval is the grouping of months i.e. 3 = 3 month intervals.
        Interval = 12 --> yearly intervals.
        """
        pdf.sort_values(by=['admission_date'], inplace=True)
        visions = pdf['visual_acuity'].to_list()
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
        df = DataSeparator.get_df(self)
        id_list = df['id'].unique()
        df.dropna(subset=['visual_acuity'], inplace=True)
        lst = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.admisssion_date = pd.to_datetime(pdf.admission_date, dayfirst=True)
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf = self.month_column(pdf, interval)
            visions = pdf['visual_acuity'].to_list()
            for i in range(len(pdf)):
                if pdf.period_since_start.iloc[i] == period:
                    if pdf.visual_acuity.iloc[i] > 0:
                        lst.append(visions[i] - visions[0])
        return np.round(np.mean(lst), 2), np.round(np.std(lst), 2), len(lst)

    def anchor(self):
        """
        Produces a dataframe of mean vision over the first year, including trial results.
        Also produces the standard ANCHOR figures for the same period.
        Input: Pandas dataframe (all patients).
        Output: Pandas dataframe.
        """
        df_list = DataSeparator.get_dataframes(self)
        df = df_list[-1]
        anchor_list = [0]
        std_list = [0]
        length_list = [0]
        months = [x for x in range(13)]
        for i in range(12):
            mean, std, length = self.vision_month(i, self.interval)
            anchor_list.append(mean)
            std_list.append(std)
            length_list.append(length)
        period_string = str(self.interval)
        dict = {'Period('+period_string+'monthInts)': months, 'Doctor_Mean': anchor_list,
                'StdDeviation': std_list, 'No.Visits': length_list}
        df = pd.DataFrame(dict)
        df.set_index('Period('+period_string+'monthInts)', inplace=True)
        return df

    def upload_results_table(self):
        dataframe = self.anchor()
        dataframe.to_csv(general_path + '/anchor.csv')