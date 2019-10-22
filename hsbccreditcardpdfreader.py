from io import BytesIO
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal, LTLine
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser


from hsbccreditcardpage import HSBCCreditCardPage

class HSBCCreditCardPdfReader:
    
    def __init__(self, filename):
        self._filename = filename
        self._doc = self._get_doc()
        self._layouts = self._get_layouts()
    
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

    @property
    def doc(self):
        return self._doc
    
    @property
    def filename(self):
        return self._filename
    
    @property
    def layouts(self):
        return self._layouts