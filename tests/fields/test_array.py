import pytest

from container.fields import Array, Value


def test_type():
    a = Array(Value("int"))

    assert a.type == "array"


def test_is_list():
    a = Array(Value("int"))

    assert isinstance(a._value, list)


def test_add():
    a = Array(Value("int"))
    a.add(1)
    a.add(2)

    assert a.add(2) == a
    assert a[0] == 1
    assert a[1] == 2


def test_set():
    a = Array(Value("str"))
    a.set("abc")
    assert a.value == ["a", "b", "c"]

    a = Array(Value("int"))
    a.set([1, 2, 3])
    assert a.value == [1, 2, 3]


def test_empty_array_value():
    a = Array(Value("int"))

    assert a.value is None


def test_getitem_with_base_type():
    a = Array(Value("int"), strict=True)
    a.add(1)
    a.add("2")

    assert a[0] is 1
    assert a[1] == 2


def test_getitem_without_base_type():
    a = Array(Value("int"))
    a.add(1)
    a.add("2")

    assert a[0] == 1
    assert a[1] == 2


def test_get_value_only_valid():
    a = Array(Value("int"), strict=False)
    a.add(1)
    a.add("2.a")

    assert a.get() == [1]
