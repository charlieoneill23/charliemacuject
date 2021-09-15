import unittest

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import date
import statistics
import warnings

warnings.filterwarnings('ignore')

data_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/data/DME'
doctor_path = data_path + '/devchau.csv'
general_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/DME'


class DataSeparator:
    """
    A class used to segment the dataset in different ways.

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
    get_df(self, drop_drug_na=False)
        Retrieves the specific dataset from the path.
        'drop_drug_na=True' will remove NAs and Brolucizumab from 'Drug' column.
    get_dataframes(self)
        Produces a list of dataframes based on df_list segmentation query.
    drug_df_separator(self)
        Segments the dataset by patients on single vs mult drugs.
    steroids_df_separator(self)
        Segments the dataset by patients on steroids, anti-VEGF or both.
    improved_df_separator(self)
        Segments the dataset by patients who improved vs didn't.
    switch_df_separator(self)
        Segments the dataset by patients who switched.
        Lucentis to Eylea, Eylea to Lucentis switches only.
    """

    def __init__(self, df_list, csv_name):
        self.df_list = df_list
        self.csv_name = csv_name
        self.data_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/data/DME'
        self.doctor_path = self.data_path + self.csv_name
        self.general_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/DME'

    def get_df(self, drop_drug_na=False):
        """
        Retrieves the specific dataset from the path.
        Input: Bool.
        Output: Pandas dataframe.
        """
        df = pd.read_csv(self.doctor_path)
        df.dropna(subset=['visual_acuity'], inplace=True)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        df.rename(columns={'CreatedDate': 'admission_date', 'InjToday': 'Drug'}, inplace=True)
        df['admission_date'] = pd.to_datetime(df['admission_date'], dayfirst=True)
        if drop_drug_na:
            df = df.dropna(subset=['Drug'])
            df = df[df['Drug'] != 'nil']
            df = df[df['Drug'] != 'None']
            df = df[df['Drug'] != 'Brolucizumab']
        return df

    def patient_dataframes(self, drop_drug_na=False):
        df_list = self.get_dataframes()
        df = df_list[-1]
        id_list = df.id.unique()
        pdf_list = []
        for eye in id_list:
            pdf = df[df.id == eye]
            if len(pdf) > 0:
                if drop_drug_na:
                    pdf.dropna(subset=['Drug'], inplace=True)
                    pdf = pdf[(pdf.Drug != 'None') & (pdf.Drug != 'No Injection')]
                    pdf = pdf[pdf.Drug != '0']
                    pdf_list.append(pdf)
                else: pdf._list.append(pdf)
        return pdf_list

    def get_dataframes(self):
        """
        Produces a list of dataframes based on df_list segmentation query.
        Input: self.
        Output: [Pandas dataframe].
        """
        if self.df_list == 'drugs':
            aVGF_df, steroid_df, both_df = self.drug_df_separator()
            return [aVGF_df, steroid_df, both_df]
        elif self.df_list == 'switched':
            luc_eyl, eyl_luc = self.switch_df_separator()
            luc_eyl
            return [luc_eyl, eyl_luc]
        elif self.df_list == 'improved':
            improved, not_improved, overall = self.improved_df_separator()
            return [improved, not_improved, overall]
        elif self.df_list == 'all':
            avgf_df, steroid_df, both_df = self.steroid_df_separator()
            improved, not_improved, overall = self.improved_df_separator()
            return [avgf_df, steroid_df, both_df, improved, not_improved, overall]
        else:
            return [self.get_df()]

    def drug_df_separator(self):
        """
        Produces a list of dataframes based single vs mult drugs.
        Input: self.
        Output: [Pandas dataframe].
        """
        df = self.get_df()
        lucentis, eylea, mult = [], [], []
        lucentis_list = ['Lucentis', '0', 'None']
        eylea_list = ['Eylea', '0', 'None']
        id_list = df['id'].unique()
        for eye in id_list:
            pdf = df[df['id'] == eye]
            ndf = pdf[pdf['Drug'] != '0']
            ndf = ndf.dropna(subset=['Drug'])
            drugs = ndf['Drug'].unique()
            if len(pdf) > 1:
                if set(drugs).issubset(lucentis_list):
                    lucentis.append(pdf)
                elif set(drugs).issubset(eylea_list):
                    eylea.append(pdf)
                else:
                    mult.append(pdf)
        if len(eylea) == 0:
            eyl2 = pd.read_csv(self.general_path+'/dummypatient.csv')
            eyl2 = eyl2.iloc[[0]]
            return pd.concat(lucentis), eyl2, pd.concat(mult)
        return pd.concat(lucentis), pd.concat(eylea), pd.concat(mult)

    def steroid_df_separator(self):
        """
        Produces a list of dataframes based steroid, anti-VEGF or both.
        Input: self.
        Output: [Pandas dataframe].
        """
        df = self.get_df()
        antiVEGF, steroid, Both = [], [], []
        antiVEGF_list = ['Lucentis', 'Eylea', 'Avastin', 'None']
        steroid_list = ['Ozurdex', 'Triesence', 'Kenalog', 'Kenacort', 'IVTA', 'None']
        id_list = df['id'].unique()
        for eye in id_list:
            pdf = df[df['id'] == eye]
            ndf = pdf[pdf['Drug'] != '0']
            ndf = ndf.dropna(subset=['Drug'])
            drugs = ndf['Drug'].unique()
            if len(pdf) > 1:
                if set(drugs).issubset(antiVEGF_list):
                    antiVEGF.append(pdf)
                elif set(drugs).issubset(steroid_list):
                    steroid.append(pdf)
                else:
                    Both.append(pdf)
        if len(steroid) == 0:
            steroid2 = pd.read_csv(self.general_path+'/dummypatient.csv')
            steroid2 = steroid2.iloc[[0]]
            if len(Both) == 0:
                both2 = pd.read_csv(self.general_path+'/dummypatient.csv')
                both2 = both2.iloc[[0]]
                return pd.concat(antiVEGF), steroid2, both2
            else:
                return pd.concat(antiVEGF), steroid2, pd.concat(Both)
        else:
            return pd.concat(antiVEGF), pd.concat(steroid), pd.concat(Both)

    def improved_df_separator(self):
        """
        Produces a list of dataframes based on improvement.
        Input: self.
        Output: [Pandas dataframe].
        """
        df = self.get_df()
        improved, not_improved, overall = [], [], []
        id_list = df['id'].unique()
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.sort_values(by=['admission_date'], inplace=True)
            vision = pdf['visual_acuity'].to_list()
            if len(pdf) > 1:
                overall.append(pdf)
                if max(vision) == vision[0]:
                    not_improved.append(pdf)
                else:
                    improved.append(pdf)
        return pd.concat(improved), pd.concat(not_improved), pd.concat(overall)

    def switch_df_separator(self):
        """
        Produces a list of dataframes based on switches.
        Input: self.
        Output: [Pandas dataframe].
        """
        df = self.get_df(drop_drug_na=True)
        df = df[df['Drug'] != 'Avastin']
        luc_eyl, eyl_luc = [], []
        drug_list = ['Lucentis', 'Eylea']
        id_list = df['id'].unique()
        for eye in id_list:
            pdf = df[df['id'] == eye]
            drugs = pdf['Drug'].unique()
            if len(drugs) > 1:
                if drugs[0] == 'Lucentis' and drugs[1] == 'Eylea':
                    luc_eyl.append(pdf)
                elif drugs[0] == 'Eylea' and drugs[1] == 'Lucentis':
                    eyl_luc.append(pdf)
            else:
                pass
        return pd.concat(luc_eyl), pd.concat(eyl_luc)


