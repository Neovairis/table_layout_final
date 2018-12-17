import pathlib
import magic
import argparse
argparser = argparse.ArgumentParser()
from table_info import TableInformation
import zipfile

argparser.add_argument('-p', dest='pathname')


results = argparser.parse_args()
f = magic.Magic(magic_file=r"c:\Windows\System32\magic.mgc")

# These are the file formats that are currently accepted!
acceptable_extensions = ['.txt', '.csv']


def show_info(pathname):
    '''
    Takes in the path of the file!
    Returns the extension of the file in pathname and a brief description about the file.

    '''
    extension = pathlib.Path(pathname).suffix
    file_type = f.from_file(pathname)
    if file_type == 'empty':
        file_type = 'an empty file. \nMay be you need to add something'

    return extension, file_type


def check_extension(extension, pathname):
    # if the extension of the file is in accepted extensions that were described above!
    if extension in acceptable_extensions:
        info_table = TableInformation(pathname)
        deli = info_table.show_delimeter()
        # check for the acceptable delimeters. Feel free to add any other delimeters as required!
        if deli not in [',', '|', ';', ':', '::', '||']:
            print('could not find a proper delimiter!   ')

        else:
            info_table.show_table_info()
    elif extension in ['.zip', '.tar', '.7z', '.rar', ]:
        print("Checking ...")
        zf = zipfile.ZipFile(pathname)
        try:
            zf.testzip()
            print('This Zip file is not password protected!')
        except RuntimeError as e:
            if 'encrypted' in str(e):
                print('The file is password protected!!')
            else:
                print('some other error')
    else:
        print("The file you provided seems to be {} file. How can I find a table in {} file?".format(
            extension, extension))


def other_handler(file_extension):
    if 'text' in file_extension:
        return True, '.txt'
    elif 'word' in file_extension:
        print("the file is in word file")
        return False, '.docx'
    elif 'excel' in file_extension:
        print("already an excel file")
        return False, '.xlsx'

    elif 'iso' in file_extension:
        print("the file is looks like a compressed iso file!!")
        return False, '.iso'
    elif 'zip' in file_extension:
        print("the file is looks like a compressed file!!")
        return True, '.zip'
    else:

        return False, file_extension


def lower_case(sentence):
    sentence = sentence.split()
    arr = []
    for i in sentence:
        arr.append(i.lower())
    sentence = ' '.join(arr)
    return sentence


def main():
    pathname = results.pathname
    print(pathname)
    extension, file_type = show_info(pathname)
    print("\n==========================Information about the file==========================")
    print("The extension of the file is {}.".format(extension))
    print("The file is idenfified as {}.".format(file_type))

    status, ext = other_handler(lower_case(file_type))
    print("==============================================================================")
    if status == True:
        check_extension(ext, pathname)


if __name__ == "__main__":
    main()
