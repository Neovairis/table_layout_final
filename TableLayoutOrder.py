from tableschema import Table
import pandas as pd
import numpy as np
from table_info import TableInformation
import csv


class TableLayoutOrder:
    '''
    Find the table using the order of the datatypes
    '''

    def __init__(self, meta_field_path, filepath):
        self.meta_field_path = meta_field_path
        self.filepath = filepath
        self.table = Table(self.filepath)
        self.meta_field = pd.read_csv(self.meta_field_path)

    def get_input_array(self):
        input_table_arr = []
        for i, value in enumerate(self.table.infer()['fields']):
            val = str(value['type']+str(i+1))
            input_table_arr.append(val)
        return input_table_arr

    def check_name(self):
        print(self.filepath)
        info = TableInformation(self.filepath)
        deli = info.show_delimeter()
        with open(self.filepath, ) as f:
            reader = csv.reader(f, delimiter=deli)
            line = next(reader)
        unique_tables = self.meta_field['TableName'].unique()
        print('sss', unique_tables)
        array_name = []
        for i in unique_tables:
            temp = self.meta_field.loc[self.meta_field["TableName"] == i]
            if np.array_equal(sorted(line), sorted(temp["fields"].values)) == True:
                array_name.append(i)
            # print(temp["fields"].values)
        return array_name

    def check_ordered(self, check_tables=[]):
        if not check_tables:
            #unique_tables = check_tables
            #unique_tables = list(set(unique_tables) & set(check_tables))
            unique_tables = self.check_name()

        else:
            print(self.check_name())
            unique_tables = self.check_name()

        probable = []
        print(unique_tables)
        for i in unique_tables:
            unique_table_arr = []
            temp = self.meta_field.loc[self.meta_field['TableName'] == i].copy(
            )
            for index, row in temp.iterrows():
                unique_table_arr.append(str(row['datatype'])+str(row['order']))

            if np.array_equal(sorted(self.get_input_array()), sorted(unique_table_arr)) == True:
                probable.append(i)
        return probable


'''
layout = TableLayoutOrder(r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv',
                          r"G:\Siddhi\Office Personal\Content Based\siddhi\table1.csv")
print(layout.check_name())
'''
