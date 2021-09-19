from DataSeparator import *
import matplotlib.pyplot as plt

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

    def plot_combinations(self):
        plt.rcdefaults()
        colrs = ['#03254c', '#1167b1', '#187bcd', '#2a9df4', '#d0efff']
        fig, ax = plt.subplots(figsize=(12, 8))
        comb_df = self.interval_combinations()
        combs = comb_df['comb']
        y_pos = np.arange(len(combs))
        interval_length = comb_df['count']
        ax.barh(y_pos, interval_length, align='center', color=colrs)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(combs)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Interval Pattern: Number of Occurrences', fontsize=18)
        plt.show()


if __name__ == "__main__":
    obj = Loading('all', '/ericmayer.csv')
    print(obj.interval_combinations())
