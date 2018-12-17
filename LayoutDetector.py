from TableLayoutOrder import TableLayoutOrder
from table_info import TableInformation


class LayoutDetector:

    def __init__(self, filepath, metadata_path, meta_table_path):
        self.meta_table_path = meta_table_path
        self.filepath = filepath
        self.metadata_path = metadata_path
        self.info = TableInformation(self.filepath)
        self.info.show_table_info()
        self.layout = TableLayoutOrder(self.metadata_path, self.filepath)

    def probable_tables(self):
        return self.info.which_table(self.meta_table_path, self.metadata_path)

    def identify(self, check_table_data=False):
        #info = TableInformation(self.filepath)
        if check_table_data == False:
            print("Will not check the table metadata!")
            result = self.layout.check_ordered()
        else:
            tables = self.probable_tables()
            print(
                "Will check the table metadata! The tables that matches are : {}".format(tables))
            result = self.layout.check_ordered(tables)
        return result


'''
detector = LayoutDetector(r'G:\Siddhi\Office Personal\table_identifier\table1.csv',
                          r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv', r'G:\Siddhi\Office Personal\table_identifier\table_meta.csv')
'''
'''
# print(detector.probable_tables())
print(detector.identify(True))
'''
