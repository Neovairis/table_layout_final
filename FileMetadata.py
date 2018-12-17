import pathlib
import magic
import argparse
argparser = argparse.ArgumentParser()
from table_info import TableInformation
import zipfile
import patoolib
from ToCsv import to_csv

f = magic.Magic(magic_file=r"c:\Windows\System32\magic.mgc")
acceptable_extensions = ['.txt', '.csv']
acceptable_delimiters = [',', '|', ';', ':', '::', '||']
acceptable_compressed = ['.zip', '.tar', '.7z', '.rar', ]


class FileMetadata:
    def __init__(self, pathname):
        self.pathname = pathname
        self.actual_extension = pathlib.Path(self.pathname).suffix
        self.file_type = f.from_file(self.pathname)

    def show_info(self):
        if self.file_type == 'empty':
            file_type = 'an empty file. \nMay be you need to add something'

        return self.actual_extension, self.file_type

    def check_extension(self):
        # if the extension of the file is in accepted extensions that were described above!
        if self.extension in acceptable_extensions:
            return 'textfile'

        if self.actual_extension == '.xlsx':
            return '.xlsx'

        elif self.extension in acceptable_compressed:
            return 'zipfile'

        else:
            return 'none'
            print("The file you provided seems to be {} file. How can I find a table in {} file?".format(
                self.extension, self.extension))

    def handle_text(self):
        info_table = TableInformation(filepath=self.pathname)
        deli = info_table.show_delimeter()
        # check for the acceptable delimeters. Feel free to add any other delimeters as required!
        if deli not in acceptable_delimiters:
            print('could not find a proper delimiter!   ')

        else:
            info_table.show_table_info()

    def extract(self, pwd=''):
        import subprocess
        rar = r'''"C:\Program Files\WinRAR\WinRAR.exe"'''
        pwd = "\""+pwd+"\""
        import os
        try:

            os.mkdir(self.pathname+"extracted")

        except:
            print("The file seems to be already exist")
        finally:
            if pwd == "\""+"\"":
                print("Password is not given. Will only extract unprotected files")
                subprocess.call((rar + " x "+" -p- -r -ibck -Y" + " \"" +
                                 self.pathname + "\"" + " " + "\"" + self.pathname+"extracted" + "\""))
            else:
                subprocess.call((rar + " x "+"-p"+pwd + " -r -ibck -Y" + " \"" +
                                 self.pathname + "\"" + " " + "\"" + self.pathname+"extracted" + "\""))
    '''
    Alternate extraction using platoolib
    
    '''
    '''
    def extract(self):
        import os
        try:
            os.mkdir(self.pathname+"extracted")
            patoolib.extract_archive(
                self.pathname, outdir=self.pathname+"extracted")
        except FileExistsError as e:
            print("The folder name already exists. Rename the folder at {}. You already seem to have extracted the compressed file. Reading from the uncompressed file! ".format(
                self.pathname))
    '''

    def list_files(self):

        from os import walk

        f = []
        d = []
        dic = {}
        for (dirpath, dirnames, filenames) in walk(self.pathname+"extracted"):

            for i in filenames:
                dic.update({i: dirpath})

        return dic

    def handle_zip(self):
        print("Checking ...")
        files_array = []
        try:
            self.extract()

            print("****************************************COMPRESSED FILES************************************************")

        finally:
            print("Extracting and processing non password protected files")
            files = self.list_files()
            print(files)
            for key, value in files.items():

                files_array.append(value+'\\'+key)
        return (files_array)

    def handle_file(self):
        if self.check_extension() == 'textfile':
            self.handle_text()
        elif self.check_extension() == 'zipfile':
            self.textfiles = []
            # the files in the zip file is stored in files
            files = self.handle_zip()
            for i in files:
                print(i)
                self.textfiles.append(i)

        else:
            print('Add support to such files!')

    def check_magic(self):
        file_type = self.lower_case(self.file_type)
        if 'text' in file_type:
            return True, '.txt'
        elif 'word' in file_type:
            print("the file is in word file")
            return False, '.docx'
        elif 'excel' in file_type:
            return True, '.xlsx'

        elif 'iso' in file_type:
            print("the file is looks like a compressed iso file!!")
            return False, '.iso'
        elif 'zip' in file_type:
            print("the file is looks like a compressed file!!")
            return True, '.zip'
        elif 'rar' in file_type:
            print("the file is looks like a compressed file!!")
            return True, '.rar'
        else:

            return False, self.file_type

    @staticmethod
    def lower_case(sentence):
        sentence = sentence.split()
        arr = []
        for i in sentence:
            arr.append(i.lower())
        sentence = ' '.join(arr)
        return sentence

    def main_handler(self):

        status, ext = self.check_magic()
        self.extension = ext
        if status == True:

            # self.check_extension()
            if self.check_extension() == 'textfile':
                # self.handle_text()
                return 'text'

            elif self.check_extension() == '.xlsx':
                return 'excel'

            elif self.check_extension() == 'zipfile':
                self.zipfiles = []
                # the files in the zip file is stored in files
                files = self.handle_zip()
                for i in files:
                    self.zipfiles.append(i)
                return 'zip'

        else:
            print('Add support to such files!')
            return None


from LayoutDetector import LayoutDetector

arr = []
excel = []
print("********************************************TESTING A COMPRESSED FILE*********************************************************************************")
#file = r'G:\Siddhi\Office Personal\Content Based\Content Based.rar'
file = r'G:\Siddhi\Office Personal\Content Based\Content Based-20181114T141022Z-001.zip'
fm = FileMetadata(file)
if fm.main_handler() == 'zip':
    print(fm.zipfiles)
    for i in fm.zipfiles:
        fm1 = FileMetadata(i)
        if fm1.main_handler() == 'text':
            arr.append(i)
        elif fm1.main_handler() == 'excel':
            excel.append(i)

    for i in arr:
        try:
            detector = LayoutDetector(i,
                                      r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv', r'G:\Siddhi\Office Personal\table_identifier\table_meta.csv')
            if detector.identify != 0:
                print(detector.identify())
        except:
            print('lol')
    print("CONVERTING EXCEL TO CSV IF THEYY EXIST")
    for i in excel:
        print("converting excel to csv")
        to_csv(i)
        try:
            detector = LayoutDetector(i+'.csv',
                                      r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv', r'G:\Siddhi\Office Personal\table_identifier\table_meta.csv')
            if detector.identify != 0:
                print(detector.identify())
        except:
            print('lol')
else:
    print('nonzip')
    detector = LayoutDetector(file,
                              r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv', r'G:\Siddhi\Office Personal\table_identifier\table_meta.csv')
    print(detector.identify(True))


print("********************************************TESTING A SINGLE FILE*********************************************************************************")

file = r'G:\Siddhi\Office Personal\table_identifier\table1.csv'

fm = FileMetadata(file)
if fm.main_handler() == 'zip':
    print('zip')
    for i in fm.zipfiles:
        fm1 = FileMetadata(i)
        if fm1.main_handler() == 'text':
            arr.append(i)

    for i in arr:
        print("===========================================================================================================================================")
        try:
            print(i)
            detector = LayoutDetector(i,
                                      r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv', r'G:\Siddhi\Office Personal\table_identifier\table_meta.csv')
            if detector.identify != 0:
                print(detector.identify())
        except:
            print('lol')
else:
    print('nonzip')
    detector = LayoutDetector(file,
                              r'G:\Siddhi\Office Personal\table_identifier\field_meta.csv', r'G:\Siddhi\Office Personal\table_identifier\table_meta.csv')
    print(detector.identify(True))
