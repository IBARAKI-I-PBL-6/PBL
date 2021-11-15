"""
データベースに関するクラス
"""
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from logging import getLogger
from typing import Tuple
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
        self.conn = sqlite3.connect(self.database_name)  # 接続する
        logger.info(f"opened : {self.database_name}")
        self.c = self.conn.cursor()  # カーソルを取得する

    def __del__(self):
        """
        データベースファイルを閉じる
        """
        self.conn.close()  # 切断する
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
        logger.info(f"execute: {command}")
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
                # テーブルを作成する
                self.execute(f'CREATE TABLE {table_name} ({args})')
                logger.info(
                    f'created : {self.database_name} :: {self.table_name}')
            except sqlite3.OperationalError as e:
                # エラーの種類がすでにテーブルが作られたのが原因ではないとき
                if not str(e) == f"table {self.table_name} already exists":
                    raise e

    def insert(self, value: Tuple, auto_committe: bool = True):
        """
        インスタンスを追加する

        Paramters
        ---------
        value : (any)
            追加するインスタンス
        auto_committe:bool (defalt = True)
            値の追加後に自動でコミットするか
        """
        self.execute(f"insert into {self.table_name} values {value}")
        if auto_committe:
            self.conn.commit()  # 変更を反映する

    def select(self, column: str = '*', filter: str = None):
        """
        インスタンスを抽出して返す

        Paramters
        ---------
        column : str (defalt ='*')
            取り出したい属性
        filter : str (defal = None)
            抽出する条件

        Returns
        -------
        res : [Tuple]
            抽出したインスタンス
        """
        mod = '' if filter is None else f'where {filter}'  # 変更を反映する
        res = self.execute(f'select {column} from {self.table_name} {mod}')
        return res

    def update(self, column: str, value: any, filter: str, auto_committe: bool = True):
        """
        タプルの値を変更する

        Paramters
        ---------
        column : str
            変更したい属性(一つのみ)
        value : any
            変更する値
        filter : str
            変更するインスタンスの条件
        auto_committe : bool (defalt : True)
            値の追加後に自動でコミットするか
        """
        mod = '' if filter is None else f'where {filter}'  # 絞り込みの条件を作る

        if type(value) is str:
            value = f"'{value}'"

        self.execute(f"update {self.table_name} set {column} = {value} {mod}")
        if auto_committe:
            self.conn.commit()  # 変更を反映する


if __name__ == '__main__':
    from logging_setting import set_logger
    set_logger()
    data2 = datatable('test.db', 'articles',
                      'id int, title varchar(1024), body text, created datetime')
    data2.insert((1, '今朝のおかず', '魚を食べました', '2020-02-01 00:00:00'))
    data2.insert((2, '今日のお昼ごはん', 'カレーを食べました', '2020-02-02 00:00:00'), False)
    data2.insert((3, '今夜の夕食', '夕食はハンバーグでした', '2020-02-03 00:00:00'))
    c = data2.select()
    print(c)
    data2.update("title", "チーズ", 'id=1')
    print(data2.select())
    data2.execute('drop table articles')
