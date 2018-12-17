import pandas as pd


def to_csv(pathname):
    '''
    takes in a xlsx file with one or more sheets and produces corresponding csv and returns their paths.
    '''
    excel = pd.ExcelFile(pathname)

    print(excel.sheet_names)
    table_path = []
    for i in excel.sheet_names:
        print(pathname+"_" +
              i+".csv")
        table_path.append(pathname+"_" +
                          i+".csv")
        df = pd.read_excel(excel, i)
        df.to_csv(pathname+"_" +
                  i+".csv", sep="|", index=False)
    return table_path


'''
excel_talbes = to_csv(
    "G:\Siddhi\Office Personal\Content Based\Content Based.rarextracted\movies.xlsx")
for i in excel_tables:
    print(i)
'''
