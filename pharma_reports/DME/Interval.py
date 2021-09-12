from DataSeparator import *
import numpy as np
import pandas as pd
from datetime import date
import statistics
import warnings
warnings.filterwarnings('ignore')

class Interval(DataSeparator):
    """
    A class used to produce common interval metrics.

    ...

    Methods
    -------
    interval_column(self, patient_dataset)
        Produces a patient dataframe with additional column for interval length.
    interval_all(self, dataset)
        Applies interval column to entire dataframe.
    """

    def get_df_list(self): return DataSeparator.get_dataframes(self)

    def interval_column(self, pdf):
        '''
        Input: patient dataframe.
        Output: patient dataframe with additional column for interval length.
        '''
        pdf.dropna(subset=['admission_date'], inplace=True)
        pdf['admission_date'] = pd.to_datetime(pdf['admission_date'], dayfirst=True)
        pdf = pdf.sort_values(by=['admission_date'])
        dates = pdf['admission_date'].reset_index(drop=True)
        weeks = [0]
        for i in range(1, len(dates)):
            week = round((dates[i] - dates[i-1]).days / 7)
            weeks.append(week)
        pdf['Interval'] = weeks
        return pdf.reset_index(drop=True)

    def interval_all(self):
        '''
        Input: whole dataframe.
        Output: whole dataframe with additional column for interval length.
        '''
        df_list = self.get_df_list()
        new_list = []
        for df in df_list:
            id_list = df['id'].unique()
            frames = []
            for eye in id_list:
                pdf = df[df['id'] == eye]
                pdf = self.interval_column(pdf)
                frames.append(pdf)
            new_list.append(pd.concat(frames))
        return new_list

    def mean_intervals(self):
        """
        Returns the mean and std of interval length for different drugs.
        """
        df_list = self.interval_all()
        mean_list, std_list = [], []
        for df in df_list:
            int_list = df.Interval.to_list()
            int_list = [x for x in int_list if x > 0 and x < 20]
            mean_list.append(np.mean(int_list))
            std_list.append(np.std(int_list))
        return mean_list, std_list

    def ext_patterns(self):
        df_list = self.interval_all()
        df = df_list[-1]
        id_list = df.id.unique()
        inj_ext, inj_ext_time, actual_ext = [], [], []
        for eye in id_list:
            pdf = df[df.id == eye]
            pdf.admission_date = pd.to_datetime(pdf.admission_date, dayfirst=True)
            pdf.sort_values(by=['admission_date'], inplace=True)
            for i in range(len(pdf)-1):
                if pdf.Interval.iloc[i+1] > pdf.Interval.iloc[i] and i != 0:
                    inj_ext.append(i+1)
                    end = pd.to_datetime(pdf.admission_date.iloc[i+1], dayfirst=True)
                    start = pd.to_datetime(pdf.admission_date.iloc[0], dayfirst=True)
                    ext_time = (end - start).days / 7
                    inj_ext_time.append(ext_time)
                    actual_ext.append(pdf.Interval.iloc[i+1] - pdf.Interval.iloc[i])
                    break
        return inj_ext, inj_ext_time, actual_ext

    def red_patterns(self):
        df_list = self.interval_all()
        df = df_list[-1]
        id_list = df.id.unique()
        inj_ext, inj_ext_time, actual_red = [], [], []
        for eye in id_list:
            pdf = df[df.id == eye]
            pdf.admission_date = pd.to_datetime(pdf.admission_date, dayfirst=True)
            pdf.sort_values(by=['admission_date'], inplace=True)
            for i in range(len(pdf)-1):
                if pdf.Interval.iloc[i+1] < pdf.Interval.iloc[i] and i!=0:
                    inj_ext.append(i+1)
                    end = pd.to_datetime(pdf.admission_date.iloc[i+1], dayfirst=True)
                    start = pd.to_datetime(pdf.admission_date.iloc[0], dayfirst=True)
                    ext_time = (end - start).days / 7
                    inj_ext_time.append(ext_time)
                    actual_red.append(pdf.Interval.iloc[i] - pdf.Interval.iloc[i+1])
                    break
        return inj_ext, inj_ext_time, actual_red

    def results_table(self):
        """
        Returns a dataframe of results..
        Input: self.
        Output: Pandas dataframe.
        """
        names = ['aVGF', 'Steroid', 'Both(aVGF,Steroid)', 'Improved', 'Not_Improved', 'Overall']
        mean_list, std_list = self.mean_intervals()
        dict = {'Drug': names, 'mean_int': mean_list, 'mean_std': std_list}
        df = pd.DataFrame(dict)
        df.set_index('Drug', inplace=True)
        return df

    def ext_red_results(self):
        ext_red = ['Extension', 'Reduction']
        inj_ext, inj_ext_time, _ = self.ext_patterns()
        ext_mean, ext_mean_time = np.mean(inj_ext), np.mean(inj_ext_time)
        ext_median, ext_median_time = np.median(inj_ext), np.median(inj_ext_time)
        ext_min, ext_min_time = np.min(inj_ext), np.min(inj_ext_time)
        ext_max, ext_max_time = np.max(inj_ext), np.max(inj_ext_time)
        inj_red, inj_red_time, _ = self.red_patterns()
        red_mean, red_mean_time = np.mean(inj_red), np.mean(inj_red_time)
        red_median, red_median_time = np.median(inj_red), np.median(inj_red_time)
        red_min, red_min_time = np.min(inj_red), np.min(inj_red_time)
        red_max, red_max_time = np.max(inj_red), np.max(inj_red_time)
        dict = {'Type': ext_red, 'Mean': [ext_mean, red_mean], 'Median': [ext_median, red_median],
                'Min': [ext_min, red_min], 'Max': [ext_max, red_max],
                'MeanTime': [ext_mean_time, red_mean_time],
                'MedianTime': [ext_median_time, red_median_time],
                'MinTime': [ext_min_time, red_min_time], 'MaxTime': [ext_max_time, red_max_time]}
        df = pd.DataFrame(dict)
        df.set_index('Type', inplace=True)
        return df

    def upload_results_table(self):
        dataframe = self.results_table()
        dataframe.to_csv(general_path + '/drug_int_metrics.csv')
        df = self.ext_red_results()
        df.to_csv(general_path + '/interval_metrics.csv')
        interval_length = self.interval_distribution()
        interval_length.to_csv(general_path + '/interval_distribution.csv')
        int_dist = self.int_dist_plot()
        int_dist.to_csv(general_path + '/int_dist_plot.csv')

    def addYears(self, d, years):
        try:
            #Return same day of the current year
            return d.replace(year = d.year + years)
        except ValueError:
            #If not same day, it will return other, i.e.  February 29 to March 1 etc.
            return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


    def year_split(self, df):
        """
        Splits the dataframe into first, second and third year (onwards) of treatment.
        """
        id_list = df.id.unique()
        year_1, year_2, year_3 = [], [], []
        for eye in id_list:
            pdf = df[df.id == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            initial = pdf.admission_date.iloc[0]
            cutoff1 = self.addYears(initial, 1)
            cutoff2 = self.addYears(initial, 2)
            pdf_1 = pdf[pdf.admission_date <= cutoff1]
            pdf_2 = pdf[(pdf.admission_date > cutoff1) & (pdf.admission_date < cutoff2)]
            pdf_3 = pdf[pdf.admission_date > cutoff2]
            year_1.append(pdf_1), year_2.append(pdf_2), year_3.append(pdf_3)
        return pd.concat(year_1), pd.concat(year_2), pd.concat(year_3)

    def number_injections(self, df):
        """
        Returns the average number of injections per patient.
        """
        id_list = df.id.unique()
        injs = []
        for eye in id_list:
            pdf = df[df.id == eye]
            pdf.dropna(subset=['Drug'], inplace=True)
            pdf = pdf[(pdf.Drug != 'No Injection') & (pdf.Drug != 'None')]
            injs.append(len(pdf))
        return np.round(np.mean(injs), 2)


    def interval_distribution(self):
        """
        Requires: 'all' --> 'overall'
        Returns interval distribution statistics by year.
        """
        df_list = self.interval_all()
        df = df_list[-1]
        year_1, year_2, year_3 = self.year_split(df)
        int1, int2 = year_1.Interval.to_list(), year_2.Interval.to_list()
        int3 = year_3.Interval.to_list()
        mean1, mean2, mean3 = np.mean(int1), np.mean(int2), np.mean(int3)
        std1, std2, std3 = np.std(int1), np.std(int2), np.std(int3)
        mode1, mode2, mode3 = statistics.mode(int1), statistics.mode(int2), statistics.mode(int3)
        min1, min2, min3 = np.min(int1), np.min(int2), np.min(int3)
        max1, max2, max3 = np.max(int1), np.max(int2), np.max(int3)
        count1 = np.round(52/mean1, 2)
        count2 = np.round(52/mean2, 2)
        count3 = self.number_injections(year_3)
        dict = {'Year': ['Year1', 'Year2', '>Year3'], 'MeanInt': [mean1, mean2, mean3],
                'StdInt': [std1, std2, std3], 'ModeInt': [mode1, mode2, mode3],
                'MinInt': [min1, min2, min3], 'MaxInt': [max1, max2, max3],
                '#Injs': [count1, count2, count3]}
        df = pd.DataFrame(dict)
        df.set_index('Year', inplace=True)
        return df

    def int_dist_plot(self):
        """
        Requires: 'all' --> 'overall'
        Returns lists of interval distributions to plot.
        """
        df_list = self.interval_all()
        df = df_list[-1]
        year_1, year_2, year_3 = self.year_split(df)
        int1, int2 = year_1.Interval.to_list(), year_2.Interval.to_list()
        int3 = year_3.Interval.to_list()
        dist = int1 + int2 + int3
        len1 = ['Year1'] * len(int1)
        len2 = ['Year2'] * len(int2)
        len3 = ['Year3'] * len(int3)
        length = len1 + len2 + len3
        dict = {'IntervalDist': dist, 'Year': length}
        df = pd.DataFrame(dict)
        return df