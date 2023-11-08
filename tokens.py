from enum import StrEnum,auto

class Token :
    def __init__(self, name, value) :
        self.name = name
        self.value = value

    def __repr__(self) :
        return f'<{self.name}:{self.value}>'

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Token) :
            return self.name == __value.name and self.value == __value.value
        return False

class TokenLiteral(Token) :
    def __init__(self, type, value):
        super().__init__('LITERAL', value)
        self.type = type

class TokenComment(Token) :
    def __init__(self, message):
        super().__init__('COMMENT', message)

class TokenName(Token) :
    def __init__(self, name):
        super().__init__('NAME', name)

class TokenOperator(Token) :
    def __init__(self, operator):
        super().__init__('OPERATOR', operator)

class TokenType(Token) :
    def __init__(self, type) :
        super().__init__('TYPE', type.name)
        self.type = type



class Types(StrEnum) :
    VOID=auto()
    INT=auto()
    CHAR=auto()
    FLOAT=auto()
    DOUBLE=auto()
