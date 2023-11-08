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

class TokenBinOperator(Token) :
    def __init__(self, operator):
        super().__init__('BIN_OPERATOR', operator)

class TokenUnOperator(Token) :
    def __init__(self, operator):
        super().__init__('UN_OPERATOR', operator)

class TokenType(Token) :
    def __init__(self, type) :
        super().__init__('TYPE', type.name)
        self.type = type

class TokenWhile(Token) :
    def __init__(self) :
        super().__init__('WHILE', 'while')

class TokenIf(Token) :
    def __init__(self) :
        super().__init__('IF', 'if')

class TokenElse(Token) :
    def __init__(self) :
        super().__init__('ELSE', 'else')


class Types(StrEnum) :
    VOID=auto()
    INT=auto()
    CHAR=auto()
    FLOAT=auto()
    DOUBLE=auto()
