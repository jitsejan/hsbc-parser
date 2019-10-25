from abc import ABCMeta, abstractmethod
from io import BytesIO
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal, LTLine
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser


from hsbcpage import HSBCPage
from hsbccreditcardpage import HSBCCreditCardPage


class HSBCPdfReader(metaclass=ABCMeta):
    
    def __init__(self, filename):
        self._filename = filename
        self._doc = self._get_doc()
        self._layouts = self._get_layouts()
        self._is_creditcard = self._is_creditcard_statement()

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
    
    def _is_creditcard_statement(self):
        """ Dirty check for creditcard statement """
        for obj in self.layouts[0]._objs:
            try:
                if 'Minimum payments'.replace(' ', '') == obj.get_text().replace(' ', '').strip():
                    return True
            except:
                pass
        return False

    def get_dataframe(self):
        df_list = []
        if self.is_creditcard:
            from hsbccreditcardpage import HSBCCreditCardPage as Page
        else:
            from hsbccurrentpage import HSBCCurrentPage as Page
        for layout in self.layouts:
            page = Page(layout)
            df_list.append(page.dataframe)
        df = pd.concat(df_list)
        return page.clean_frame(df)

    @property
    def doc(self):
        return self._doc
    
    @property
    def filename(self):
        return self._filename

    @property
    def is_creditcard(self):
        return self._is_creditcard

    @property
    def layouts(self):
        return self._layouts