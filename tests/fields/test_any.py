from container.fields import Any


def test_get1():
    a = Any()
    a._value = 2

    assert a.get() == 2


def test_get2():
    a = Any()
    a._value = list()

    assert a.get() == list()


def test_get3():
    a = Any()
    a._value = dict()

    assert a.get() == dict()


def test_set():
    test_data = {"a": 1, "b": 2}
    a = Any()
    a.set(test_data)

    assert a.get() == test_data and a._value == test_data


def test_type():
    a = Any()

    assert a.type == "any"
