import pytest

from container.fields import Cell


valid_cell_value = {"a": 1, "b": 2}


class Cell1(Cell):
    cell = valid_cell_value


@pytest.fixture
def cell():
    return Cell1()


def test_overwrite_cell_to_value(cell):
    assert cell._value == valid_cell_value
    assert id(cell._value) != id(valid_cell_value)


def test_get(cell):
    with pytest.raises(NotImplementedError):
        cell.get()


def test_value(cell):
    with pytest.raises(NotImplementedError):
        cell.value


def test_set(cell):
    with pytest.raises(NotImplementedError):
        cell.set()


def test_required():
    d = Cell(required=True)

    assert d.required is True


def test_not_required():
    d = Cell(required=False)

    assert d.required is False


def test_type():
    c = Cell()
    assert c.type is None