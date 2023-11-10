from tokens import Token,TokenLiteral,TokenComment,TokenName,TokenBinOperator,TokenUnOperator,TokenWhile,TokenIf,TokenElse,TokenType,Types
from lnlast import Ast,IfAst,WhileAst,VarDecAst,VarAst,FunDecAst,CommentAst,BodyAst,LiteralAst,FunCallAst,BinOpAst

class Parser :
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = 0
        self.nb_tokens = len(tokens)
        self.variables = {}
        self.current = self.tokens[self.index] if self.index < self.nb_tokens else None

    def _get_current(self) :
        if self.index >= self.nb_tokens :
            return None
        self.tokens[self.index]

    def _next(self) :
        self.index += 1
        self.current = self._get_current()
        return self.current

    def _parse_TODO(self) :
        pass

    def _parse_function_dec(self, type:TokenType, name:TokenName) :
        parameters = []
        self._next()
        while self.current != Token('PARA', ')') :
            print('Parsing dec parameters', self.current)
            parameters.append(self._parse_TODO())
        self._next()
        return FunDecAst(type, name, parameters, self._parse_TODO())

    def _parse_variable(self, type:TokenType, name:TokenName) :
        print('Parsing variable', type, name)
        if self.current == TokenBinOperator('=') :
            print('Parsing variable with value')
            self._next()
            val = self._parse_TODO()
            return VarDecAst(type, name, val)
        elif self.current == Token('PONCUTATION', ',') :
            self.variables[name.value] = type
            return None # No Need to declare Variables in LNL
        elif self.current == Token('PONCTUATION', ';') :
            self.variables[name.value] = type
            return None

    def _parse_function_or_variable(self, type:TokenType, name: TokenName) :
        if self._next() == Token('PARA', '(') :
            return self._parse_function_dec(type, name)
        return self._parse_variable(type, name)

    def _parse_type(self) :
        type_token = self.current
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
        print('Next :', self.current)
        if self.current != Token('PARA', '(') :
            raise Exception('Function call must start with (, not ' + str(self.current) + ' at ' + str(self.index))

        self._next()
        parameters = []
        while self.current != Token('PARA', ')') and self.current != None :
            print('Parsing parameters for call', self.current)
            if self.current == Token('PONCTUATION', ';') :
                raise Exception('Function call must end with ), not ;')
            res = self._parse_TODO()
            if res != None :
                parameters.append(res)

            if self.current == Token('PONCTUATION', ',') :
                self._next()

        if self.current != Token('PARA', ')') :
            raise Exception('Function call must end with ), ')
        self._next()
        return FunCallAst(name, parameters)

    def _parse_parenthesis(self) :
        self._next()
        expr = self._parse_TODO()
        if self.current != Token('PARA', ')') :
            raise Exception('Parenthesis must end with )')
        self._next()
        return expr

    def _parse_fun_call_or_var(self) :
        name = self.current
        next = self._next()
        if next == Token('PARA', '(') :
            return self._parse_fun_call(name)
        elif next == TokenBinOperator('=') :
            return self._parse_variable(self.variables[name.value], name)

    def _parse_while(self) :
        print('Parsing while')
        self._next()
        condition = self._parse_parenthesis()
        body = self._parse_TODO()
        return WhileAst(condition, body)

    def _parse_if(self) :
        print('Parsing if')
        self._next()
        condition = self._parse_parenthesis()
        # TODO : If Not `{` then parse only one line
        body = self._parse_TODO()
        else_body = None
        if isinstance(self.current, TokenElse)  :
            self._next()
            # TODO : If Not `{` then parse only one line
            else_body = self._parse_TODO()

        return IfAst(condition, body, else_body)

    def _parse_switch(self) :
        print('>>>>>>>>>>')
        print('=============    Parsing', self.current)
        print('<<<<<<<<<<')
        if self.current == None :
            return None
        elif isinstance(self.current, TokenType) :
            return self._parse_type()
        elif isinstance(self.current, TokenComment) :
            self._next()
            return CommentAst(self.current.value)
        elif isinstance(self.current, TokenName) :
            return self._parse_fun_call_or_var()
        elif isinstance(self.current, TokenWhile) :
            return self._parse_while()
        elif isinstance(self.current, TokenLiteral) :
            self._next()
            return LiteralAst(self.current.value, self.current.type)
        elif self.current == Token('PARA', '(') :
            print('Parsing parenthesis')
            return self._parse_parenthesis()

    def _parse(self) :
        # If not in fun_dec : need macro or type
        # If in fun_dec : need macro or type or variable or expression (arithmetic, function call, parenthesis, etc.)
        # If in parenthesis : need expression
        # If in variable : need `=` + expression or nothing
        return self._parse_switch()

    def _parse_body(self) :
        body = []
        while True :
            print('Parsing body')
            element = self._parse()
            if self.current == None :
                break
            if element != None :
                body.append(element)
            if self.current == Token('PONCTUATION', ';') :
                self._next()
                continue
            elif not isinstance(body[-1], CommentAst) and not isinstance(body[-1], BodyAst) and not isinstance(body[-1], IfAst) and not isinstance(body[-1], WhileAst) and not isinstance(body[-1], FunDecAst) :
                break
        return BodyAst(body)

    def parse(self) :
        return self._parse_body()
