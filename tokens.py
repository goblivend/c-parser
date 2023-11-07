from enum import StrEnum,auto

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

class Comment(Token) :
    def __init__(self, message):
        super().__init__('COMMENT', message)

class Type(Token) :
    def __init__(self, type) :
        super().__init__('TYPE', type.name)
        self.type = type

class Types(StrEnum) :
    VOID=auto()
    INT=auto()
    CHAR=auto()
    FLOAT=auto()
    DOUBLE=auto()
