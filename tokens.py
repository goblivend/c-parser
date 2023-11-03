import enum

class Token :
    def __init__(self, name, value) :
        self.name = name
        self.value = value

    def __repr__(self) :
        return f'<{self.name}:{self.value}>'

class Literal(Token) :
    def __init__(self, type, value):
        super().__init__('LITERAL', value)
        self.type = type

class Types(str, enum.Enum) :
    VOID='void'
    INT='int'
    CHAR='char'
    FLOAT='float'
    DOUBLE='double'
