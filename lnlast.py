from nodes import Node, Edge
from tokens import TokenType

id = 0


class Ast:
    def __init__(self) -> None:
        global id
        self.id = f'node_{id}'
        id += 1
        pass

    def copy(self):
        return Ast()

    def to_json(self, coords):
        return {'nodes': None, 'edges': None}

    def outflow(self):
        return 'outflow'


class IfAst(Ast):
    def __init__(self, cond: Ast, ifast: Ast, elseast: Ast) -> None:
        super().__init__()
        self.cond = cond
        self.ifast = ifast
        self.elseast = elseast

    def copy(self):
        return IfAst(self.cond.copy(), self.ifast.copy(), self.elseast.copy())

    def outflow(self):
        return 'outflow3'

    def to_json(self, coords):
        nodes = [Node(self.id, 'If', {'name': 'If'}, coords[0], coords[1], 0, 106)]
        edges = [
            Edge(self.cond.id, 'output', self.id, 'input'),
            Edge(self.ifast.id, 'inflow', self.id, 'outflow1'),
            Edge(self.elseast.id, 'inflow', self.id, 'outflow2'),
        ]
        cond_coords = [coords[0] - 200, coords[1]]
        if_coords = [coords[0] - 100, coords[1] - 150]
        else_coords = [coords[0] + 100, coords[1] - 150]

        children = [
            self.cond.to_json(cond_coords),
            self.ifast.to_json(if_coords),
            self.elseast.to_json(else_coords)
        ]

        coords[1] = max(if_coords[1], else_coords[1])

        for child in children:
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'if({self.cond}) {self.ifast} else {self.elseast}'


class WhileAst(Ast):
    def __init__(self, cond: Ast, bodyast: Ast) -> None:
        super().__init__()
        self.cond = cond
        self.bodyast = bodyast

    def copy(self):
        return WhileAst(self.cond.copy(), self.bodyast.copy())

    def outflow(self):
        return 'outflow2'

    def to_json(self, coords):
        nodes = [Node(self.id, 'While', {'name': 'While'}, coords[0], coords[1], 0, 106)]
        edges = [
            Edge(self.cond.id, 'output', self.id, 'input'),
            Edge(self.id, 'outflow1', self.bodyast.id, 'inflow'),
        ]
        cond_coords = [coords[0] - 200, coords[1]]
        coords[1] += 150
        children = [
            self.cond.to_json(cond_coords),
            self.bodyast.to_json(coords),
        ]

        for child in children:
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'while({self.cond}) {self.bodyast}'


class VarDecAst(Ast):
    def __init__(self, type: TokenType, name: str, value: Ast) -> None:
        super().__init__()
        self.type = type
        self.name = name
        self.value = value

    def copy(self):
        return VarDecAst(self.type, self.name, self.value.copy())

    def to_json(self, coords):
        nodes = [Node(self.id, 'Variable', {'name': 'Variable', 'value': self.name}, coords[0], coords[1], 0, 0)]
        edges = [
            Edge(self.value.id, 'output', self.id, 'input')
        ]
        value_coord = [coords[0] - 200, coords[1]]
        children = [
            self.value.to_json(value_coord)
        ]

        for child in children:
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'{self.type} {self.name} = {self.value}'


class VarAst(Ast):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def copy(self):
        return VarAst(self.name)

    def to_json(self, coords):
        res = {
            'nodes': [Node(self.id, 'Variable', {'name': 'Variable', 'value': self.name}, coords[0], coords[1], 0, 0)],
            'edges': []}
        return res

    def __repr__(self) -> str:
        return f'{self.name}'


class LiteralAst(Ast):
    def __init__(self, value, type: TokenType) -> None:
        super().__init__()
        self.value = value
        self.type = type

    def copy(self):
        return LiteralAst(self.value, self.type)

    def to_json(self, coords):
        res = {'nodes': [
            Node(self.id, 'Literal', {'name': 'Literal', 'type': self.type.name, 'value': str(self.value)}, coords[0],
                 coords[1], 300,
                 106)], 'edges': []}
        return res

    def __repr__(self) -> str:
        return f'{self.value}'


