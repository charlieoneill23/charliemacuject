class separator:
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
    
    def __init__(self, df_list):
        self.df_list = df_list
        
    def get_df(self, drop_drug_na=False):
        """
        Retrieves the specific dataset from the path.
        Input: Bool.
        Output: Pandas dataframe.
        """
        df = pd.read_csv(path)
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
        
    def drug_df_separator(self):
        """
        Produces a list of dataframes based single vs mult drugs.
        Input: self.
        Output: [Pandas dataframe].
        """
        df = self.get_df(drop_drug_na=True)
        df = df.dropna(subset=['Drug'])
        lucentis, eylea, avastin, mult = [], [], [], []
        drug_list = ['Lucentis', 'Eylea', 'Avastin']
        id_list = df['id'].unique()
        for eye in id_list:
            pdf = df[df['id'] == eye]
            drugs = pdf['Drug'].unique()
            if len(drugs) == 1:
                if drugs[0] == 'Lucentis':
                    lucentis.append(pdf)
                elif drugs[0] == 'Eylea':
                    eylea.append(pdf)
                else:
                    avastin.append(pdf)
            else:
                mult.append(pdf)
        return pd.concat(lucentis), pd.concat(eylea), pd.concat(mult)
    
    def steroid_df_separator(self):
        """
        Produces a list of dataframes based steroid, anti-VEGF or both.
        Input: self.
        Output: [Pandas dataframe].
        """
        df = self.get_df(drop_drug_na=True)
        df = df.dropna(subset=['Drug'])
        antiVEGF, steroid, Both = [], [], []
        antiVEGF_list = ['Lucentis', 'Eylea', 'Avastin']
        steroid_list = ['Ozurdex', 'Triesence', 'Kenalog', 'Kenacort', 'IVTA']
        id_list = df['id'].unique()
        for eye in id_list:
            pdf = df[df['id'] == eye]
            drugs = pdf['Drug'].unique()
            if len(pdf) > 1:
                if set(drugs).issubset(antiVEGF_list):
                    antiVEGF.append(pdf)
                elif set(drugs).issubset(steroid_list):
                    steroid.append(pdf)
                else:
                    Both.append(pdf)
        return pd.concat(antiVEGF), pd.concat(steroid), pd.concat(Both)
    
    def improved_df_separator(self):
        """
        Produces a list of dataframes based on improvement.
        Input: self.
        Output: [Pandas dataframe].
        """
        df = self.get_df()
        improved, not_improved = [], []
        id_list = df['id'].unique()
        for eye in id_list:
            pdf = df[df['id'] == eye]
            pdf.dropna(subset=['visual_acuity'], inplace=True)
            pdf.sort_values(by=['admission_date'], inplace=True)
            vision = pdf['visual_acuity'].to_list()
            if len(pdf) > 1:
                if max(vision) == vision[0]:
                    not_improved.append(pdf)
                else:
                    improved.append(pdf)
        return pd.concat(improved), pd.concat(not_improved), df
    
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