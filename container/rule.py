class Operator(object):
    def _eq(self, op1, op2):
        return op1 == op2

    def _ne(self, op1, op2):
        return op1 != op2

    def _is(self, op1, op2):
        return op1 is op2

    def _gt(self, op1, op2):
        return op1 > op2

    def _lt(self, op1, op2):
        return op1 < op2

    def _gte(self, op1, op2):
        return op1 >= op2

    def _lte(self, op1, op2):
        return op1 <= op2

    def do(self, name):
        op_name = "_" + name

        return getattr(self, op_name)


class Rule(Operator):
    def __init__(self, cell1, do, cell2=None, const=None, cont=None, strict=True):
        self.cell1 = cell1
        self.cell2 = cell2
        self.const = const
        self.do_name = do
        
        self.strict = strict

        self.cont = cont

    def set_cont(self, cont):
        self.cont = cont

    def __get_operands(self):
        val1 = self.cont.path(self.cell1).value

        val2 = None
        if self.cell2 is not None:
            val2 = self.cont.path(self.cell2).value
        else:
            val2 = self.const

        return val1, val2

    def use(self):
        op = self.do(self.do_name)

        val1, val2 = self.__get_operands()
        
        res = op(val1, val2)
        if self.strict:
            if not res:
                raise ValueError("{} not {} {}".format(val1, self.do_name, val2))

        return res



if __name__ == "__main__":
    op = Operator()

    print(op.do("nae")(None,None))