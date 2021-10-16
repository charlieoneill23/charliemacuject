from DataSeparator import *
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import date
import statistics
import statsmodels.stats.api as sms
import warnings
warnings.filterwarnings('ignore')

class Vision(DataSeparator):
    """
    A class used to produce common visual metrics.

    ...

    Attributes
    ----------
    df_list : str
        a formatted string to determine subset of patients being analysed
        options:
            - 'drugs': segment patients by those on single vs mult drugs
            - 'improved': segment patients by those who improved vs didn't
            - 'switched': segment patients by switches (L to E, E to L only)
            - 'all': segment by all of the above

    Methods
    -------
    pvi(self, dataset)
        Produces a list of patient PVIs from dataset.
    tpvi(self, dataset)
        Produces a list of patient TPVIs from dataset.
    vlp(self, dataset)
        Produces a list of patient VLPs from dataset.
    ovc(self, dataset)
        Produces a list of patient OVCs from dataset.
    vision_weeks(self, weeks)
        Calculates the mean vision for all patients at a specific visit number.
    anchor(self, weeks)
        Produces a dataframe of mean vision over the first year, including trial results.
    list_results(self, dataset)
        Produces a list of above visual metrics (PVI, TPVI, VLP, OVC) for given dataset.
    list_sds(self, dataset)
        Produces a list of the 95% CI bounds for all visual metrics, for given dataset.
    results_table(self)
        Returns a Pandas dataframe of all visual metrics.
    """

    # df_list can be either drugs, improved, switched or all
    def __init__(self, df_list, csv_name):
        self.df_list = df_list
        self.csv_name = csv_name
        self.data_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/data/DME'
        self.doctor_path = self.data_path + self.csv_name
        self.general_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/DME'

    def pvi(self, df):
        """
        Produces a list of patient PVIs from dataset.
        Peak Visual Improvement (PVI) is defined as max vision minus initial vision.
        Input: Pandas dataframe.
        Output: list of LogMAR letters.
        """
        id_list = df['id'].unique()
        pvi_list = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            visions = pdf['visual_acuity'].to_list()
            if len(visions) > 0:
                pvi_pdf = max(visions) - visions[0]
                pvi_list.append(pvi_pdf)
        return pvi_list

    def tpvi(self, df):
        """
        Produces a list of patient TPVIs from dataset.
        Time to Peak Visual Improvement (TPVI) is defined in days.
        Input: Pandas dataframe.
        Output: list of days.
        """
        id_list = df['id'].unique()
        tpvi_list = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.admission_date = pd.to_datetime(pdf.admission_date, dayfirst=True)
            pdf.sort_values(by=['admission_date'], inplace=True)
            dates = pdf['admission_date'].to_list()
            initial_date = dates[0]
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            visions = pdf['visual_acuity'].to_list()
            ndf = pdf[pdf['visual_acuity'] == max(visions)]
            new_dates = ndf['admission_date'].to_list()
            time = (new_dates[0] - initial_date).days
            tpvi_list.append(time)
        return tpvi_list

    def tpvi_injs(self, df):
        """
        Produces a list of patient TPVIs (in # of injs) from dataset.
        Input: Pandas dataframe.
        Output: list of days.
        """
        id_list = df['id'].unique()
        tpvi_list = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            visions = pdf['visual_acuity'].to_list()
            max_value = max(visions)
            max_index = visions.index(max_value)
            tpvi_list.append(max_index)
        return tpvi_list

    def ovc(self, df):
        """
        Produces a list of patient OVCs from dataset.
        Overall Visual Change (OVC) is defined as last vision minus initial vision.
        Input: Pandas dataframe.
        Output: list of LogMAR letters.
        """
        id_list = df['id'].unique()
        ovc_list = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            visions = pdf['visual_acuity'].to_list()
            ovc_list.append(visions[-1] - visions[0])
        return ovc_list

    def vlp(self, df):
        """
        Produces a list of patient VLPs from dataset.
        Vision Loss from Peak (VLP) is defined as max vision minus last vision.
        Input: Pandas dataframe.
        Output: list of LogMAR letters.
        """
        id_list = df['id'].unique()
        vlp_list = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            visions = pdf['visual_acuity'].to_list()
            recent = visions[-1]
            max_vision = max(visions)
            vlp_list.append(max_vision - recent)
        return vlp_list

    def baseline(self, df):
        id_list = df.id.unique()
        baseline_list = []
        for eye in id_list:
            pdf = df[df.id == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            if pdf.visual_acuity.iloc[0] != 0:
                baseline_list.append(pdf.visual_acuity.iloc[0])
        return baseline_list

    def list_results(self, df):
        """
        Produces a list of the visual metrics defined (PVI, TPVI, VLP, OVC).
        Input: Pandas dataframe.
        Output: float x 4.
        """
        pvi_list, tpvi_list, tpvi_injs_list = self.pvi(df), self.tpvi(df), self.tpvi_injs(df),
        vlp_list, ovc_list = self.vlp(df), self.ovc(df)
        baseline_list = self.baseline(df)
        return np.mean(pvi_list), np.mean(tpvi_list), np.mean(tpvi_injs_list), np.mean(vlp_list), np.mean(ovc_list), np.mean(baseline_list)

    def list_sds(self, df):
        """
        Produces a list of the 95% CI bounds for all visual metrics.
        Input: Pandas dataframe.
        Output: float x 4
        """
        pvi_list, tpvi_list, tpvi_injs_list = self.pvi(df), self.tpvi(df), self.tpvi_injs(df),
        vlp_list, ovc_list, baseline_list = self.vlp(df), self.ovc(df), self.baseline(df)
        lst = [pvi_list, tpvi_list, tpvi_injs_list, vlp_list, ovc_list, baseline_list]
        to_return = []
        for item in lst:
            ci = stats.t.interval(alpha=0.95, df=len(item)-1, loc=np.mean(item), scale=stats.sem(item))
            std = np.mean(item) - ci[0]
            to_return.append(std)
        return np.round(to_return[0], 2), np.round(to_return[1], 2), np.round(to_return[2], 2), np.round(to_return[3], 2), np.round(to_return[4], 2), np.round(to_return[5], 2)

    def mean_vis(self, df):
        id_list = df['id'].unique()
        mean_list = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            visions = pdf['visual_acuity'].to_list()
            mean_list.append(np.mean(visions))
        return mean_list

    def std_vis(self, df):
        id_list = df['id'].unique()
        std_list = []
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            visions = pdf['visual_acuity'].to_list()
            std_list.append(np.std(visions))
        return std_list

    def results_table(self):
        """
        Returns a dataframe of results for all visual metrics.
        Input: self.
        Output: Pandas dataframe.
        """
        names = ['aVGF', 'Steroid', 'Both(aVGF,Steroid)', 'Improved', 'Not_Improved', 'Overall']
        df_lst = DataSeparator.get_dataframes(self)
        pvi, tpvi, tpvi_i, vlp, ovc, pvi_sd, tpvi_sd, tpvi_i_sd = [], [], [], [], [], [], [], [],
        vlp_sd, ovc_sd, mean_vis, vis_std, base, base_sd = [], [], [], [], [], []
        for i in range(len(df_lst)):
            dataframe = df_lst[i]
            name = names[i]
            Pvi, Tpvi, Tpvi_I, Vlp, Ovc, Base = self.list_results(dataframe)
            Pvi_sd, Tpvi_sd, Tpvi_I_sd, Vlp_sd, Ovc_sd, Base_sd = self.list_sds(dataframe)
            mean_vision = np.mean(self.mean_vis(dataframe))
            vision_std = np.mean(self.std_vis(dataframe))
            pvi.append(Pvi), tpvi.append(Tpvi), tpvi_i.append(Tpvi_I), vlp.append(Vlp), ovc.append(Ovc)
            pvi_sd.append(Pvi_sd), tpvi_sd.append(Tpvi_sd), tpvi_i_sd.append(Tpvi_I_sd), vlp_sd.append(Vlp_sd)
            ovc_sd.append(Ovc_sd), mean_vis.append(mean_vision), vis_std.append(vision_std)
            base.append(Base), base_sd.append(Base_sd)
        dict = {'Drug': names, 'PVI': pvi, 'PVI_sd': pvi_sd, 'TPVI': tpvi, 'TPVI_sd': tpvi_sd, 'TPVI_Injs': tpvi_i,
                'TPVI_Injs_sd': tpvi_i_sd, 'VLP': vlp, 'VLP_sd': vlp_sd, 'OVC': ovc, 'OVC_sd': ovc_sd,
                'MeanVis': mean_vis, 'StdVis': vis_std, 'Baseline': base, 'Baseline_sd': base_sd}
        df = pd.DataFrame(dict)
        df.set_index('Drug', inplace=True)
        return df

    def upload_results_table(self):
        dataframe = self.results_table()
        dataframe.to_csv(general_path + '/visual_metrics.csv')
        drug_dist = self.va_dist_table()
        drug_dist.to_csv(general_path + '/drug_dist_table.csv')
        va_dist = self.va_distributions()
        va_dist.to_csv(general_path + '/va_distributions.csv')

    def patient_counts(self):
        df_list = DataSeparator.get_dataframes(self)
        counts = []
        for df in df_list:
            counts.append(len(df.id.unique()))
        return counts

    def va_distributions(self):
        """
        Outputs a list for each type of patient of VAs.
        This allows us to analyse the distribution of vision.
        """
        df_list = DataSeparator.get_dataframes(self)
        luc_lst = self.va_dist_helper(df_list[0])
        eyl_lst = self.va_dist_helper(df_list[1])
        m_lst = self.va_dist_helper(df_list[2])
        dictDF = {'aVGF_Dist': pd.Series(luc_lst), 'Steroid_Dist': pd.Series(eyl_lst),
                'Both_dist': pd.Series(m_lst)}
        return pd.DataFrame(dictDF)


    def va_dist_helper(self, df):
        id_list = df.id.unique()
        lst = []
        for eye in id_list:
            pdf = df[df.id == eye]
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            lst.append(np.mean(pdf.visual_acuity))
        return lst

    def va_dist_table(self):
        """
        Outputs a table of distribution of VAs.
        This allows us to analyse the distribution of vision.
        """
        df_list = DataSeparator.get_dataframes(self)
        luc_list = self.va_dist_helper(df_list[0])
        eyl_list = self.va_dist_helper(df_list[1])
        m_list = self.va_dist_helper(df_list[2])
        names = ['aVGF', 'Steroid', 'Both']
        means = [np.mean(luc_list), np.mean(eyl_list), np.mean(m_list)]
        medians = [np.median(luc_list), np.median(eyl_list), np.median(m_list)]
        stds = [np.std(luc_list), np.std(eyl_list), np.std(m_list)]
        maxs = [max(luc_list), max(eyl_list), max(m_list)]
        mins = [min(luc_list), min(eyl_list), min(m_list)]
        dict = {'Drug': names, 'Mean': means, 'Median': medians,
                'StandardDev': stds, 'Maximum': maxs, 'Minimum': mins}
        df = pd.DataFrame(dict)
        df.set_index('Drug', inplace=True)
        return df


if __name__ == "__main__":
    #unittest.main()
    obj = Vision('all', '/ericmayer.csv')
    df = obj.get_df()
    tpvi_list = obj.tpvi(df)
    ci = sms.DescrStatsW(tpvi_list).tconfint_mean()
    print(np.mean(tpvi_list), (ci[1]-ci[0])/2)
    tpvi_injs = obj.tpvi_injs(df)
    ci2 = sms.DescrStatsW(tpvi_injs).tconfint_mean()
    print(np.mean(tpvi_injs), (ci2[1]-ci2[0])/2)