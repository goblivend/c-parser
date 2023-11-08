from tokens import Token,TokenLiteral,TokenComment,TokenName,TokenOperator,TokenType,Types
from lnlast import Ast,IfAst,WhileAst,VarDecAst,VarAst,FunDecAst,CommentAst,BodyAst,LiteralAst,FunCallAst

class Parser :
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = 0
        self.nb_tokens = len(tokens)

    def _get_current(self) :
        if self.index >= self.nb_tokens :
            return None
        return self.tokens[self.index]

    def _next(self) :
        self.index += 1
        return self._get_current()

    def _parse_body(self) :
        body = []
        while True :
            print('Parsing body')
            element = self._parse()
            print(element)
            if element == None :
                break
            body.append(element)
            if self._get_current() == Token('PONCTUATION', ';') :
                self._next()
                continue
            elif not isinstance(body[-1], CommentAst) and not isinstance(body[-1], BodyAst) and not isinstance(body[-1], IfAst) and not isinstance(body[-1], WhileAst) and not isinstance(body[-1], FunDecAst) :
                break
        return BodyAst(body)

    def _parse_func_body(self) :
        if self._next() != Token('PARA', '{') :
            Exception('Body must start with {')
        body =  self._parse_body()
        if self._get_current() != Token('PARA', '}') :
            Exception('Body must end with }')
        self._next()
        return body

    def _parse_function_dec(self, type:TokenType, name:TokenName) :
        parameters = []
        self._next()
        while self._get_current() != Token('PARA', ')') :
            print('Parsing parameters', self._get_current())
            parameters.append(self._parse())
        self._next()
        return FunDecAst(type, name, parameters, self._parse_func_body())

    def _parse_variable(self, type:TokenType, name:TokenName) :
        token = self._get_current()
        if token == TokenOperator('=') :
            return VarDecAst(type, name, self._parse())
        elif token == Token('PONCUTATION', ',') :
            return None # No Need to declare Variables in LNL

    def _parse_function_or_variable(self, type:TokenType, name: TokenName) :
        if self._next() == Token('PARA', '(') :
            return self._parse_function_dec(type, name)
        return self._parse_variable(type, name)

    def _parse_type(self) :
        type_token = self._get_current()
        next_token = self._next()
        if next_token == None :
            return None
        elif isinstance(next_token, TokenName) :
            return self._parse_function_or_variable(type_token, next_token)
        elif next_token == Token('PARA', ')') :
            return None

    def _parse_fun_call(self) :
        name = self._get_current()
        if self._next() != Token('PARA', '(') :
            Exception('Function call must start with (')

        self._next()
        parameters = []
        while self._get_current() != Token('PARA', ')') and self._get_current() != None :
            print('Parsing parameters', self._get_current())
            parameters.append(self._parse())
            if self._get_current() == Token('PONCTUATION', ',') :
                self._next()

        if self._get_current() != Token('PARA', ')') :
            Exception('Function call must end with )')
        self._next()
        return FunCallAst(name, parameters)


    def _parse(self) :
        token = self._get_current()
        if token == None :
            return None
        elif isinstance(token, TokenType) :
            return self._parse_type()
        elif isinstance(token, TokenComment) :
            self._next()
            return CommentAst(token.value)
        elif isinstance(token, TokenName) :
            return self._parse_fun_call()
        elif isinstance(token, TokenLiteral) :
            self._next()
            return LiteralAst(token.value, token.type)


    def parse(self) :
        return self._parse_body()
