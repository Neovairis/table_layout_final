import pathlib
import magic
import argparse
from table_info import TableInformation
import zipfile
import patoolib
import subprocess
import os
from LayoutDetector import LayoutDetector
from to_database import DatabaseWriter
from database_logger import file_process_log, file_repo
import xlrd
import csv
import pandas as pd
from datetime import datetime

from configparser import ConfigParser

parser = ConfigParser()
parser.read('conf.ini')
table_meta = parser.get('path', 'table_meta')
field_meta = parser.get('path', 'field_meta')
acceptable_delimiters = [',', '|', ';', ':', '::', '||']

argparser = argparse.ArgumentParser()

args = argparser.add_argument('-path', dest='filepath')

f = magic.Magic()


rar = r'''"C:\Program Files\WinRAR\WinRAR.exe"'''


def lower_case(sentence):
    sentence = sentence.split()
    arr = []
    for i in sentence:
        arr.append(i.lower())
    sentence = ' '.join(arr)
    return sentence


class Extraction:
    @staticmethod
    def list_zip(path):
        '''
        returns the list of zip file in the path
        '''
        f = []
        d = []
        dic = {}
        for (dirpath, dirnames, filenames) in os.walk(path):
            for i in filenames:
                dic.update({i: dirpath})
        zip_arr = []
        for key, value in dic:
            zip_path = value + "\\" + key
            ext = Extensions(zip_path)
            if (ext.check_magic()[1] == ".rar") or (ext.check_magic()[1] == ".zip"):
                zip_arr.append(zip_path)
        return zip_arr

    def __init__(self, filepath, pwd=[]):
        self.pwd = pwd
        self.filepath = filepath

    def list_files(self):
        '''
        Return the paths of the files
        '''
        f = []
        d = []
        dic = {}
        for (dirpath, dirnames, filenames) in os.walk(self.filepath+"extracted"):
            for i in filenames:
                dic.update({i: dirpath})

        return dic

    def extract(self):
        '''
        extracts the compressed files
        '''
        try:
            os.mkdir(self.filepath+"extracted")

        except:
            print("The file already Exists")
        finally:
            if self.pwd == []:
                print("Password is not given. Will only extract unprotected files")
                subprocess.call((rar + " x "+" -p- -r -ibck -Y" + " \"" +
                                 self.filepath + "\"" + " " + "\"" + self.filepath+"extracted" + "\""))
            else:
                '''
                Try all given passwords
                '''
                for i in self.pwd:
                    subprocess.call((rar + " x "+"-p"+"\""+self.pwd+"\"" + " -r -ibck -Y" + " \"" +
                                     self.filepath + "\"" + " " + "\"" + self.filepath+"extracted" + "\""))

    def excel_txt_arr(self):
        '''
        returns list of paths for text files, excel files and zip files
        '''

        txt = []
        xlsx = []
        zipp = []
        for key, value in self.list_files().items():
            path = value + "\\" + key
            ext = Extensions(path)

            ext = Extensions(path)
            if ext.check_magic()[1] == ".txt":
                txt.append(path)
            elif ext.check_magic()[1] == ".xlsx":
                xlsx.append(path)
            elif (ext.check_magic()[1] == ".zip") or (ext.check_magic()[1] == '.rar'):
                zipp.append(path)
            else:
                print("NON SUPPORTED FILE")
            print(ext.check_magic())
        return txt, xlsx, zipp

files = []
class Extensions:
    '''
    Deals with extensions
    '''

    def __init__(self, filepath):
        self.filepath = filepath
        self.actual_extension = pathlib.Path(self.filepath).suffix
        self.file_type = f.from_file(self.filepath)

    def check_magic(self):
        '''
        Checks the magic number of the file and returns file type. The File type can be added as required.
        '''
        file_type = lower_case(self.file_type)
        if 'text' in file_type:
            return True, '.txt'
        elif 'word' in file_type:
            print("the file is in word file")
            return False, '.docx'
        elif 'excel' in file_type:
            return True, '.xlsx'

        elif 'iso' in file_type:
            print("the file looks like a compressed iso file!!")
            return False, '.iso'
        elif 'zip' in file_type:
            print("the file  looks like a compressed zip file!!")
            return True, '.zip'
        elif 'rar' in file_type:
            print("the file  looks like a compressed rar file!!")
            return True, '.rar'
        else:

            return False, self.file_type


