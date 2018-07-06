from pprint import pformat
import copy

import ujson

from container import exc
from container.rule import Rule


class Cell(object):
    """Base class for all fields"""

    # cell type, defines starting point of container type
    cell = None

    def __init__(self, required=False, meta={}):
        # contains additional descriptive data
        self.meta = meta

        self.required = required
        self._value = None
        self._type = None
        self.is_valid = True
        if self.__class__.cell is not None:
            self._value = copy.copy(self.__class__.cell)

    def get(self):
        raise NotImplementedError

    def set(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self.get()


class Any(Cell):
    def __init__(self, required=False, meta={}):
        super(Any, self).__init__(required, meta)
        self._type = "any"

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


class Dictionary(Cell):
    cell = dict()

    def __init__(self, required=False, meta={}):
        super(Dictionary, self).__init__(required, meta)
        self._type = "dict"

    def __getitem__(self, key):
        return self._value.get(key)

    def __setitem__(self, key, val):
        self._value[key] = val

    def set(self, dictionary):
        if isinstance(dictionary, dict):
            self._value = dict()
            for key in dictionary:
                self._value[key] = dictionary[key]
        else:
            raise TypeError("Cant set from non 'dict'")

    def get(self):
        # WHY: is it necessary??
        if self._value:
            return self._value


class Array(Cell):
    cell = list()

    def __init__(self, required=False, base_type=None, meta={}):
        super(Array, self).__init__(required, meta)
        self.base_type = base_type
        self._type = "array"

    def __getitem__(self, ind):
        if self.base_type is not None:
            val = self._value[ind]
            if isinstance(val, self.base_type):
                return val
            else:
                return None
        else:
            return self._value[ind]

    def add(self, val):
        self._value.append(val)

        return self

    def set(self, val):
        self._value = list()
        for el in val:
            self.add(el)

    def get(self):
        res = list()
        for ind in range(len(self._value)):
            val = self[ind]
            if val is not None:
                res.append(val)

        if res:
            return res


class Value(Cell):
    types = {"float", "int", "str", "bool"}

    def __init__(
            self, type_name, strict=True,
            allowed=None, required=False, meta={}
            ):
        super(Value, self).__init__(required, meta)
        # self._value = None
        self.strict = strict
        self._type = self.__check_type(type_name)
        self.allowed = allowed

    # def __str__(self):
        # return "<Value v:{0}, t:{1}>".format(self._value, self.type)

    # def __repr__(self):
    #     return str(self.value)

    def parse_float(self, val):
        try:
            if isinstance(val, bool):
                raise Exception
            elif isinstance(val, float):
                return val
            elif isinstance(val, int):
                return float(val)
            elif isinstance(val, str):
                if "," in val:
                    val = val.replace(",", ".")

                val = float(val)

                return val

        except Exception as e:
            if self.strict:
                raise exc.FloatError("Can't convert to float, input value: {}".format(val))
            else:
                self.is_valid = False
                return None

    def parse_bool(self, val):
        return bool(val)

    def parse_int(self, val):
        try:
            if isinstance(val, int):
                return val
            elif isinstance(val, float):
                return int(val)
            elif isinstance(val, str):
                if "," in val:
                    val = val.replace(",", ".")

                val = val.split(".")[0]
                return int(val)

        except Exception as e:
            if self.strict:
                raise exc.IntError("Can't convert to int, input value: {}".format(val))
            else:
                self.is_valid = False
                return None

    def set(self, value):
        self._value = value

        return self

    def get(self):
        if self._value is not None:
            if self.type == "float":
                _val = self.parse_float(self._value)
                return self.__is_allowed(_val)
            if self.type == "int":
                _val = self.parse_int(self._value)
                return self.__is_allowed(_val)
            if self.type == "str":
                return self.__is_allowed(str(self._value))
            if self.type == "bool":
                _val = self.parse_bool(self._value)
                return self.__is_allowed(_val)

    def __is_allowed(self, val):
        if self.allowed:
            if val in self.allowed:
                return val
            else:
                if self.strict:
                    raise exc.ForbiddenValue("Value '{}' not in allowed: '{}'".format(val, self.allowed))
                else:
                    self.is_valid = False
                    return None
        else:
            return val

    def __check_type(self, type_name):
        if type_name in self.types:
            return type_name
        else:
            raise exc.WrongFieldType("Type '{}' not in allowed list: '{}'".format(type_name, self.types))


class Container(object):
    body = None
    rules = None
    # def_key_name = "name"
    # def_val_name = "value"

    def __init__(
            self, key_name=None, val_name=None,
            required=False, strict=True, meta={}
            ):
        self.meta = {}
        self._type = "container"

        self.required = required
        self.strict = strict

        if self.__class__.body:
            self._value = dict()
            for key, val in self.__class__.body.items():
                val.meta["__name"] = key
                val.meta["__parent"] = self
                if isinstance(val, Container):
                    print(val)
                    val.strict = self.strict
                self._value[key] = copy.deepcopy(val)
        else:
            self._value = dict()

        if self.__class__.rules:
            self._rules = list()
            for el in self.__class__.rules:
                self._rules.append(el)

                # self._rules[key] = copy.deepcopy(val)
        else:
            self._rules = tuple()

        # if key_name:
        #     self.def_key_name = key_name

        # if val_name:
        #     self.def_val_name = val_name

    @property
    def type(self):
        return self._type

    def __getitem__(self, key):
        if key in self._value:
            field = self._value.get(key)
            # print(self._value.get(key))
            return field
            # if isinstance(field, Container):
            #     return field
            # return field._value
            # return self._value.get(key).value
        else:
            if self.strict:
                raise exc.NotSupportedField("{} does not support field: {}".format(self.__class__.__name__, key))

    def __setitem__(self, key, val):
        if key in self._value:
            value = self._value.get(key)
            # TODO: add dictionary type
            if isinstance(value, (Value, Any)):
                value.set(val)
            # TODO: add this class
            # if isinstance(value, Parameter):
            #     value.set(*val)
        else:
            if self.strict:
                raise exc.NotSupportedField("{} does not support field: {}".format(self.__class__.__name__, key))

    def populate(self, dictionary):
        assert isinstance(dictionary, dict), "Input value should be <dict>, got : {}".format(type(dictionary))

        for fname in dictionary:
            # TODO: update this for populating Collection and other complex type
            field = self[fname]

            if isinstance(field, Container):
                print("container")
                print(fname, type(field))
                field.populate(dictionary[fname])
            else:
                # print(fname, type(field))
                if field is not None:
                    field.set(dictionary[fname])
            # data = dictionary[fname]
            # dest = self._values.get(fname)
            # assert isinstance(dest, (Value, Any)), "Cant populate complex type {} yet".format(type(dest))
            # dest.set(data)

        return self

    @property
    def value(self):
        features = dict()
        for key, val in self._value.items():
            required = val.required
            try:
                value = val.value
            except (exc.IntError, exc.FloatError, exc.ForbiddenValue) as e:
                value = None

            if value is not None:
                features[key] = value
            elif value is None and required:
                if self.strict:
                    raise exc.RequiredField("Field '{}' is required for container '{}'".format(key, self.__class__.__name__))
        if self.strict:
            self.use_rules()

        if features:
            return features

    def meta_search(self, meta_name, logic, value):
        """Find fields by meta key value"""

        res = list()
        for field_name in self._value:
            field = self._value[field_name]
            if field.type == "container":
                sub_cont_res = field.meta_search(meta_name, logic, value)
                res.extend(sub_cont_res)
            else:
                meta_value = field.meta.get(meta_name)
                if meta_value is not None:
                    if logic == "eq":
                        if meta_value == value:
                            res.append(field)
                    else:
                        print("[container]Don't know such logic value: {}".format(logic))

        return res

    def path(self, name):
        name_chain = name.split(".")
        if name_chain:
            first_el_name = name_chain.pop(0)
            rest_name = ".".join(name_chain)

            first_el = self._value.get(first_el_name)
            if first_el is not None:
                if first_el.type == "container" and rest_name != "":
                    return first_el.path(rest_name)
                else:
                    return first_el

    def use_rules(self):
        if self._rules:
            for rule in self._rules:
                rule.set_cont(self)
                print(rule.use())

    @property
    def schema(self):
        schema = dict()

        for name, val in self._value.items():
            t = val.type
            if t == "container":
                schema[name] = val.schema
            else:
                schema[name] = val.type

        return schema

    @property
    def fields(self):
        return self._value.keys()

    @property
    def json(self):
        return ujson.dumps(self.value)

    # def __str__(self):
    #     return pformat(self._value)

    # def __repr__(self):
    #     return pformat(self._value)

if __name__ == "__main__":
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

        rules = (
            Rule(cell1="a", do="lt", cell2="d.b"),
            )

    # c = Cont2(strict=False)
    # c["a"] = 20
    # c["b"] = 10
    # c["c"] = 11
    # c["d"]["a"] = 1
    # # c["d"]["b"] = 12

    # # res = c.meta_search("edit", "eq", True)
    # res = c.meta_search("__name", "eq", "a")
    # print(res)

    # res1 = c.path("d.b")


    # c1 = Cont(strict=False)

    # c1.populate({"a": 1, "b": "2"})

    # print(c1.value)

    c1 = Cont1()
    c1["a"] = 100
    c1["d"]["b"] = "22,5"

    print(c1.value)