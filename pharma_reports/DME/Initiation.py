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
        initiation_list = []
        pdf_list = DataSeparator.patient_dataframes(self, drop_drug_na=True)
        for pdf in pdf_list:
            drugs = pdf.Drug.to_list()
            if len(drugs) > 0:
                initiation_list.append(drugs[0])
        return Counter(initiation_list), len(initiation_list)

    def initiation_steroid_vegf(self):
        antiVEGF_list = ['Lucentis', 'Eylea', 'Avastin', 'None']
        steroid_list = ['Ozurdex', 'Triesence', 'Kenalog', 'Kenacort', 'IVTA', 'None']
        avgf_count, steroid_count = 0, 0
        pdf_list = DataSeparator.patient_dataframes(self, drop_drug_na=True)
        for pdf in pdf_list:
            drugs = pdf.Drug.to_list()
            if len(drugs) > 0:
                if drugs[0] in antiVEGF_list: avgf_count+=1
                if drugs[0] in steroid_list: steroid_count+=1
        total = avgf_count + steroid_count
        return (avgf_count/total), (steroid_count/total)



if __name__ == "__main__":
    obj = Initiation('all', '/brendanvote.csv')
    print(obj.initiation_steroid_vegf())