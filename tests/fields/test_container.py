import pytest

from container.fields import Container, Value, Any, Dictionary, Array
from container import exc


class Cont(Container):
    body = {
        "a": Value("int", meta={"edit": True})
    }


class Cont1(Container):
    body = {
        "a": Value("int"),
        "b": Cont()
        }


class Cont2(Container):
    body = {
        "a": Value("int", meta={"edit": True}),
        "b": Value("int", meta={"edit": False}),
        "c": Value("int", meta={"edit": True})
    }


_body = {
    "v1": Value("int"),
    "v2": Value("float"),
    "v3": Value("bool"),
    "v4": Value("str", required=True),
    "a1": Any(),
    "a2": Any(),
    "r1": Array(Value("int")),
    "d1": Dictionary(),
    "c1": Cont()
    }


class C(Container):
    body = _body


@pytest.fixture
def cont():
    c1 = C()
    c1["v1"] = 1
    c1["v2"] = 2
    c1["v3"] = 2
    c1["v4"] = "fs"
    c1["a1"] = {"a": 1}
    c1["a2"] = "asd"
    return c1


def test_type(cont):
    assert cont.type == "container"


def test_overwrite():
    c = C(strict=False)
    assert id(c._value) != id(_body)
    assert c.strict is False
    c = C()
    assert c.strict is True


def test_getitem(cont):
    cont["d1"]["a"] = 1

    assert isinstance(cont["v1"], Value)
    assert isinstance(cont["a1"], Any)
    assert isinstance(cont["a2"], Any)
    assert isinstance(cont["v2"], Value)
    assert isinstance(cont["v3"], Value)
    assert isinstance(cont["v4"], Value)
    assert isinstance(cont["d1"], Dictionary)
    assert isinstance(cont["c1"], Container)
    assert isinstance(cont["c1"]["a"], Value)
    assert cont["d1"]["a"] == 1


def test_value(cont):
    assert cont["v1"].value == 1
    assert cont["v2"].value == 2.0
    assert cont["v3"].value is True
    assert cont["v4"].value == "fs"
    assert cont["a1"].value == {"a": 1}
    assert cont["a2"].value == "asd"

    cont["c1"]["a"] = 23
    assert cont["c1"]["a"].value == 23
    assert cont["c1"].value == {"a": 23}




def test_fields(cont):
    assert set(cont.fields) == {"v1", "v2", "v3", "v4", "a1", "a2", "r1", "c1", "d1"}


def test_get_not_supported_field(cont):
    with pytest.raises(exc.NotSupportedField):
        cont["aa"]


def test_set_not_supported_field(cont):
    with pytest.raises(exc.NotSupportedField):
        cont["aa"] = 2


def test_value_required_field(cont):
    cont["v4"] = None
    with pytest.raises(exc.RequiredField):
        cont.value





def test_populate(cont):
    data = {
        "v1": 1,
        "v2": 1,
        "v3": 1,
        "v4": "1",
        "a1": [1, 2, 3],
        "a2": {"a": 1},

        "c1": {"a": 20}
        }

    c = C()
    c.populate(data)

    print(c.value)
    assert c.value == data


def test_required_container(cont):
    cont["c1"].required = True
    with pytest.raises(exc.RequiredField):
        cont.value


def test_strict_container(cont):
    data = {
        # should be integer
        "v1": "dsa",
        "v2": 1,
        "v3": 1,
        "v4": "1",
        "a1": [1, 2, 3],
        "a2": {"a": 1},

        "c1": {"a": 20}
        }

    c = C()
    c["v1"].required = True
    c.populate(data)

    with pytest.raises(exc.IntError):
        c.value


def test_empty_fields(cont):
    cont["v1"] = 0
    cont["v2"] = 0.
    cont["v3"] = False
    cont["v4"] = ""
    cont["a1"] = dict()
    cont["a2"] = list()

    assert cont.value == {"v1": 0, "v2": 0.0, "v3": False, "v4": "", "a1": dict(), "a2": list()}
    cont["v3"] = None
    assert cont.value == {"v1": 0, "v2": 0.0, "v4": "", "a1": dict(), "a2": list()}
    cont["c1"]["a"] = 2
    assert cont.value == {"v1": 0, "v2": 0.0, "v4": "", "a1": dict(), "a2": list(), "c1": {"a": 2}}
    cont["c1"]["a"] = None
    assert cont.value == {"v1": 0, "v2": 0.0, "v4": "", "a1": dict(), "a2": list()}


def test_schema():
    assert Cont1().schema == {'b': {'a': 'int'}, 'a': 'int'}
    assert Cont().schema == {'a': 'int'}

def test_meta_search():
    c = Cont2()
    print(c._value["a"])
    res = c.meta_search("edit", "eq", True)
    print(res)