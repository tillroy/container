import pytest

from container.fields import Array


def test_type():
    a = Array()

    assert a.type == "array"


def test_is_list():
    a = Array()

    assert isinstance(a._value, list)


def test_add():
    a = Array()
    a.add(1)
    a.add(2)

    assert a.add(2) == a
    assert a[0] == 1
    assert a[1] == 2


def test_set():
    a = Array()
    a.set("abc")
    assert a.value == ["a", "b", "c"]

    a = Array()
    a.set([1, 2, 3])
    assert a.value == [1, 2, 3]


def test_empty_array_value():
    a = Array()

    assert a.value is None


def test_getitem_with_base_type():
    a = Array(base_type=str)
    a.add(1)
    a.add("2")

    assert a[0] is None
    assert a[1] == "2"


def test_getitem_without_base_type():
    a = Array()
    a.add(1)
    a.add("2")

    assert a[0] == 1
    assert a[1] == "2"


def test_get_value_only_valid():
    a = Array(base_type=int)
    a.add(1)
    a.add("2")

    assert a.get() == [1]
