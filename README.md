### Define data structure

```python
from container.fields import Container, Value
from container.rule import Rule

class Cont(Container):
    body = {
        "a": Value("int", meta={"edit": True}),
        "b": Value("int", meta={"edit": True}, required=True)
    }

class Cont1(Container):
    body = {
        "a": Value("int", meta={"edit": True}),
        "b": Value("int", meta={"edit": False}),
        "c": Value("int", meta={"edit": True}),
        "d": Cont()
    }
    # 'a' has to be less then "d.b"
    rules = (
        Rule(cell1="a", do="lt", cell2="d.b"),
        )
```

Fill container data

```python
c = Cont(strict=False)

c.populate({"a": 1, "b": "22,5"})
```

Show data

```python
print(c.value)

{'b': 22.5, 'a': 1}
```

```python
c1 = Cont1()
c1["a"] = 100
c1["d"]["b"] = "22,5"
```

Raise as exception
```
Traceback (most recent call last):
  File "/mnt/hdd/myprojects/container/container/fields.py", line 449, in <module>
    print(c1.value)
  File "/mnt/hdd/myprojects/container/container/fields.py", line 335, in value
    self.use_rules()
  File "/mnt/hdd/myprojects/container/container/fields.py", line 377, in use_rules
    print(rule.use())
  File "/mnt/hdd/myprojects/container/container/rule.py", line 62, in use
    raise ValueError("{} not {} {}".format(val1, self.do_name, val2))
ValueError: 100 not lt 22
```