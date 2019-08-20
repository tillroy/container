# -*- coding: utf-8 -*-
from container.fields import Container, Value


def build_container(config, strict=True):
    _body = dict()
    for el in config:
        val = Value(el["type"], required=el["required"])
        _body[el["name"]] = val

    class ContainerBuilder(Container):
        body = _body

    res = ContainerBuilder(strict=strict)
    return res



if __name__ == "__main__":
    conf = [
        {"name": "test", "type": "int", "required": True},
        {"name": "test1", "type": "int", "required": True},
        {"name": "test2", "type": "int", "required": True},
    ]
    res = build_container(conf, strict=True)
    res["test"] = "123"
    print(res.value)