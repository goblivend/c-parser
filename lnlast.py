from nodes import Node, Edge
from tokens import Type

id=0

class Ast :
    def __init__(self) -> None:
        global id
        self.id = id
        id+=1
        pass

    def to_json(self) :
        return {'nodes': None, 'edges': None}

class IfAst(Ast) :
    def __init__(self, cond:Ast, ifast:Ast, elseast:Ast, afterast:Ast) -> None:
        super().__init__()
        self.cond = cond
        self.ifast = ifast
        self.elseast = elseast
        self.afterast = afterast

    def to_json(self) :
        nodes = [Node(self.id, 'If', {'name':'If'}, 0, 0, 0, 0)]
        edges = [
            Edge(self.id, 'input', self.cond.id, 'output'),
            Edge(self.id, 'outflow1', self.ifast.id, 'inflow'),
            Edge(self.id, 'outflow2', self.elseast.id, 'inflow'),
            Edge(self.id, 'outflow3', self.afterast.id, 'inflow')
        ]
        children = [
            self.cond.to_json(),
            self.ifast.to_json(),
            self.elseast.to_json(),
            self.afterast.to_json()
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}


class WhileAst(Ast) :
    def __init__(self, cond:Ast, bodyast:Ast, afterast:Ast) -> None:
        super().__init__()
        self.cond = cond
        self.bodyast = bodyast
        self.afterast = afterast

    def to_json(self) :
        nodes = [Node(self.id, 'If', {'name':'While'}, 0, 0, 0, 0)]
        edges = [
            Edge(self.id, 'input', self.cond.id, 'output'),
            Edge(self.id, 'outflow1', self.bodyast.id, 'inflow'),
            Edge(self.id, 'outflow2', self.afterast.id, 'inflow')
        ]
        children = [
            self.cond.to_json(),
            self.bodyast.to_json(),
            self.afterast.to_json()
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

class VarDecAst(Ast) :
    def __init__(self, type:Type, name:str, value:Ast) -> None:
        super().__init__()
        self.type = type
        self.name = name
        self.value = value

    def to_json(self) :
        nodes = [Node(self.id, 'VarDec', 0, 0, 0, 0)]
        edges = [
            Edge(self.id, 'input', self.value.id, 'output')
        ]
        children = [
            self.value.to_json()
        ]

        for child in children :
            nodes += child['nodes']
            edges += child['edges']

        return {'nodes': nodes, 'edges': edges}

class VarAst(Ast) :
    def __init__(self, name:str) -> None:
        super().__init__()
        self.name = name

    def to_json(self) :
        return {'nodes': [Node(self.id, 'Var', 0, 0, 0, 0)], 'edges': []}

class LiteralAst(Ast) :
    def __init__(self, value, type:Type) -> None:
        super().__init__()
        self.value = value
        self.type = type

    def to_json(self) :
        return {'nodes': [Node(self.id, 'Literal', {'name': 'Literal', 'type': self.type.name, 'value': str(self.value)}, 0, 0, 0, 0)], 'edges': []}
