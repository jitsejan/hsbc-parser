import pandas as pd

from hsbcpage import HSBCPage

class HSBCPdfReader:
    
    def __init__(self, filename):
        self._filename = filename
        self._doc = self._get_doc()
        self._layouts = self._get_layouts()
    
    def get_dataframe(self):
        df_list = []
        for layout in self.layouts:
            page = HSBCPage(layout)
            df_list.append(page.dataframe)
        df = pd.concat(df_list)
        df['date'] = df['date'].ffill()
        df.dropna(subset=['payment_description', 'date'], inplace=True)
        df['paid_in'] = df['paid_in'].str.replace(',', '').astype('float') 
        df['paid_out'] = df['paid_out'].str.replace(',', '').astype('float')
        df['balance'] = df['balance'].str.replace(',', '').astype('float')
        df = df.drop(['y'], axis=1)
        df['amount'] = df['paid_in'].fillna(df['paid_out']*-1)
        df['amount'] = df['amount'].bfill()
        df = df[~df['payment_description'].isin(['BALANCE CARRIED FORWARD', 'BALANCE BROUGHT FORWARD', '.'])]
        odf = df.groupby(['date', 'amount'])['payment_description'].agg(lambda col: ' '.join(col)).to_frame()
        odf = odf.reset_index()
        odf['date'] = pd.to_datetime(odf['date'])
        return odf.sort_values('date')
        
    def _get_doc(self):
        cstr = BytesIO()
        with open(self.filename, 'rb') as fp:
            cstr.write(fp.read())
        cstr.seek(0)
        return PDFDocument(PDFParser(cstr))

    def _get_layouts(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(line_margin=0.000001, char_margin=1)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        layouts = list()
        for page in PDFPage.create_pages(self.doc):
            interpreter.process_page(page)
            layout = device.get_result()
            layouts.append(layout)

        return layouts
    
    @property
    def doc(self):
        return self._doc
    
    @property
    def filename(self):
        return self._filename
    
    @property
    def layouts(self):
        return self._layouts