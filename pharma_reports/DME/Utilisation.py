from DataSeparator import *
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class Utilisation(DataSeparator):

    def get_df(self): return DataSeparator.get_df(self)

    def drug_totals(self, num_visits, drug_name):
        df = self.get_df()
        eye_list = df['id'].unique()
        drugs_list, names_list = [], ['Lucentis', 'Avastin', 'Eylea']
        for eye in eye_list:
            count, df_new = 0, df[df['id'] == eye]
            if len(df_new) > num_visits:
                for i in range(len(df_new)):
                    while count < num_visits:
                        date = df_new['admission_date'].iloc[i]
                        drug = df_new['Drug'].iloc[i]
                        if drug in names_list:
                            drugs_list.append(drug)
                        count += 1
                        i += 1
        count_drug = drugs_list.count(drug_name)
        return count_drug

    # this function recurses over all patients in dataframe
    def all_drugs(self, visit_num, drug_name):
        df = self.get_df()
        counts = []
        for i in range(1, visit_num+1):
            average_drug = self.drug_totals(i, drug_name)
            counts.append(average_drug)
        return counts

    # plot the figures
    def plot_ut(self):
        w, y, z = self.all_drugs(100, 'Lucentis'), self.all_drugs(100, 'Eylea'), self.all_drugs(100, 'Avastin')
        matplotlib.rcParams['font.size'] = 18
        x = list(range(1, 101))
        fig = plt.figure(figsize=(12, 7))
        ax = plt.axes()
        ax.set(xlabel='Visit Number', ylabel='Number of Injections Using Drug')
        ax.plot(x, w, label='Lucentis', color='#03254c')
        ax.plot(x, y, label='Eylea', color='#187bcd')
        ax.plot(x, z, label='Avastin', color='orange')
        ax.legend(loc='lower left')
        right_side = ax.spines["right"]
        left_side = ax.spines['left']
        top_side = ax.spines['top']
        right_side.set_visible(False)
        left_side.set_visible(False)
        top_side.set_visible(False)
        plt.savefig('ut_plot.png', dpi=300, bbox_inches='tight')

    def avgf_steroids(self, num_visits, drug_name):
        pdf_list = DataSeparator.patient_dataframes(self)
        avgf_list = ['Lucentis', 'Avastin', 'Eylea']
        steroid_list = ['Ozurdex', 'Triesence', 'Kenalog', 'Kenacort', 'IVTA']
        drugs_list = []
        for pdf in pdf_list:
            count = 0
            if len(pdf) > num_visits:
                for i in range(len(pdf)):
                    while count < num_visits:
                        drug = pdf['Drug'].iloc[i]
                        if drug in avgf_list:
                            drugs_list.append('Anti-VEGF')
                        if drug in steroid_list:
                            drugs_list.append('Steroid')
                        count += 1
                        i += 1
        count_drug = drugs_list.count(drug_name)
        return count_drug

    def all_vgf_steroid(self, visit_num, drug_name):
        counts = []
        for i in range(1, visit_num+1):
            average_drug = self.avgf_steroids(i, drug_name)
            counts.append(average_drug)
        return counts

    def plot_avgf_steroid(self):
        w, y = self.all_vgf_steroid(100, 'Anti-VEGF'), self.all_vgf_steroid(100, 'Steroid')
        matplotlib.rcParams['font.size'] = 18
        x = list(range(1, 101))
        fig = plt.figure(figsize=(12, 7))
        ax = plt.axes()
        ax.set(xlabel='Visit Number', ylabel='Number of Injections Using Drug')
        ax.plot(x, w, label='Anti-VEGF', color='orange')
        ax.plot(x, y, label='Steroid', color='#187bcd')
        ax.legend(loc='lower left')
        right_side = ax.spines["right"]
        left_side = ax.spines['left']
        top_side = ax.spines['top']
        right_side.set_visible(False)
        left_side.set_visible(False)
        top_side.set_visible(False)
        plt.savefig('ut_plot.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    obj = Utilisation('all', '/devchau.csv')
    obj.plot_avgf_steroid()