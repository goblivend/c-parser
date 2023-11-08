from nodes import Node, Edge
from tokens import TokenType

id=0
y=0

class Ast :
    def __init__(self) -> None:
        global id
        self.id = f'node_{id}'
        id+=1
        pass

    def to_json(self) :
        return {'nodes': None, 'edges': None}

class IfAst(Ast) :
    def __init__(self, cond:Ast, ifast:Ast, elseast:Ast) -> None:
        super().__init__()
        self.cond = cond
        self.ifast = ifast
        self.elseast = elseast

    def to_json(self) :
        global y
        nodes = [Node(self.id, 'If', {'name':'If'}, 0, y, 0, 0)]
        y+=100
        edges = [
            Edge(self.cond.id, 'output',self.id, 'input'),
            Edge(self.ifast.id, 'inflow',self.id, 'outflow1'),
            Edge(self.elseast.id, 'inflow', self.id, 'outflow2'),
        ]
        children = [
            self.cond.to_json(),
            self.ifast.to_json(),
            self.elseast.to_json()
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'if({self.cond}) {self.ifast} else {self.elseast}'

class WhileAst(Ast) :
    def __init__(self, cond:Ast, bodyast:Ast) -> None:
        super().__init__()
        self.cond = cond
        self.bodyast = bodyast

    def to_json(self) :
        global y
        nodes = [Node(self.id, 'While', {'name':'While'}, 0, y, 0, 0)]
        y+=100
        edges = [
            Edge(self.cond.id, 'output',self.id, 'input'),
            Edge(self.id, 'outflow1', self.bodyast.id, 'inflow'),
        ]
        children = [
            self.cond.to_json(),
            self.bodyast.to_json(),
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'while({self.cond}) {self.bodyast}'

class VarDecAst(Ast) :
    def __init__(self, type:TokenType, name:str, value:Ast) -> None:
        super().__init__()
        self.type = type
        self.name = name
        self.value = value

    def to_json(self) :
        global y
        nodes = [Node(self.id, 'VarDec', 0, y, 0, 0)]
        y+=100
        edges = [
            Edge(self.value.id, 'output', self.id, 'input')
        ]
        children = [
            self.value.to_json()
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'{self.type} {self.name} = {self.value}'

class VarAst(Ast) :
    def __init__(self, name:str) -> None:
        super().__init__()
        self.name = name

    def to_json(self) :
        global y
        res = {'nodes': [Node(self.id, 'Var', 0, y, 0, 0)], 'edges': []}
        y+=100
        return res
    def __repr__(self) -> str:
        return f'{self.name}'

class LiteralAst(Ast) :
    def __init__(self, value, type:TokenType) -> None:
        super().__init__()
        self.value = value
        self.type = type

    def to_json(self) :
        global y
        res=  {'nodes': [Node(self.id, 'Literal', {'name': 'Literal', 'type': self.type.name, 'value': str(self.value)}, 0, y, 300, 106)], 'edges': []}
        y+=100
        return res
    def __repr__(self) -> str:
        return f'{self.value}'

class BinOpAst(Ast) :
    BINOP_NAMES = {
        '+': 'Add',
        '-': 'Sub',
        '*': 'Mul',
        '/': 'Div',
        '%': 'Mod',
        '==': 'Eq',
        '!=': 'Not',
        '>': 'Gt',
        '<': 'Lt',
        '>=': 'Ge',
        '<=': 'Le',
        '&&': 'And',
        '||': 'Or'
    }

    def __init__(self, left:Ast, op:str, right:Ast) -> None:
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def to_json(self) :
        global y
        nodes = [Node(self.id, 'BinOp', {'name': BinOpAst.BINOP_NAMES[self.op]}, 0, y, 121, 66)]
        y+=100
        edges = [
            Edge(self.left.id, 'output', self.id, 'input1'),
            Edge(self.right.id, 'output', self.id, 'input2')
        ]
        children = [
            self.left.to_json(),
            self.right.to_json()
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'{self.left} {self.op} {self.right}'

class BodyAst(Ast) :
    def __init__(self, statements:[Ast]) -> None:
        super().__init__()
        self.statements = statements
        self.id = None
        i = 0
        while i < len(statements) :
            statement = statements[i]
            if not isinstance(statement, CommentAst) :
                self.id = statement.id
                break
            i += 1

    def to_json(self) :
        nodes = []
        edges = []
        for statement in self.statements :
            nodes += statement.to_json()['nodes']
            edges += statement.to_json()['edges']
        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return '{' + ';'.join(str(statement) for statement in self.statements) + '}'

class FunDecAst(Ast) :
    def __init__(self, type:TokenType, name:str, parameters:[Ast], body:BodyAst) -> None:
        if name != 'main' :
            Exception('Only main function is supported')
        super().__init__()
        self.type = type
        self.name = name
        self.parameters = parameters
        self.body = body

    def to_json(self):
        global y
        nodes = [Node('START', 'Input', {'name': 'Start'}, 0, y, 105, 86)]
        y += 100
        edges = []

        if len(self.body.statements) != 0 :
            edges.append(Edge('START', 'outflow', self.body.id, 'inflow'))
            children = [
                 self.body.to_json()
            ]

            for child in children :
                nodes += child['nodes']
                edges += child['edges']
        return  {'nodes': nodes , 'edges': edges}

    def __repr__(self) -> str:
        return f'{self.type} {self.name}({self.parameters}) {self.body}'

class CommentAst(Ast) :
    def __init__(self, comment:str) -> None:
        super().__init__()
        self.comment = comment

    def to_json(self) :
        global y
        res =  {'nodes': [Node(self.id, 'Comment', {'name': self.comment}, 0, y, 0, 0)], 'edges': []}
        y+=100
        return res
    def __repr__(self) -> str:
        return f'{self.comment}'

class FunCallAst(Ast) :
    def __init__(self, name:str, parameters:[Ast]) -> None:
        super().__init__()
        self.name = name
        #self.parameters = parameters
        if name != 'printf' :
            Exception('Only printf function is supported')
        if len(parameters) != 2 :
            Exception('printf function must have 2 parameters')

        self.parameter = parameters[1]

    def to_json(self) :
        global y
        nodes = [Node(self.id, 'Print', {'name': 'Print'}, 0, y, 136, 62)]
        y+=100
        edges = [
            Edge(self.parameter.id, 'output',self.id, 'input')
        ]
        children = [
            self.parameter.to_json()
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}