class Handler:
    '''
    Handler Class used to deal with the files. The main entry point of the file
    '''
    
    def __init__(self, filepath):
        
        self.filepath = filepath

    def txthandler(self):
        '''
        Receives the path to text file and detects the layout
        '''
        info_table = TableInformation(filepath=self.filepath)
        deli = info_table.show_delimeter()
        # check for the acceptable delimeters. Feel free to add any other delimeters as required!
        if deli not in acceptable_delimiters:
            print('could not find a proper delimiter!')
        else:
            files.append(self.filepath)
            print(self.filepath)    
            
            '''
            # find layout
            layout = LayoutDetector(self.filepath, field_meta,
                                    table_meta)
            write_this = pd.read_csv(self.filepath, sep=deli)
            write_this.drop_duplicates(inplace=True)
            probable_table = layout.identify()
            writer = DatabaseWriter()
            writer.make_connection(db='data')
            try:
                writer.get_database_table(probable_table[0])
                writer.append_chunk(dataframe=write_this,
                                    op_type='pandas', )
            except IndexError:
                print("No tables found that match the layout!")

            # return probable_table, write_this
            '''
    def to_csv(self):
        '''
        Convert the excel file to csv and sets the paths to newly converted csvs
        '''
        excel = pd.ExcelFile(self.filepath)

        print(excel.sheet_names)
        self.table_path = []
        for i in excel.sheet_names:
            self.table_path.append(self.filepath+"_" +
                                   i+".csv")
            df = pd.read_excel(excel, i)
            df.to_csv(self.filepath+"_" +
                      i+".csv", sep="|", index=False)

    def xlsxhandler(self):
        '''
        Handlles the excel files
        '''
        # convert to csv
        self.to_csv()
        for i in self.table_path:
            print(i)
            new_handle = Handler(i)
            new_handle.handle_file()

    def compressed_handler(self):
        '''
        Handles thee compressed files. I.e extract the compressed file and handle the content as well
        '''
        # check if encrypted
        # extract
        # check if compressed file exists
        # extract
        # get list of files
        # handle file
        extraction = Extraction(self.filepath)
        extraction.extract()
        file_list = extraction.excel_txt_arr()
        # check if the file is text file
        for i in file_list[0]:
            texthandle = Handler(i)
            texthandle.handle_file()
        # check if the file is an excel file
        for i in file_list[1]:
            xlhandle = Handler(i)
            xlhandle.handle_file()
        # check if the file is compressed file
        for i in file_list[2]:
            zhandle = Handler(i)
            zhandle.handle_file()

    def handle_file(self):
        
        '''
        handle the file according to the extensions. Accept the file and determine the file type and handle accordingly
        '''
        
    
        ext = Extensions(self.filepath)
        status, extension = ext.check_magic()
        filename = os.path.basename(self.filepath)
        #s = file_repo(file_name = filename,file_path = self.filepath,file_arrived_date = datetime.now(),client = 1, module_layout = 1, latest_phase = 1,is_incremental = 'y',file_type = 'csv',active_flag = 1,created_by= 'siddhi',created_on = datetime.now(),updated_by = 'siddhi',comment = 'test',updated_on = datetime.now())
        #s  = file_repo.selectBy(file_name = filename,file_path = self.filepath,file_arrived_date = datetime.now(),client = 1, module_layout = 1, latest_phase = 1,is_incremental = 'y',file_type = 'csv',active_flag = 1,created_by= 'siddhi',created_on = datetime.now(),updated_by = 'siddhi',comment = 'test',updated_on = datetime.now())
        if extension == ".txt":
            self.txthandler()
        elif extension == ".xlsx":
            self.xlsxhandler()
        elif (extension == ".rar") or (extension == ".zip"):
            self.compressed_handler()
        else:
            print("Invalid Format Format : ", extension)


'''
handle = Handler(
    "G:\Siddhi\Office Personal\Content Based\Content Based.rarextracted\movies.xlsx")
handle.handle_file()
'''

def is_blank(filepath):
    # checking the file size
    if os.stat(filepath).st_size == 0:
        print("The file is empty.\nTerminating")
        return True
    else:
        return False
        

def main():
    results = argparser.parse_args()
    filepath = results.filepath
    filename = os.path.basename(filepath)
    extension = Extensions(filepath)
    ext = extension.check_magic()[1]
    fr = file_repo(file_name = filename,file_path =filepath,file_arrived_date = datetime.now(),client = 1, module_layout = 1, latest_phase = 1,is_incremental = 'y',file_type =ext ,active_flag = 1)
    fpl = file_process_log(component_command_string='new_file_detector()', result_string = 'New File Recieved', log_path = 'none', action_method = 'S', file = fr.id,client = 1, phase = 1, component = 1, )
    file_repo_id = fr.id
    if os.path.exists(filepath) == True:
        
        file_empty_check = is_blank(filepath)
        if file_empty_check == False:
            file_process_log(component_command_string='blank_file_idenifier() filename size', result_string = 'File Not Empty', log_path = 'none', action_method = 'S', file = fr.id,client = 1, phase = 1, component = 1, )
            handle = Handler(filepath)
            handle.handle_file()
            print(files)

        else : 
            file_process_log(component_command_string='blank_file_idenifier() filename size', result_string = 'File Empty', log_path = 'none', action_method = 'S', file = fr.id,client = 1, phase = 1, component = 1, )


    else:
        print("File does not exist!")

    #detect new file
    #check blank file
    # identify format 
    # handle file format
    # identify layout
    # pre imoprt
    # import
if __name__ == "__main__":
    main()

# usage
'''
handle = Handler(
    "G:\Siddhi\Office Personal\Content Based\Content Based-20181114T141022Z-001.zip")
handle.handle_file()
'''
# use these files for testing purposes