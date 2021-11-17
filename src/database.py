"""
データベースに関するクラス
"""
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from logging import getLogger
from typing import Tuple
logger = getLogger(__name__)


class AlreadyExistsError(sqlite3.Error):
    """
    テーブルを作ったが、すでに存在しているときに投げられるエラー
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
                # エラーの種類がすでにテーブルが作られたのが原因であるとき
                if str(e) == f"table {self.table_name} already exists":
                    raise AlreadyExistsError(
                        f"{self.table_name} has already exist")
                else:
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
            self.commit()  # 変更を反映する

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
            self.commit()  # 変更を反映する

    def show(self):
        """
        テーブルの内容を返す
        """
        return self.select()


class database_1(datatable):
    """
    在室している人数に関するデータベース

    主キー
    ------
    time : int
        時間

    属性キー
    -------
    count : int
        その時間の最新の在室人数
    max_count : int
        その時間の在室人数の最大
    """
    __last_updated_time: int  # 最後に更新した時間

    def __init__(self):
        """
        コンストラクター
        """
        try:
            # テーブルを初期化する
            super().__init__("test.db", "table1", "time int primary key, count int, max_count int")
            # トリガーを設定する(table1の更新後、更新前のmax_countが更新後のcountより小さいならば、更新した時間のmax_countをcountに変更する)
            self.execute(
                "create trigger max_counter after update on table1 when old.max_count  < new.count begin update table1 set max_count = count where time=old.time; end")
        except AlreadyExistsError:
            pass
        else:
            for i in range(24):
                self.insert((i, 0, 0), False)
            self.commit()
        self.__last_updated_time = -1

    def change_in_room(self, time: int, count: int):
        """
        time[h]に在室している人の値をcountに変更する
        同時に在室している人の値の最大値を更新する

        Paramters
        ---------
        time : int
            更新したい時間
        count : int
            更新する人数
        """

        if self.__last_updated_time == -1:  # 初めての更新
            init_max = 0
            self.__last_updated_time = time
        else:  # この時間では初めての更新
            init_max, = self.select('count', f'time={self.__last_updated_time}')[
                0]  # 最後の更新時間での在室数
            logger.info(f"init_max: {init_max}")
            while(not self.__last_updated_time == time):
                next_time = (self.__last_updated_time+1) % 24  # 次の時間
                # 最後の更新時間の次の時間の最大を最後の更新時間での在室数に
                self.update('max_count', init_max, f'time={next_time}')
                # 最後の更新時間の次の時間の在室数を最後の更新時間での在室数に
                self.update('count', init_max, f'time={next_time}')
                self.__last_updated_time = next_time

        self.update('count', count, f'time={time}')  # この時間の在室数を更新
        # 最大値を更新(トリガーで行われる)

    def change_in_room_increase(self, time: int):
        """
        time[h]に在室している人の値を一人増やす
        同時に在室している人の値の最大値を更新する

        Paramters
        ---------
        time : int
            更新したい時間
        """
        if self.__last_updated_time == -1:  # 初めての更新
            init_max = 0
            self.__last_updated_time = time
        else:  # この時間では初めての更新
            init_max, = self.select('count', f'time={self.__last_updated_time}')[
                0]  # 最後の更新時間での在室数
            logger.info(f"init_max: {init_max}")
            while(not self.__last_updated_time == time):
                next_time = (self.__last_updated_time+1) % 24  # 次の時間
                # 最後の更新時間の次の時間の最大を最後の更新時間での在室数に
                self.update('max_count', init_max, f'time={next_time}')
                # 最後の更新時間の次の時間の在室数を最後の更新時間での在室数に
                self.update('count', init_max, f'time={next_time}')
                self.__last_updated_time = next_time

        self.update('count', init_max+1, f'time={time}')  # この時間の在室数を更新
        # 最大値を更新(トリガーで行われる)

    def change_in_room_decrease(self, time: int):
        """
        time[h]に在室している人の値を一人減らす

        Paramters
        ---------
        time : int
            更新したい時間
        """
        if self.__last_updated_time == -1:  # 初めての更新
            self.__last_updated_time = time
        else:  # この時間では初めての更新
            init_max, = self.select('count', f'time={self.__last_updated_time}')[
                0]  # 最後の更新時間での在室数
            logger.info(f"init_max: {init_max}")
            while(not self.__last_updated_time == time):
                next_time = (self.__last_updated_time+1) % 24  # 次の時間
                # 最後の更新時間の次の時間の最大を最後の更新時間での在室数に
                self.update('max_count', init_max, f'time={next_time}')
                # 最後の更新時間の次の時間の在室数を最後の更新時間での在室数に
                self.update('count', init_max, f'time={next_time}')
                self.__last_updated_time = next_time

        self.update('count', init_max-1, f'time={time}')  # この時間の在室数を更新
        # 最大値を更新(トリガーで行われる)

    def get_max_in_room(self, time: int) -> int:
        """
        時間がtime[h]の時の、在室している人数の最大値を取得する

        Parameters
        ----------
        time : int
            在室している人数の最大を取得したい時間

        Returns
        -------
        max_count: int
            時間がtime[h]の時の、在室している人数の最大値
        """
        max_count = self.select('max_count', f'time={time}')
        res, = max_count[0]
        return res

    def get_count_in_room(self, time: int) -> int:
        """
        時間がtime[h]の時の、在室している人数の最新の値を取得する

        Parameters
        ----------
        time : int
            在室している人数の最大を取得したい時間

        Returns
        -------
        count: int
            時間がtime[h]の時の、在室している人数の最新値
        """
        count = self.select('count', f'time={time}')
        res, = count[0]
        return res


class database_2(datatable):
    """
    出入りした人数に関するデータベース

    主キー
    ------
    time : int
        時間

    属性キー
    -------
    count : int
        その時間での出入りの階数
    """

    def __init__(self):
        """
        コンストラクター
        """
        try:
            # テーブルを初期化する
            super().__init__("test.db", "table2", "time int primary key, count int")
        except AlreadyExistsError:
            pass
        else:
            for i in range(24):
                self.insert((i, 0), False)
            self.commit()

    def change_total_room(self, time: int, count: int):
        """
        time[h]に出入りした人数の値をcountに変更する

        Paramters
        ---------
        time : int
            更新したい時間
        count : int
            更新する人数
        """
        self.update('count', count, f'time={time}')  # この時間の出入り数を更新

    def get_total_room(self, time: int) -> int:
        """
        時間がtime[h]の時の、出入りした人数を取得する

        Parameters
        ----------
        time : int
            出入りした人数を取得したい時間

        Returns
        -------
        count: int
            時間がtime[h]の時の、 出入りした人数の値
        """
        count = self.select('count', f'time={time}')
        res, = count[0]
        return res

    def change_total_room_increase(self, time: int):
        """
        time[h]に出入りした人数の値を1加算する

        Paramters
        ---------
        time : int
            変更したい時間
        """
        self.update('count', self.get_total_room(
            time)+1, f'time={time}')  # この時間の出入り数を更新

    def reset_total_room_increase(self, time: int):
        """
        time[h]に出入りした人数の値を0にする

        Paramters
        ---------
        time : int
            変更したい時間
        """
        self.update('count', 0, f'time={time}')  # この時間の出入り数を更新


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
    data3 = database_1()
    print(data3.show())
    print(data3.get_max_in_room(0))
