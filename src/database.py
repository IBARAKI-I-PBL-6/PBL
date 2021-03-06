"""
データベースに関するクラス
"""
import sqlite3
from logging import getLogger
from sqlite3 import Connection, Cursor
from typing import List, Tuple

logger = getLogger(__name__)


class AlreadyExistsError(sqlite3.Error):
    """
    テーブルを作ったが、すでに存在しているときに投げられるエラー(sqlite3.Errorから継承)
    """


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
        data_name : str
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

        Parameters
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

    def commit(self):
        """変更を反映する"""
        self.conn.commit()


class datatable(database):
    """
    テーブルの操作を行う
    """
    table_name: str

    def __init__(self, database_name: str, table_name: str, args: str = None):
        """
        コンストラクタ
        テーブルオブジェクトを作成する

        Parameters
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
                # エラーの種類がすでにテーブルが作られたのが原因であるとき
                if str(e) == f"table {self.table_name} already exists":
                    raise AlreadyExistsError(
                        f"{self.table_name} has already exist")
                else:
                    raise e

    def insert(self, value: Tuple, auto_committe: bool = True):
        """
        インスタンスを追加する

        Parameters
        ---------
        value : (Tuple)
            追加するインスタンス
        auto_committe : bool (defalt = True)
            値の追加後に自動でコミットするか
        """
        self.execute(f"insert into {self.table_name} values {value}")
        if auto_committe:
            self.commit()  # 変更を反映する

    def select(self, column: str = '*', filter: str = None):
        """
        インスタンスを抽出して返す

        Parameters
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

        Parameters
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
            self.commit()  # 変更を反映する

    def delate(self, filter: str, auto_committe: bool = True):
        """
        タプルの値を変更する

        Parameters
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

        self.execute(f"DELETE from {self.table_name} {mod}")
        if auto_committe:
            self.commit()  # 変更を反映する

    def show(self):
        """
        テーブルの内容を返す

        Returns
        -------
        res : [Tuple]
            テーブルの内容
        """
        return self.select()


class database_sql_instance:
    """
    databasea_sqlのインスタンス1つ分を格納するクラス

    Attributes
    ---------
    id : int
        通し番号
    enter : int
        一時間の総入室人数
    max_in_room : int
        一時間の在室人数の最大
    alert :int
        総警告回数
    """
    id: int
    enter: int
    max_in_room: int
    alert: int

    def __init__(self, id: int, enter: int, max_in_room: int, alert: int):
        """
        データの初期化

        Parameters
        ---------
        id : int
            通し番号
        enter : int
            一時間の総入室人数
        max_in_room : int
            一時間の在室人数の最大
        alert :int
            総警告回数
        """
        # 各値を順番の代入する
        self.id = id
        self.enter = enter
        self.max_in_room = max_in_room
        self.alert = alert


class database_sql(datatable):

    """
    一時間ごとの入室人数、最大在室人数、総警告回数に関するデータベース

    主キー
    ------
    id : int
        入力の通し番号

    属性キー
    -------
    enter : int
        その時間の総入室人数
    max_in_room : int
        その時間の在室人数の最大
    """
    __update_counter: int  # データを追加した回数
    ROTATE_DAYS = 30  # データを保存する日数

    def __init__(self):
        """
        コンストラクター
        """
        try:
            # テーブルを初期化する
            super().__init__("test.db", "database_sql",
                             "id int , enter int, max_in_room int , alert int")
        except AlreadyExistsError:
            pass
        self.__update_counter = 0

    def add_datas(self, enter: List[int], max_in_room: List[int], alert: List[int]):
        """
        データを追加する

        Parameters
        ---------
        enter : List[int]
            各時間ごとの総入室人数[人]
        max_in_room : List[int]
            各時間ごとの最大在室人数[人]
        alert : List[int]
            各時間ごとの総警告回数[回]

        Requirement
        -----------
        - len(enter) == len(max_in_room) == len(alert) (各引数の要素数は同じ)
        - len(enter) < 24 (引数の要素数は24以下)

        Raises
        ------
        RuntimeError
            len(enter) != len(max_in_room) の時、もしくは　len(enter) != len(alert)のとき
        """
        # len(enter) == len(max_in_room) == len(alert)かどうか確かめる
        if len(enter) != len(max_in_room) or len(max_in_room) != len(alert):
            # さもなければ RuntimeErrorを投げる
            raise RuntimeError("len(enter) != len(max_in_room) != len (alert)")

        # idがself.__update_counter*24 以上(self.__update_counter+1)*24+未満のインスタンスを削除する
        self.delate(
            f'(id >= {self.__update_counter*24}) and ( id < {(self.__update_counter+1)*24})')

        # len(enter) 回繰り返す(i):
        for i in range(len(enter)):
            #   id をself.__update_counter *24 + iにする
            id = self.__update_counter * 24 + i
            #   (id, enter[i],max_in_room[i], alert[i])を追加する
            self.insert((id, enter[i], max_in_room[i], alert[i]))
        # self.__update_counterを1加算して、それをself.ROTATE_DAYSで割ったあまりにする
        self.__update_counter = (self.__update_counter + 1) % self.ROTATE_DAYS

    def get_data(self, id: int):
        """
        id がidであるインスタンスを取得する

        Parameters
        ---------
        id : int
            取得したいデータのidの値 (検討中)

        Returns
        -------
        result : database_sql_instance
            データのidがidであるインスタンスを格納したクラス
        """

        #id,enter, max_in_room,alertにidがidであるときの値を代入する
        id, enter, max_in_room, alert = self.select(filter=f'id={id}')[0]
        # database_sql_instanceのインスタンスを作成する、引数は、先ほど取得した変数の順
        res = database_sql_instance(id, enter, max_in_room, alert)
        # 先ほどのインスタンスを返す
        return res


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
    print("daa2")
    print(data2.select(filter='id=2'))
    data2.execute('drop table articles')
    data3 = database_1()
    print(data3.show())
    print(data3.get_max_in_room(0))
