import pytest

from container.fields import Value
from container import exc


def test_check_avaliable_types():
    v = Value("str")

    assert v.types == {"float", "int", "str", "bool"}


def test_check_type():
    with pytest.raises(exc.WrongFieldType):
        Value(type_name="string")


# BOOL
def test_parse_bool_success():
    v = Value(type_name="bool")
    
    v._value = 1
    assert v.value is True

    v._value = 2.2
    assert v.value is True

    v._value = "2"
    assert v.value is True

    v._value = {"a"}
    assert v.value is True

    v._value = [1, 4, 4, 4, 4]
    assert v.value is True


def test_parse_bool_failure():
    v = Value(type_name="bool")

    v._value = ""
    assert v.value is False

    v._value = list()
    assert v.value is False

    v._value = dict()
    assert v.value is False

    v._value = set()
    assert v.value is False


def test_get_unset_value():
    v = Value(type_name="bool")
    assert v.value is None

    v = Value(type_name="float")
    assert v.value is None

    v = Value(type_name="int")
    assert v.value is None

    v = Value(type_name="str")
    assert v.value is None


# FLOAT
def test_parse_float_strict_failure():
    v = Value(type_name="float", strict=True)
    with pytest.raises(exc.FloatError):
        v.parse_float("2a")


def test_parse_float_not_srtict_failure():
    v = Value(type_name="float", strict=False)
    res = v.parse_float("22a")

    assert res is None
    assert v.is_valid is False


def test_parse_float_success():
    v = Value(type_name="float")
    
    res = v.parse_float("2")
    assert res == 2.0

    res = v.parse_float("2.")
    assert res == 2.0

    res = v.parse_float("2,")
    assert res == 2.0

    res = v.parse_float(".1")
    assert res == 0.1

    res = v.parse_float(",1")
    assert res == 0.1
    
    res = v.parse_float("2,23")
    assert res == 2.23

    res = v.parse_float("2.222")
    assert res == 2.222

    res = v.parse_float(2)
    assert res == 2.0

    res = v.parse_float(2.0)
    assert res == 2.0


def test_return_none():
    v = Value(type_name="float")

    res = v.parse_float(None)
    assert res is None

# INTEGER
def test_parse_int_strict_failure():
    v = Value(type_name="int", strict=True)
    with pytest.raises(exc.IntError):
        v.parse_int("2a")


def test_parse_int_not_srtict_failure():
    v = Value(type_name="int", strict=False)
    res = v.parse_int("2a")

    assert res is None
    assert v.is_valid is False


def test_parse_int_success():
    v = Value(type_name="int")
    
    res = v.parse_int("1")
    assert res == 1

    res = v.parse_int("1.1")
    assert res == 1

    res = v.parse_int("1,1")
    assert res == 1

    res = v.parse_int("1,a")
    assert res == 1

    res = v.parse_int("1.a")
    assert res == 1

    res = v.parse_int(1)
    assert res == 1

    res = v.parse_int(1.2)
    assert res == 1


def test_is_allowed_failure():
    v = Value(type_name="int", allowed={1, 2, 3, 4})

    with pytest.raises(exc.ForbiddenValue):
        v.set(5)
        v.value


def test_is_allowed_not_strict_failure():
    v = Value(type_name="int", allowed={1, 2, 3, 4}, strict=False)

    v.set(5)
    assert v.value is None
    assert v.is_valid is False


def test_is_allowed():
    v = Value(type_name="int", allowed={1, 2, 3, 4})

    v.set(1)
    assert v.value == 1


def test_get_all_values():
    vi = Value("int")
    assert vi.set("1").value == 1
    assert vi.set("1.1").value == 1
    assert vi.set("1,1").value == 1
    assert vi.set("1,a").value == 1
    assert vi.set("1,").value == 1
    assert vi.set("1.").value == 1
    assert vi.set(1).value == 1
    assert vi.set(1.3).value == 1
    assert vi.set(None).value is None

    vf = Value("float")
    assert vf.set("1").value == 1.0
    assert vf.set("1.1").value == 1.1
    assert vf.set("1,1").value == 1.1
    assert vf.set("1,").value == 1.0
    assert vf.set(".1").value == 0.1
    assert vf.set(",1").value == 0.1
    assert vf.set(1).value == 1.0
    assert vf.set(1.2).value == 1.2
    assert vf.set(None).value is None


def test_set():
    v = Value("int")

    assert v.set(1) == v