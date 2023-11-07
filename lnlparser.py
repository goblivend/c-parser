from tokens import Token,Literal,Comment,Type,Types
from lnlast import Ast,IfAst,WhileAst

class Parser :
    def __init__(self, tokens) -> None:
        self.tokens = tokens

    def parse(self) :
        pass
