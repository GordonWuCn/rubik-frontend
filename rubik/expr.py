#


class Expr:
    def __add__(self, other):
        return Op('add',[self, other])

    def __sub__(self, other):
        return Op('sub',[self, other])

    def __mul__(self, other):
        return Op('mul',[self, other])

    def __div__(self, other):
        return Op('div',[self, other])

    def __le__(self, other):
        return Op('le',[self, other])

    def __lt__(self, other):
        return Op('lt',[self, other])

    def __ge__(self, other):
        return Op('ge',[self, other])

    def __gt__(self, other):
        return Op('gt',[self, other])

    def __eq__(self, other):
        return Op('eq',[self, other])

    def __ne__(self, other):
        return Op('ne',[self, other])

    def __lshift__(self, other):
        return Op('lshift',[self, other])

    def __rshift__(self, other):
        return Op('rshift',[self, other])


class Op(Expr):
    op_dict = \
        {'add': '+',
         'sub': '-',
         'mul': '*',
         'div': '/',
         'le': '<=',
         'lt': '<',
         'ge': '>=',
         'gt': '>',
         'eq': '==',
         'ne': '!=',
         'lshift': '<<',
         'rshift': '>>',
         }

    def __init__(self, type, operand_list):
        self.type = type
        self.operand_list = operand_list
        self.hcode = ''
        self.dcode = ''
        self.ecode = ''
    def literal(self, proto_name):
        if self.type not in self.op_dict.keys():
            handler = getattr(self, "handle_" + self.type)
        else:
            handler = self.op_trans
        return handler(proto_name)

    def handle_hash(self, proto_name):
        #To use hash, the presumption is every protocol will only hash their keys once.
        #cannot deduct the length of key
        self.hcode = f'{proto_name}_select_t{{\n'
        for operand in self.operand_list:
            #uint32_t is pure makeup
            #TODO change this self.hcode += f'\tuint32_t {operand.literal(proto_name)};\n'
            pass
        self.hcode += "};\n"

        # self.dcode = f'struct {proto_name}_select_t* {proto_name}_select;\n'

        self.ecode = f"{proto_name}_hash({proto_name}_select)\n"

        return self.ecode

    def op_trans(self, proto_name):
        code = []
        for i in [0, 1]:
            if isinstance(self.operand_list[i], int):
                code.append(str(self.operand_list[i]))
            else:
                code.append(self.operand_list[i].literal(proto_name))

        return code[0] + self.op_dict[self.type] + code[1]

    def __str__(self):
        return (
            'OP:' + self.type + '(' + 
            str_list([str(operand) for operand in self.operand_list]) +
            ')'
        )


class Field(Expr):
    def __init__(self, name, layout):
        self.name = name
        self.layout = layout
        self.bit_obj = self.layout_search()

    def literal(self, proto_name):
        return self.bit_obj.literal(proto_name)
        
    def layout_search(self):
        func = getattr(self, self.layout.__class__.__name__ + "_search")
        return func(self.layout)

    def SeqLayout_search(self, layout):
        for l in layout.layout_list:
            func = getattr(self, l.__class__.__name__ + "_search")
            res = func(l)
            if res:
                return res

    def StructLayout_search(self, layout):
        for name, field in layout.iter_field():
            if name == self.name:
                return field
        return None

    def IfElseLayout_search(self, layout):
        for l in [layout.false, layout.true]:
            func = getattr(self, l.__class__.__name__ + "_search")
            res = func(l)
            if res: 
                return res

    def WhileAnyLayout_search(self, layout):
        for l in layout.choice_list:
            func = getattr(self, l.__class__.__name__ + "_search")
            res = func(l)
            if res: 
                return res

class Cursor(Expr):
    def literal(self, proto_name):
        return "cur_pos"
