import pandas as pd
from mysql import connector
import mysql
import sqlalchemy


class DatabaseWriter:
    '''
    Takes a dataframe and writes it to the existing table in the database
    '''

    def make_connection(self, host='localhost', user='root', passwd='', db='default'):
        '''
        host: string type, hostname of the database
        user : string type, user of the database
        passwd : string type, password for the database
        db : string type, name of the database

        '''

        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        try:
            self.mydb = connector.connect(host=self.host,
                                          user=self.user,
                                          passwd=self.passwd,
                                          database=self.db)
            self.mycursor = self.mydb.cursor()
        except Exception as e:
            print("In Function  make_connection", str(e))

    def get_database_table(self, table_name):
        self.table_name = table_name
        try:
            self.sql = pd.read_sql_table(
                self.table_name, "mysql://"+self.user+self.passwd+"@"+self.host+"/"+self.db)
        except Exception as e:
            print("Cannot connect to the database. Details: \n", str(e))

    def append_line(self, val):

        st = ("%s,"*self.sql.shape[1]).split(",")[:-1]
        self.query = ("INSERT INTO " + self.table_name +
                      ' (' + ','.join(self.sql.columns.values) + ')' +
                      ' VALUES ' + ' (' + ','.join(st) + ')')
        try:
            self.mycursor.execute(self.query, val)
            self.mydb.commit()
        except Exception as e:
            print("Cannot execute the query! Details: \n", str(e))

    def append_chunk(self, dataframe, op_type='pandas'):
        self.dataframe = dataframe
        if op_type != 'pandas':
            for i in self.dataframe.iterrows():
                try:
                    self.append_line(tuple(i[1]))
                except Exception as e:
                    print(str(e))
        else:
            try:
                self.dataframe.to_sql(name=self.table_name, con="mysql://"+self.user +
                                      self.passwd+"@"+self.host+"/"+self.db, if_exists='append', index=False)
            except sqlalchemy.exc.IntegrityError as e:
                print("Primary key is already in the terget table. Aborting..")
            except sqlalchemy.exc.OperationalError as e:
                print("In function append_chunk", str(e))

    def remove_dups(self):
        pass


# USAGE
df = pd.read_csv(r"G:\Siddhi\Office Personal\meta\table1.csv")
writer = DatabaseWriter()
writer.make_connection(db='table_identify')
writer.get_database_table('table1')
writer.append_chunk(op_type='pandas', dataframe=df)
