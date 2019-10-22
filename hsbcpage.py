from abc import ABCMeta, abstractmethod

class HSBCPage(metaclass=ABCMeta):
    MARGIN = 15

    def __init__(self, layout):
        self._objs = layout._objs
        self._min_y_val = self._get_min_y_val()
        self._max_y_val = self._get_max_y_val()
        self._lines = self.get_data_lines()
        self._table = self.get_data_table()
        self._dataframe = self.get_dataframe()

    def _get_min_y_val(self):
        """ Get bottom limit """
        footer = self._get_info_footer_obj()
        return footer.y0 if footer else 0
        
    def _get_max_y_val(self):
        """ Get top limit """
        header = self._get_info_header_obj()
        return header.y0 - self.MARGIN if header else 0

    @abstractmethod
    def _get_info_header_obj(self):
        pass
    
    @abstractmethod
    def _get_info_footer_obj(self):
        pass