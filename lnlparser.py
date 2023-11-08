from tokens import Token,TokenLiteral,TokenComment,TokenName,TokenBinOperator,TokenUnOperator,TokenWhile,TokenIf,TokenElse,TokenType,Types
from lnlast import Ast,IfAst,WhileAst,VarDecAst,VarAst,FunDecAst,CommentAst,BodyAst,LiteralAst,FunCallAst,BinOpAst

class Parser :
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = 0
        self.nb_tokens = len(tokens)
        self.variables = {}

    def _get_current(self) :
        if self.index >= self.nb_tokens :
            return None
        return self.tokens[self.index]

    def _next(self) :
        self.index += 1
        return self._get_current()

    def _parse_func_body(self) :
        if self._get_current() != Token('PARA', '{') :
            raise Exception('Body must start with {, not ' + str(self._get_current()) + ' at ' + str(self.index))
        self._next()
        body =  self._parse_body()
        if self._get_current() != Token('PARA', '}') :
            raise Exception('Body must end with }, not ' + str(self._get_current()) + ' at ' + str(self.index))
        self._next()
        return body

    def _parse_function_dec(self, type:TokenType, name:TokenName) :
        parameters = []
        self._next()
        while self._get_current() != Token('PARA', ')') :
            print('Parsing dec parameters', self._get_current())
            parameters.append(self._parse())
        self._next()
        return FunDecAst(type, name, parameters, self._parse_func_body())

    def _parse_variable(self, type:TokenType, name:TokenName) :
        print('Parsing variable', type, name)
        token = self._get_current()
        if token == TokenBinOperator('=') :
            print('Parsing variable with value')
            self._next()
            val = self._parse()
            return VarDecAst(type, name, val)
        elif token == Token('PONCUTATION', ',') :
            self.variables[name.value] = type
            return None # No Need to declare Variables in LNL
        elif token == Token('PONCTUATION', ';') :
            self.variables[name.value] = type
            return None

    def _parse_function_or_variable(self, type:TokenType, name: TokenName) :
        if self._next() == Token('PARA', '(') :
            return self._parse_function_dec(type, name)
        return self._parse_variable(type, name)

    def _parse_type(self) :
        type_token = self._get_current()
        next_token = self._next()
        print('Parsing type')
        if next_token == None :
            return None
        elif isinstance(next_token, TokenName) :
            return self._parse_function_or_variable(type_token, next_token)
        elif next_token == Token('PARA', ')') :
            return None

    def _parse_fun_call(self, name:TokenName) :
        print('Parsing function call', name)
        next = self._get_current()
        print('Next :', next)
        if next != Token('PARA', '(') :
            raise Exception('Function call must start with (, not ' + str(next) + ' at ' + str(self.index))

        self._next()
        parameters = []
        while self._get_current() != Token('PARA', ')') and self._get_current() != None :
            print('Parsing parameters for call', self._get_current())
            if self._get_current() == Token('PONCTUATION', ';') :
                raise Exception('Function call must end with ), not ;')
            res = self._parse()
            if res != None :
                parameters.append(res)

            if self._get_current() == Token('PONCTUATION', ',') :
                self._next()

        if self._get_current() != Token('PARA', ')') :
            raise Exception('Function call must end with ), ')
        self._next()
        return FunCallAst(name, parameters)

    def _parse_parenthesis(self) :
        self._next()
        expr = self._parse()
        if self._get_current() != Token('PARA', ')') :
            raise Exception('Parenthesis must end with )')
        self._next()
        return expr

    def _parse_fun_call_or_var(self) :
        name = self._get_current()
        next = self._next()
        if next == Token('PARA', '(') :
            return self._parse_fun_call(name)
        elif next == TokenBinOperator('=') :
            return self._parse_variable(self.variables[name.value], name)

    def _parse_while(self) :
        print('Parsing while')
        self._next()
        condition = self._parse_parenthesis()
        body = self._parse_body()
        return WhileAst(condition, body)

    def _parse_if(self) :
        print('Parsing if')
        self._next()
        condition = self._parse_parenthesis()
        body = self._parse_body()
        else_body = None
        if isinstance(self._get_current(), TokenElse)  :
            self._next()
            else_body = self._parse_body()

        return IfAst(condition, body, else_body)

    def _parse_switch(self) :
        token = self._get_current()
        print('>>>>>>>>>>')
        print('=============    Parsing', token)
        print('<<<<<<<<<<')
        if token == None :
            return None
        elif isinstance(token, TokenType) :
            return self._parse_type()
        elif isinstance(token, TokenComment) :
            self._next()
            return CommentAst(token.value)
        elif isinstance(token, TokenName) :
            return self._parse_fun_call_or_var()
        elif isinstance(token, TokenWhile) :
            return self._parse_while()
        elif isinstance(token, TokenLiteral) :
            self._next()
            return LiteralAst(token.value, token.type)
        elif token == Token('PARA', '(') :
            print('Parsing parenthesis')
            return self._parse_parenthesis()

    def _parse(self) :
        return self._parse_switch()

    def _parse_body(self) :
        body = []
        while True :
            print('Parsing body')
            element = self._parse()
            if self._get_current() == None :
                break
            if element != None :
                body.append(element)
            if self._get_current() == Token('PONCTUATION', ';') :
                self._next()
                continue
            elif not isinstance(body[-1], CommentAst) and not isinstance(body[-1], BodyAst) and not isinstance(body[-1], IfAst) and not isinstance(body[-1], WhileAst) and not isinstance(body[-1], FunDecAst) :
                break
        return BodyAst(body)

    def parse(self) :
        return self._parse_body()