class DataSeparatorTest(unittest.TestCase):
    def setUp(self):
        import warnings
        warnings.filterwarnings('ignore')

    def test_improved(self):
        """
        Testing set(improved + not_improved) = overall dataset
        """
        self.setUp()
        doctors = ['/alextan.csv','/devchau.csv','/devchau_bor.csv','/ericmayer.csv','/brendanvote.csv']
        for doctor in doctors:
            obj = DataSeparator('all', doctor)
            a,b,c = obj.improved_df_separator()
            self.assertEqual(len(a) + len(b), len(c))

    def test_drugs(self):
        """
        Testing set(Lucentis + Eylea + Multiple) = overall dataset
        """
        self.setUp()
        doctors = ['/alextan.csv','/devchau.csv','/devchau_bor.csv','/ericmayer.csv','/brendanvote.csv']
        for doctor in doctors:
            obj = DataSeparator('all', doctor)
            x,y,z = obj.drug_df_separator()
            _,_,overall = obj.improved_df_separator()
            a = len(x) + len(y) + len(z)
            b = len(overall)
            self.assertLess(abs(a-b), 2)

    def test_steroid(self):
        """
        Testing set(steroid + aVGF + both) = overall dataset
        """
        self.setUp()
        doctors = ['/alextan.csv','/devchau.csv','/devchau_bor.csv','/ericmayer.csv','/brendanvote.csv']
        for doctor in doctors:
            obj = DataSeparator('all', doctor)
            x,y,z = obj.steroid_df_separator()
            _,_,overall = obj.improved_df_separator()
            if len(x) > 1 and len(y) > 1 and len(z) > 1:
                a = len(x) + len(y) + len(z)
                b = len(overall)
                self.assertLess(abs(a-b), 2)

    def test_overall(self):
        """
        Testing set(steroid + aVGF + both) = set(Lucentis + Eylea + Multiple)
        """
        self.setUp()
        doctors = ['/alextan.csv','/devchau.csv','/devchau_bor.csv','/ericmayer.csv','/brendanvote.csv']
        for doctor in doctors:
            obj = DataSeparator('all', doctor)
            x,y,z = obj.steroid_df_separator()
            h,i,j = obj.drug_df_separator()
            if len(x) > 1 and len(y) > 1 and len(z) > 1:
                a = len(x) + len(y) + len(z)
                b = len(h) + len(i) + len(j)
                self.assertLess(abs(a-b), 2)


if __name__ == '__main__':
    unittest.main()
