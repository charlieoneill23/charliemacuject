from DataSeparator import *
from collections import Counter

class Initiation(DataSeparator):

    def __init__(self, df_list, csv_name):
        self.df_list = df_list
        self.csv_name = csv_name
        self.data_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/data/DME'
        self.doctor_path = self.data_path + self.csv_name
        self.general_path = '/Users/charlesoneill/DataspellProjects/charliemacuject/pharma_reports/DME'

    def initiation_drug(self):
        df_list = DataSeparator.get_dataframes(self)
        df = df_list[-1]
        id_list = df.id.unique()
        initiation_list = []
        for eye in id_list:
            pdf = df[df.id == eye]
            pdf.dropna(subset=['Drug'], inplace=True)
            pdf = pdf[(pdf.Drug != 'None') & (pdf.Drug != 'No Injection')]
            pdf = pdf[pdf.Drug != '0']
            drugs = pdf.Drug.to_list()
            if len(drugs) > 0:
                initiation_list.append(drugs[0])
        return Counter(initiation_list), len(initiation_list)

if __name__ == "__main__":
    obj = Initiation('all', '/devchau.csv')
    print(obj.initiation_drug())