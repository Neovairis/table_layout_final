from csv import Sniffer
import pandas as pd
import datetime
import numpy as np


class TableInformation:
    '''
    this is used to give information about the tables
    '''

    @staticmethod
    def validate(date_text):
        try:

            datetime.datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except:
            pass

    def __init__(self, filepath):
        self.filepath = filepath

    def show_line(self):
        try:
            with open(self.filepath, "r", errors='ignore') as myfile:
                head = [next(myfile) for x in range(2)]
            try:
                #
                self.line = head[1]
            except:
                self.line = head[0]
            # print(self.line)
            return self.line
        except FileNotFoundError:
            print("OOPS! Did you type in the correct path?")

    def show_delimeter(self):
        sniffer = Sniffer()
        sniffer.preferred = [',', '|', ';', ':', '::', '||']
        dialect = sniffer.sniff(self.show_line())
        self.deli = dialect.delimiter
        return self.deli

    def show_table_info(self):
        try:
            self.length = len(self.show_line().split(self.show_delimeter()))
            print("Line : {} \nDelimeter : {} \nLength : {}\nDate : {}".format(
                self.line, self.deli, self.length, self.is_date()))
            return self.line, self.deli, self.length, self.is_date()
        except AttributeError:
            print("OOPS! ")

    def is_date(self):
        c = 0
        dte = []
        for i in self.line.split(','):
            if (self.validate(i[1:11])) or (self.validate(i)):
                dte.append(c)

            c += 1
        return dte

    def which_table(self, table_meta, field_meta):
        self.table_meta = pd.read_csv(table_meta, header=None)

        '''def dateparse(x): return pd.datetime.strptime(x, '%Y-%m-%d')
        date = self.is_date()'''

        probable = []
        # print(self.table_meta)
        for index, row in self.table_meta.iterrows():
            #print(row[1], row[2])
            if (row[1] == self.length) & (row[2] == self.deli):
                # print(row[0])
                #print(self.length, self.deli)
                probable.append(row[0].lower())
        print('this', probable)
        return probable
