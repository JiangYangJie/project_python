# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : mysql   
#     data      : 2019/11/10
import pymysql

class cursor():
    def __init__(self, SQL):
        """
        cursor:该对象用来创建SQL游标，该类的主要用途是对cursor进行封装，使用with机制进行使用
        :param SQL: SQl对象
        :param sql_statement: sql语句
        """
        self.SQL = SQL

    def read(self, sql_statement, *args):
        try:
            self.cursor.execute(sql_statement, list(args))
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return ('')

    def write(self, sql_statement, *args):
        try:
            self.cursor.executemany(sql_statement, [args])
        except Exception as e:
            print(e)
            print('sql error')

    def __enter__(self):
        self.cursor = self.SQL.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        return True


class mysql():
    def __init__(self,host='localhost', user='root',password='admin',db='houseprice', port=3306,):
        self.SQL = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port,
            charset="utf8")

    def read(self, sql_statement, *args):
        try:
            self.cursor.execute(sql_statement, args)
            # print(self.cursor.fetchall())
            return self.cursor.fetchall()
        except:
            return ('')

    def write(self, sql_statement, *args):
        try:
            self.cursor.executemany(sql_statement, args[0])
            self.SQL.commit()
        except Exception as e:
            self.SQL.rollback()
            print('sql error:',e)


    def __enter__(self):
        self.cursor = self.SQL.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.SQL.close()
        return True
