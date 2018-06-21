import pytest

from container.fields import Dictionary


@pytest.fixture
def dictionary():
    d = Dictionary()
    d._value = {"a": 1}
    return d


def test_is_dict():
    d = Dictionary()

    assert isinstance(d._value, dict)


def test_get_unset_value():
    v = Dictionary()

    assert v.value is None


def test_get_empty_is_none(dictionary):
    dictionary._value = {}
    assert dictionary.get() is None


def test_getitem_success(dictionary):
    assert dictionary["a"] == 1


def test_getitem_failure(dictionary):
    dictionary._value = {}

    assert dictionary["a"] is None


def test_setitem(dictionary):
    dictionary["b"] = 2

    assert dictionary["b"] == 2


def test_setitem_overwrite(dictionary):
    dictionary["a"] = 100

    assert dictionary["a"] == 100


def test_value_equival_value(dictionary):
    assert dictionary.get() == dictionary.value


def test_value_is_original_dict(dictionary):
    assert dictionary._value == dictionary.get() and dictionary._value == dictionary.value


def test_required():
    d = Dictionary(required=True)

    assert d.required is True


def test_not_required():
    d = Dictionary(required=False)

    assert d.required is False


def test_type():
    d = Dictionary()
    assert d.type is "dict"


def test_set():
    data = {"a": 1, "v": 2, "c": [1, 2], "s": {"a": 2}}

    d = Dictionary()
    d.set(data)

    assert d.value == data
    assert d["a"] == 1
    assert d["v"] == 2
    assert d["c"] == [1, 2]
    assert d["c"][1] == 2
    assert d["s"] == {"a": 2}
    assert d["s"]["a"] == 2