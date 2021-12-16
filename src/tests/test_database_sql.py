
import pytest
from ..logging_setting import set_logger

from ..database import database_sql, database_sql_instance
from logging import getLogger
set_logger()
logger = getLogger(__name__)


@pytest.fixture(scope='function')
def init():

    with open("test.db", 'w'):
        pass
    data = database_sql()
    yield {'data': data}


def test_database_sql_init(init):
    """
    初期化に対するテスト
    """
    data = init['data']
    out = data.show()
    print(out)
    assert out == []


def test_database_sql_single(init):
    """
    値を一回変更した時のテスト
    """
    data = init['data']
    data.add_datas([3], [2], [5])
    res = data.get_data(0)
    assert res.id == 0
    assert res.enter == 3
    assert res.max_in_room == 2
    assert res.alert == 5


def test_database_sql_double(init):
    """
    同じ時刻で複数個追加した時のテスト
    """
    data = init['data']
    data.add_datas([3, 6], [2, 4], [5, 13])
    res = data.get_data(0)
    assert res.id == 0
    assert res.enter == 3
    assert res.max_in_room == 2
    assert res.alert == 5
    res = data.get_data(1)
    assert res.id == 1
    assert res.enter == 6
    assert res.max_in_room == 4
    assert res.alert == 13


def test_database_sql_get_double2(init):
    """
    複数の時刻で複数回変更した時のテスト
    """
    data = init['data']
    data.add_datas([3], [2], [5])
    data.add_datas([6], [4], [13])
    res = data.get_data(0)
    assert res.id == 0
    assert res.enter == 3
    assert res.max_in_room == 2
    assert res.alert == 5
    res = data.get_data(24)
    assert res.id == 24
    assert res.enter == 6
    assert res.max_in_room == 4
    assert res.alert == 13


def test_database_sql_get_mouth(init):
    """
    値の削除を伴うデータの実行
    """
    data = init['data']
    for i in range(0,40):
        data.add_datas([i], [i], [i]) #30日目に0に戻る
    res = data.get_data(0)
    assert res.id == 0
    assert res.enter == 30
    assert res.max_in_room == 30
    assert res.alert == 30
