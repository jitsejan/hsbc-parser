import pandas as pd

class HSBCPage:
    MARGIN = 15

    def __init__(self, layout):
        self._objs = layout._objs
        self._min_y_val = self._get_min_y_val()
        self._max_y_val = self._get_max_y_val()
        self._lines = self.get_data_lines()
        self._table = self.get_data_table()
        self._dataframe = self.get_dataframe()
        
    def _get_info_header_obj(self):
        info_header = "Date".replace(" ", "")
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == info_header:
                    return obj
            except:
                pass
        return None
    
    def _get_info_footer_obj(self):
        info_footer = "Information about the Financial Services Compensation Scheme".replace(" ", "")
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == info_footer:
                    return obj
            except:
                pass
        return None

    def _get_min_y_val(self):
        footer = self._get_info_footer_obj()
        return footer.y0 if footer else 0
        
    def _get_max_y_val(self):
        header = self._get_info_header_obj()
        return header.y0 if header else 0
    
    def _get_balance_margins(self):
        find_text = 'Balance'
        for obj in self.objs:
            if obj.get_text().strip() == find_text:
                return obj.x0-self.MARGIN, obj.x1+self.MARGIN

    def _get_paid_in_margins(self):
        find_text = 'Paidin'
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == find_text.replace(" ", ""):
                    return obj.x0-self.MARGIN, obj.x1+self.MARGIN
            except:
                pass

    def _get_paid_out_margins(self):
        find_text = 'Paidout'
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == find_text.replace(" ", ""):
                    return obj.x0-self.MARGIN, obj.x1+self.MARGIN
            except:
                pass

    def _get_date_margins(self):
        find_text = 'Date'
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == find_text.replace(" ", ""):
                    return obj.x0-self.MARGIN, obj.x1+2*self.MARGIN
            except:
                pass

    def _get_payment_type_margins(self):
        find_text = 'Payment'
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == find_text.replace(" ", ""):
                    return obj.x0-self.MARGIN, obj.x0+self.MARGIN
            except:
                pass     

    def _get_payment_description_margins(self):
        find_text = 'Payment'
        for obj in self.objs:
            try:
                if obj.get_text().strip().replace(" ", "") == find_text.replace(" ", ""):
                    return obj.x0+self.MARGIN, obj.x0+200
            except:
                pass

    def _is_in_date_column(self, obj):
        min_v, max_v = self._get_date_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def _is_in_payment_type_column(self, obj):
        min_v, max_v = self._get_payment_type_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def _is_in_payment_description_column(self, obj):
        min_v, max_v = self._get_payment_description_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def _is_in_balance_column(self, obj):
        min_v, max_v = self._get_balance_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def _is_in_paid_in_column(self, obj):
        min_v, max_v = self._get_paid_in_margins()
        return obj.x0 > min_v and obj.x1 < max_v

    def _is_in_paid_out_column(self, obj):
        min_v, max_v = self._get_paid_out_margins()
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
                            'is_date': self._is_in_date_column(obj),
                            'is_payment_type': self._is_in_payment_type_column(obj),
                            'is_payment_description': self._is_in_payment_description_column(obj),
                            'is_balance': self._is_in_balance_column(obj),
                            'is_paid_in': self._is_in_paid_in_column(obj),
                            'is_paid_out': self._is_in_paid_out_column(obj),
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
                'date': self.get_date(line),
                'payment_type': self.get_payment_type(line),
                'payment_description': self.get_payment_description(line),
                'paid_out': self.get_paid_out(line),
                'paid_in': self.get_paid_in(line),
                'balance': self.get_balance(line),
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
    def get_date(line):
        for item in line:
            if item['is_date']:
                return item['text']
        return None

    @staticmethod
    def get_payment_type(line):
        for item in line:
            if item['is_payment_type']:
                return item['text']
        return None

    @staticmethod
    def get_payment_description(line):
        for item in line:
            if item['is_payment_description']:
                return item['text']
        return None

    @staticmethod
    def get_paid_in(line):
        for item in line:
            if item['is_paid_in']:
                return item['text']
        return None

    @staticmethod
    def get_paid_out(line):
        for item in line:
            if item['is_paid_out']:
                return item['text']
        return None

    @staticmethod
    def get_balance(line):
        for item in line:
            if item['is_balance']:
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