import cx_Oracle
import hashlib


class Database:
    tables = {'users', 'eventt'}



    def __init__(self):
        try:
            self.con = cx_Oracle.connect('SYSTEM/dbms@127.0.0.1')
           # self.con = cx_Oracle.connect('oracleAdmin/Admin321@oracledbaws.cgbepdadfdij.us-east-1.rds.amazonaws.com:1521/ORCL')
            self.cur = self.con.cursor()
            self.check_table()


        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("Oracle-Error-1: ", error.code)
            print("Oracle-Error-Message1: ", error.message)

    def check_table(self):
        fd = open('db.sql', 'r')
        sqlfile = fd.read()
        fd.close()
        sqlcommands = sqlfile.split(';')
        for command in sqlcommands:
            try:
                self.cur.execute(command)
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                print("Oracle-Error-Code: ", error.code)
                print("Oracle-Error-Message: ", error.message)
        self.con.commit()


db = Database()