class BinOpAst(Ast):
    BINOP_NAMES = {
        '+': 'Add',
        '-': 'Sub',
        '*': 'Mult',
        '/': 'Div',
        '%': 'Mod',
        '==': 'Equal',
        '!=': 'Not',
        '>': 'Greater',
        '<': 'Less',
        '>=': 'Greater',
        '<=': 'Less',
        '&&': 'And',
        '||': 'Or'
    }

    def __init__(self, left: Ast, op: str, right: Ast) -> None:
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def copy(self):
        return BinOpAst(self.left.copy(), self.op, self.right.copy())

    def to_json(self, coords):
        nodes = [Node(self.id, 'BinOpNode', {'name': BinOpAst.BINOP_NAMES[self.op]}, coords[0], coords[1], 121, 66)]
        edges = [
            Edge(self.left.id, 'output', self.id, 'input1'),
            Edge(self.right.id, 'output', self.id, 'input2')
        ]
        left_coords = [coords[0] - 400, coords[1] - 60]
        right_coords = [coords[0] - 400, coords[1] + 60]

        children = [
            self.left.to_json(left_coords),
            self.right.to_json(right_coords)
        ]

        for child in children:
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return f'{self.left} {self.op} {self.right}'


class BodyAst(Ast):
    def __init__(self, statements: [Ast]) -> None:
        super().__init__()
        self.statements = statements
        self.id = None
        i = 0
        while i < len(statements):
            statement = statements[i]
            if not isinstance(statement, CommentAst):
                self.id = statement.id
                break
            i += 1

    def copy(self):
        return BodyAst([statement.copy() for statement in self.statements])

    def to_json(self, coords):
        nodes = []
        edges = []
        last: Ast = None
        for line in self.statements:
            statement = line.to_json(coords)
            if last is not None:
                edges.append(Edge(last.id, last.outflow(), line.id, 'inflow'))
            last = line
            coords[1] += 100
            nodes += statement['nodes']
            edges += statement['edges']
        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        return '{' + ';'.join(str(statement) for statement in self.statements) + '}'


class FunDecAst(Ast):
    def __init__(self, type: TokenType, name: str, parameters: [Ast], body: BodyAst) -> None:
        if name != 'main':
            raise Exception('Only main function is supported :' + name)
        if parameters == None:
            raise Exception('Main function must have parameters')
        super().__init__()
        self.type = type
        self.name = name
        self.parameters = parameters
        self.body = body

    def copy(self):
        return FunDecAst(self.type, self.name, [parameter.copy() for parameter in self.parameters], self.body.copy())

    def to_json(self, coords):
        nodes = [Node('START', 'Input', {'name': 'Start'}, coords[0], coords[1], 105, 86)]
        edges = []

        if len(self.body.statements) != 0:
            edges.append(Edge('START', 'outflow', self.body.id, 'inflow'))
            coords[1] += 100
            children = [
                self.body.to_json(coords)
            ]

            for child in children:
                nodes += child['nodes']
                edges += child['edges']
        return {'nodes': nodes, 'edges': edges}

    def __repr__(self) -> str:
        params = ', '.join(self.parameters) if len(self.parameters) != 0 else 'void'
        return f'{self.type} {self.name}(' + params + f') {self.body}'


class CommentAst(Ast):
    def __init__(self, comment: str) -> None:
        super().__init__()
        self.comment = comment

    def copy(self):
        return CommentAst(self.comment)

    def to_json(self, coords):
        res = {'nodes': [Node(self.id, 'Comment', {'name': self.comment}, coords[0], coords[1], 233, 66)], 'edges': []}
        return res

    def __repr__(self) -> str:
        return f'{self.comment}'


class FunCallAst(Ast):
    def __init__(self, name: str, parameters: [Ast]) -> None:
        super().__init__()
        self.name = name
        if name != 'printf':
            raise Exception('Only printf function is supported')
        if len(parameters) != 2:
            raise Exception('printf function must have 2 parameters : ' + str(parameters))

        self.parameters = parameters[1:]

    def copy(self):
        return FunCallAst(self.name, [parameter.copy() for parameter in self.parameters])

    def to_json(self, coords):
        nodes = [Node(self.id, 'Print', {'name': 'Print'}, coords[0], coords[1], 136, 62)]
        edges = [
            Edge(self.parameters[0].id, 'output', self.id, 'input')
        ]
        children = [
            self.parameters[0].to_json([coords[0] - 400, coords[1]])
        ]

        for child in children:
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

    def __repr__(self):
        return f'{self.name}({self.parameters[0]})'
