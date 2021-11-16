from ..database import database_1
import pytest


def test_database_1_init():
    data1=database_1()
    assert len(data1.show())==24
    return True


def test_database_1_reinit():
    return True