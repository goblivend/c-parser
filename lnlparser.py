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
        return self.tokens[self.index]

    def _next(self) :
        self.index += 1
        self.current = self._get_current()
        return self.current

    def _parse_function_dec(self, type:TokenType, name:TokenName) :
        parameters = []
        self._next()
        while self.current != Token('PARA', ')') :
            param = self._parse_expr()
            if param != None :
                parameters.append(param)
        self._next()
        return FunDecAst(type, name.value, parameters, self._parse_curled_body())

    def _parse_function_or_variable(self, type:TokenType, name: TokenName) :
        if self._next() == Token('PARA', '(') :
            return self._parse_function_dec(type, name)
        return self._parse_variable(type, name)

    def _parse_type(self) :
        type_token = self.current
        next_token = self._next()
        if next_token == None :
            return None
        elif isinstance(next_token, TokenName) :
            return self._parse_function_or_variable(type_token, next_token)
        elif next_token == Token('PARA', ')') :
            return None

    def _parse_if(self) :
        self._next()
        condition = self._parse_parenthesis()
        body = self._parse_curled_or_line()
        else_body = None
        if isinstance(self.current, TokenElse)  :
            self._next()
            else_body = self._parse_curled_or_line()
        return IfAst(condition, body, else_body)

    def _parse_while(self) :
        self._next()
        condition = self._parse_parenthesis()
        body = self._parse_curled_or_line()
        return WhileAst(condition, body)

    def _parse_curled_or_line(self) :
        return self._parse_curled_body() if self.current == Token('PARA', '{') else self._parse_ari_expr()

    def _parse_parenthesis(self) :
        self._next()
        expr = self._parse_ari_expr()
        if self.current != Token('PARA', ')') :
            raise Exception('Parenthesis must end with )')
        self._next()
        return expr

    def _parse_variable(self, type:TokenType, name:TokenName) :
        if self.current == TokenBinOperator('=') :
            self._next()
            val = self._parse_ari_expr()
            return VarDecAst(type, name.value, val)
        elif self.current == Token('PONCUTATION', ',') :
            self.variables[name.value] = type
            return None # No Need to declare Variables in LNL
        elif self.current == Token('PONCTUATION', ';') :
            self.variables[name.value] = type
            return None

    def _parse_fun_call(self, name:TokenName) :
        if self.current != Token('PARA', '(') :
            raise Exception('Function call must start with (, not ' + str(self.current) + ' at ' + str(self.index))
        self._next()
        parameters = []
        while self.current != Token('PARA', ')') and self.current != None :
            if self.current == Token('PONCTUATION', ';') :
                raise Exception('Function call must end with ), not ;')
            res = self._parse_ari_expr()
            if res is not None:
                parameters.append(res)

            if self.current == Token('PONCTUATION', ',') :
                self._next()

        if self.current != Token('PARA', ')') :
            raise Exception('Function call must end with ), ')
        self._next()
        return FunCallAst(name.value, parameters)

    def _parse_fun_call_or_var(self) :
        name = self.current
        next = self._next()
        if next == Token('PARA', '(') :
            return self._parse_fun_call(name)
        elif next == TokenBinOperator('=') :
            return self._parse_variable(self.variables[name.value], name)
        else :
            return VarAst(name.value)

    def _parse_expr(self) :
        token = self.current
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
            return self._parse_parenthesis()

    def _parse_ari_expr(self) :
        ast = self._parse_expr()
        while isinstance(self.current, TokenBinOperator) or isinstance(self.current, TokenUnOperator) :
            op = self.current
            self._next()
            right = self._parse_expr()
            if op.value == '>=' or op.value == '<=':
                compare = BinOpAst(ast, op.value[0], right)
                equal = BinOpAst(ast.copy(), '==', right.copy())
                return BinOpAst(compare, '||', equal)
            ast = BinOpAst(ast, op.value, right)
        return ast

    def _parse(self) :
        return self._parse_ari_expr()

    def _parse_curled_body(self) :
        if self.current != Token('PARA', '{') :
            raise Exception('Curled body must end with {')
        self._next()
        body = []
        while self.current != Token('PARA', '}') and self.current != None :
            element = self._parse()
            if element != None :
                body.append(element)
            if self.current == Token('PONCTUATION', ';') :
                self._next()
        if self.current != Token('PARA', '}') :
            raise Exception('Curled body must end with }')
        self._next()
        return BodyAst(body)

    def _parse_body(self) :
        body = []
        while True :
            element = self._parse()
            if element != None:
                body.append(element)
            if self.current == None :
                break
            if self.current == Token('PONCTUATION', ';') :
                self._next()
                continue
        return BodyAst(body)

    def _needs_semi_column(ast: Ast):
        return not isinstance(ast, CommentAst) and not isinstance(ast, BodyAst) and not isinstance(ast, IfAst) and not isinstance(ast, WhileAst) and not isinstance(ast, FunDecAst)

    def parse(self) :
        return self._parse_body()
