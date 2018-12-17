from tableschema import Table
import pandas as pd
import numpy as np
from TableLayoutOrder import TableLayoutOrder


order = TableLayoutOrder(r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv',
                         r"G:\Siddhi\Office Personal\Content Based\tags.csv")

test_table = pd.read_csv(
    r"G:\Siddhi\Office Personal\Content Based\siddhi\table1.csv", sep="|", header=None)

print(test_table.head())
field_meta = pd.read_csv(
    r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv')


unique_tables = field_meta['TableName'].unique()
array_name = []
for i in unique_tables:
    temp = field_meta.loc[field_meta["TableName"] == i]
    if np.array_equal(sorted(test_table.loc[0, :].values), sorted(temp["fields"].values)) == True:
        array_name.append(i)
    print(temp["fields"].values)

print(array_name)
