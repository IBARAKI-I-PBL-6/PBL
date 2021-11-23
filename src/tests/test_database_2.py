
import pytest
from ..logging_setting import set_logger

from ..database import database_2
from logging import getLogger
set_logger()
logger = getLogger(__name__)


@pytest.fixture(scope='function')
def init():

    with open("test.db", 'w'):
        pass
    data2 = database_2()
    yield {'data2': data2}


def test_database_2_init(init):
    """
    初期化に対するテスト
    """
    data2 = init['data2']
    out = data2.show()
    assert len(out) == 24
    logger.warning(out)
    for i in range(24):
        assert(out[i] == (i,  0))


def test_database_2_single(init):
    """
    値を一回変更した時のテスト
    """
    data2 = init['data2']
    data2.change_total_room(3, 5)
    assert data2.get_total_room(3) == 5
    assert data2.show()[3] == (3, 5)


def test_database_2_double(init):
    """
    同じ時刻の人数を複数回変更した時のテスト
    """
    data2 = init['data2']
    assert data2.show()[0] == (0, 0)
    data2.change_total_room(0, 10)
    assert data2.show()[0] == (0,  10)
    data2.change_total_room(0, 6)
    assert data2.show()[0] == (0,  6)
    data2.change_total_room(0, 40)
    assert data2.show()[0] == (0,  40)


def test_database_2_get_total(init):
    """
    同じ時刻の人数を複数回変更した時のテスト
    """
    data2 = init['data2']
    assert data2.get_total_room(0) == 0
    data2.change_total_room(0, 10)
    assert data2.get_total_room(0) == 10
    data2.change_total_room(0, 6)
    assert data2.get_total_room(0) == 6
    data2.change_total_room(0, 40)
    assert data2.get_total_room(0) == 40


def test_database_2_reset(init):
    """
    reset_in_roomのテスト
    """
    data2 = init['data2']
    assert data2.get_total_room(0) == 0
    data2.change_total_room(0, 10)
    assert data2.get_total_room(0) == 10
    data2.reset_total_room(0)
    assert data2.get_total_room(0) == 0


def test_database_2_step(init):
    """
    同じ時刻の人数を一人ずつ回変更した時のテスト
    """
    data2 = init['data2']
    assert data2.get_total_room(0) == 0
    for i in range(10):
        data2.change_total_room_increase(0)
    assert data2.get_total_room(0) == 10
    for i in range(30):
        data2.change_total_room_increase(0)
    assert data2.get_total_room(0) == 40


def test_database_2_two_hour(init):
    """
    2時間にわたって人数を変化したときのテスト
    """
    data2 = init['data2']
    assert data2.show()[0] == (0,  0)
    data2.change_total_room_increase(0)
    data2.change_total_room_increase(0)
    assert data2.show()[0] == (0,  2)
    data2.change_total_room_increase(1)
    data2.change_total_room_increase(1)
    assert data2.show()[1] == (1,  2)
    data2.change_total_room_increase(4)
    assert data2.show()[0] == (0,  2)
    assert data2.show()[1] == (1,  2)
    assert data2.show()[4] == (4,  1)
