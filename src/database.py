"""
データベースに関するクラス
"""
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from logging import getLogger
logger = getLogger(__name__)

class database:
    """
    データベースファイルの操作を行うクラス
    
    """
    conn:Connection 
    c:Cursor
    database_name: str

    def __init__(self,data_name:str):
        """
        データベースファイルを開く

        Parameters
        ---------
            data_neme : str
            開くデータベースファイルの名前
        """
        self.database_name=data_name
        self.conn = sqlite3.connect(self.database_name)
        logger.info(f"opened : {self.database_name}")
        self.c=self.conn.cursor()

    def __del__(self):
        """
        データベースファイルを閉じる
        """
        self.conn.close()
        logger.info(f"closed : {self.database_name}")
    def excute(self,command:str):
        """
        SQLコマンドを実行する

        Paramters
        ---------
        command : str
            実行コマンド

        Returns
        -------
        res: [Teple]
            実行後のカーソルにfetchall()をした時の返り値

        Raises
        ------
        sqlite3.OperationalError
            コマンド列が不正であった場合
        """
        self.c.execute(command)
        return self.c.fetchall()


if __name__=='__main__':
    from logging_setting import set_logger
    set_logger()
    data = database('test.db')
    
    print(data.excute("select * from articles"))
    data.excute("select")

