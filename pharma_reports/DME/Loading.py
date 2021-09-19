from DataSeparator import *

class Loading(DataSeparator):

    def interval_combinations(self):
        pdf_list = DataSeparator.patient_dataframes(self)
        interval_list = []
        for pdf in pdf_list:
            pdf.dropna(subset=['NextInt'], inplace=True)
            pdf = pdf[pdf.NextInt < 13]
            if len(pdf) > 4:
                interval = []
                for i in range(4):
                    interval.append(pdf.NextInt.iloc[i])
                interval_list.append(interval)
        interval_set = [list(x) for x in set(tuple(x) for x in interval_list)]
        count, comb = [], []
        for i in interval_set:
            if interval_list.count(i) > 5:
                count.append(interval_list.count(i))
                comb.append(i)
        comb_df = pd.DataFrame({'count': count,'comb': comb})
        comb_df = comb_df.sort_values('count', ascending=False)
        return comb_df

if __name__ == "__main__":
    obj = Loading('all', '/devchau.csv')
    print(obj.interval_combinations())
