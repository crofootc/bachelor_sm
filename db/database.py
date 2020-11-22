import mysql.connector as MySQL
import datetime
import db.delete_db
import db.set_up_db

# TODO: DELETE THIS?
def reset():
    try:
        delete_db.delete_tables()
    except:
        print("No Database to Delete")
    set_up_db.set_up()

# TODO: DELETE THIS LATER
def response():
    return "OK"

class Database():
    def __init__(self, host, db, user, pw):
        self.__db = db
        self.__conn = MySQL.connect(host=host, user=user, database=db, password=pw)
        self.__curs = self.__conn.cursor()

    def check_connection(self):
        print(self.__conn)
        print(self.__curs)

    # This should be faster use this for now
    def insert_ignore(self, table : str, data : list):
        # Get Columns ###
        self.__curs.execute(
            f'''
            show columns from {self.__db}.{table};
            '''
            )
        results = self.__curs.fetchall()

        # Get all columns except the primary key which auto increments
        col = [item[0] for item in results if not item[3]=='PRI']

        # Create Syntax to insert the data ###
        columns = ", ".join(col)
        values = '"' + '", "'.join(map(str, data)) + '"'
        sql = f"INSERT IGNORE INTO `{self.__db}`.`{table}` ({columns}) VALUES ({values})"

        # Allowing for nulls
        sql = sql.replace('"NULL"','NULL')

        self.__curs.execute(sql)
        self.__conn.commit()

        return True, data