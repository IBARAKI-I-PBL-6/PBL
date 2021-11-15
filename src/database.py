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
    conn: Connection
    c: Cursor
    database_name: str

    def __init__(self, data_name: str):
        """
        データベースファイルを開く

        Parameters
        ---------
            data_neme : str
            開くデータベースファイルの名前
        """
        self.database_name = data_name
        self.conn = sqlite3.connect(self.database_name)
        logger.info(f"opened : {self.database_name}")
        self.c = self.conn.cursor()

    def __del__(self):
        """
        データベースファイルを閉じる
        """
        self.conn.close()
        logger.info(f"closed : {self.database_name}")

    def execute(self, command: str):
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


class datatable(database):
    """
    テーブルの操作を行う
    """
    table_name: str

    def __init__(self, database_name: str, table_name: str, args: str = None):
        """
        コンストラクタ
        テーブルオブジェクトを作成する

        Paramters
        ---------
        database_name :str
            データベースのファイル名
        table_name : str
            ターブルの名前
        args : str (defalt = None)
            テーブルの属性

        Raies
        -----
        sqlite3.OperationalError
            argsを指定したときにその文字列が不正な文字列であったとき
        """
        super().__init__(database_name)
        self.table_name = table_name

        if args is not None:
            try:
                self.execute(f'CREATE TABLE {table_name} ({args})')
                logger.info(
                    f'created : {self.database_name} :: {self.table_name}')
            except sqlite3.OperationalError as e:
                if not str(e) == f"table {self.table_name} already exists":
                    raise e


if __name__ == '__main__':
    from logging_setting import set_logger
    set_logger()
    #data = database('test.db')

    #print(data.excute("select * from articles"))
    # data.excute("select")
    data2 = datatable('test.db', 'articles', 'a in')
