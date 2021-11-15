"""
データベースに関するクラス
"""
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor

class database:
    """
    データベースファイルの操作を行うクラス
    
    """
    conn:Connection 
    c:Cursor

    def __init__(self,data_name:str):
        """
        データベースファイルを開く

        Parameters
            data_neme : str
            開くデータベースファイルの名前
        """
        self.conn = sqlite3.connect(data_name)
        
        self.c=self.conn.cursor()

    def __del__(self):
        """
        データベースファイルを閉じる
        """
        self.conn.close()


if __name__=='__main__':
    data=database('test1.db')