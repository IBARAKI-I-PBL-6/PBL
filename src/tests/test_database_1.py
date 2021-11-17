
import pytest
from ..logging_setting import set_logger

from ..database import database, database_1
from logging import getLogger
set_logger()
logger = getLogger(__name__)


@pytest.fixture(scope='function')
def init() -> database:

    with open("test.db", 'w'):
        pass
    data1 = database_1()
    yield {'data1': data1}


def test_database_1_init(init):
    """
    初期化に対するテスト
    """
    data1 = init['data1']
    out = data1.show()
    assert len(out) == 24
    logger.warning(out)
    for i in range(24):
        assert(out[i] == (i, 0, 0))
    return True


def test_database_1_single(init):
    """
    値を一回変更した時のテスト
    """
    data1 = init['data1']
    data1.change_in_room(3, 5)
    assert data1.get_max_in_room(3) == 5
    assert data1.show()[3] == (3, 5, 5)


def test_database_1_reinit(init):
    """値を入れた後に再び初期化したときのテスト"""
    test_database_1_single(init)
    data1 = database_1()
    out = data1.show()
    logger.warning(out)
    for i in range(24):
        if i == 3:
            continue
        assert out[i] == (i, 0, 0)
    assert out[3] == (3, 5, 5)

    return True


def test_database_1_double(init):
    """
    同じ時刻の人数を複数回変更した時のテスト
    """
    data1 = init['data1']
    assert data1.show()[0] == (0, 0, 0)
    data1.change_in_room(0, 10)
    assert data1.show()[0] == (0, 10, 10)
    data1.change_in_room(0, 6)
    assert data1.show()[0] == (0, 6, 10)
    data1.change_in_room(0, 40)
    assert data1.show()[0] == (0, 40, 40)


def test_database_1_get_count(init):
    """
    get_count_in_roomのテスト
    """
    data1 = init['data1']
    assert data1.get_count_in_room(0) == 0
    data1.change_in_room(0, 10)
    assert data1.get_count_in_room(0) == 10
    data1.change_in_room(0, 6)
    assert data1.get_count_in_room(0) == 6
    data1.change_in_room(0, 40)
    assert data1.get_count_in_room(0) == 40


def test_database_1_get_max(init):
    """
    get_max_in_roomのテスト
    """
    data1 = init['data1']
    assert data1.get_max_in_room(0) == 0
    data1.change_in_room(0, 10)
    assert data1.get_max_in_room(0) == 10
    data1.change_in_room(0, 6)
    assert data1.get_max_in_room(0) == 10
    data1.change_in_room(0, 40)
    assert data1.get_max_in_room(0) == 40


def test_database_1_step(init):
    """
    同じ時刻の人数を一人ずつ回変更した時のテスト
    """
    data1 = init['data1']
    assert data1.show()[0] == (0, 0, 0)
    for _ in range(10):
        data1.change_in_room_increase(0)
    assert data1.show()[0] == (0, 10, 10)
    for _ in range(4):
        data1.change_in_room_decrease(0)
    assert data1.show()[0] == (0, 6, 10)
    for _ in range(34):
        data1.change_in_room_increase(0)
    assert data1.show()[0] == (0, 40, 40)


def test_database_1_two_hour(init):
    """
    2時間にわたって人数を変化したときのテスト
    """
    data1 = init['data1']
    assert data1.show()[0] == (0, 0, 0)
    data1.change_in_room_increase(0)
    data1.change_in_room_increase(0)
    assert data1.show()[0] == (0, 2, 2)
    data1.change_in_room_decrease(1)
    assert data1.show()[1] == (1, 1, 2)
    data1.change_in_room_increase(1)
    data1.change_in_room_increase(1)
    assert data1.show()[1] == (1, 3, 3)
    data1.change_in_room_increase(2)
    assert data1.show()[2] == (2, 4, 4)


def test_database_1_stay(init):
    """
    1時間以上、人数が変化しないときのテスト
    """
    data1 = init['data1']
    assert data1.show()[0] == (0, 0, 0)
    data1.change_in_room_increase(0)
    data1.change_in_room_increase(0)
    assert data1.show()[0] == (0, 2, 2)
    data1.change_in_room_decrease(2)
    assert data1.show()[1] == (1, 2, 2)
    assert data1.show()[2] == (2, 1, 2)
    data1.change_in_room_increase(2)
    data1.change_in_room_increase(2)
    assert data1.show()[2] == (2, 3, 3)
    data1.change_in_room_increase(5)
    assert data1.show()[2] == (2, 3, 3)
    assert data1.show()[3] == (3, 3, 3)
    assert data1.show()[4] == (4, 3, 3)
    assert data1.show()[5] == (5, 4, 4)


def test_database_1_deyond(init):
    """
    日をまたぐときののテスト
    """
    data1 = init['data1']
    assert data1.show()[23] == (23, 0, 0)
    data1.change_in_room_increase(23)
    assert data1.show()[23] == (23, 1, 1)
    data1.change_in_room_increase(3)
    logger.warning(data1.show())
    assert data1.show()[0] == (0, 1, 1)
    assert data1.show()[1] == (1, 1, 1)
    assert data1.show()[2] == (2, 1, 1)
    assert data1.show()[3] == (3, 2, 2)
    data1.change_in_room(23,4)
    assert data1.show()[23] == (23, 4, 4)
    data1.change_in_room_decrease(3)
    logger.warning(data1.show())
    assert data1.show()[0] == (0, 4, 4)
    assert data1.show()[1] == (1, 4, 4)
    assert data1.show()[2] == (2, 4, 4)
    assert data1.show()[3] == (3, 3, 4)
