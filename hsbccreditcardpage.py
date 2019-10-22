import pandas as pd

from hsbcpage import HSBCPage


class HSBCCreditCardPage(HSBCPage):
    
    def _get_info_header_obj(self):
        info_header = "Your Transaction Details".replace(" ", "")
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == info_header:
                    return obj
            except:
                pass
        return None
    
    def _get_info_footer_obj(self):
        info_footer = "Summary Of Interest On This Statement".replace(" ", "")
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == info_footer:
                    return obj
            except:
                pass
        return None

    
    
    def _get_amount_margins(self):
        find_text = 'Amount'
        for obj in self.objs:
            if obj.get_text().strip() == find_text:
                return obj.x0-self.MARGIN, obj.x1+self.MARGIN

    def _get_transaction_date_margins(self):
        find_text = 'Transaction Date'
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == find_text.replace(" ", ""):
                    return obj.x0-self.MARGIN, obj.x1+2*self.MARGIN
            except:
                pass

    def _get_details_margins(self):
        find_text = 'Details'
        max_val, _ = self._get_amount_margins()
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == find_text.replace(" ", ""):
                    return obj.x0-self.MARGIN, max_val
            except:
                pass

    def _is_in_amount_column(self, obj):
        min_v, max_v = self._get_amount_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def _is_in_transaction_date_column(self, obj):
        min_v, max_v = self._get_transaction_date_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def _is_in_details_column(self, obj):
        min_v, max_v = self._get_details_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def get_data_lines(self):
        lines = {}
        for obj in self.objs:
            if self.y_min_val < obj.y0 < self.y_max_val:
                try:
                    if obj.y0 not in lines.keys():
                        lines[obj.y0] = []
                    lines[obj.y0].append(
                        {
                            'y': obj.y0,
                            'text': obj.get_text().strip(),
                            'is_amount': self._is_in_amount_column(obj),
                            'is_transaction_date': self._is_in_transaction_date_column(obj),
                            'is_details': self._is_in_details_column(obj),
                        }
                    )
                except:
                    pass
        return lines
    
    def get_data_table(self):
        table = []
        for lindex in self.lines:
            line = self.lines[lindex]
            table.append({
                'y': lindex, 
                'date': self.get_transaction_date(line),
                'amount': self.get_amount(line),
                'details': self.get_details(line),
            })
        return table
    
    def get_dataframe(self):
        if self.table:
            df = pd.DataFrame(self.table)
            if not df.empty:
                df = df.sort_values('y', ascending=False)
            return df
        return pd.DataFrame()
    
    @staticmethod
    def get_transaction_date(line):
        for item in line:
            if item['is_transaction_date']:
                return item['text']
        return None

    @staticmethod
    def get_amount(line):
        for item in line:
            if item['is_amount']:
                return item['text']
        return None

    @staticmethod
    def get_details(line):
        for item in line:
            if item['is_details']:
                return item['text']
        return None
   
    @property
    def objs(self):
        return self._objs
    
    @property
    def lines(self):
        return self._lines
    
    @property
    def table(self):
        return self._table
    
    @property
    def dataframe(self):
        return self._dataframe

    @property
    def y_min_val(self):
        return self._min_y_val
    
    @property
    def y_max_val(self):
        return self._max_y_val