import pandas as pd

from hsbccreditcardpage import HSBCCreditCardPage
from hsbcpdfreader import HSBCPdfReader

class HSBCCreditCardPdfReader(HSBCPdfReader):
    
    def get_dataframe(self):
        df_list = []
        for layout in self.layouts:
            page = HSBCCreditCardPage(layout)
            df_list.append(page.dataframe)
        df = pd.concat(df_list)
        df.dropna(subset=['details', 'date'], inplace=True)
        df['amount'] = df['amount'].ffill()
        df['amount'] = df['amount'].apply(self.get_amount)
        df = df.drop(['y'], axis=1)
        df['date'] = pd.to_datetime(df['date'])
        odf = df.groupby(['date', 'amount'])['details'].agg(lambda col: ' '.join(col)).to_frame()
        odf = odf.reset_index()
        odf['date'] = pd.to_datetime(odf['date'])
        return odf.sort_values('date')
        
    def get_amount(self, field):
        if isinstance(field, float):
            return float(field)*-1
        elif field.endswith('CR'):
            field = field.strip('CR')
            field = field.replace(',', '')
            return float(field)
        else:
            field = field.replace(',', '')
            return float(field)*-1
