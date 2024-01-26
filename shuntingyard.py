from tokens import *
from lnlast import *

def _generate_ast(left: Ast, op:Token, right: Ast) :
    if op.value == '>=' or op.value == '<=':
        compare = BinOpAst(left, op.value[0], right)
        equal = BinOpAst(left.copy(), '==', right.copy())
        return BinOpAst(compare, '||', equal)
    else :
        return BinOpAst(left, op.value, right)

def _prefix_to_ast(tokens) :
    tok = tokens.pop(0)
    if isinstance(tok, Ast) or tok == None :
        return tok
    elif tok == TokenUnOperator('-') :
        right = _prefix_to_ast(tokens)
        if isinstance(right, LiteralAst) :
            right.value = -right.value
            return right
        return _generate_ast(LiteralAst(0, TokenType(Types.Int)), tok, right)
    elif tok == TokenUnOperator('++') :
        right = _prefix_to_ast(tokens)
        return VarDecAst(right.type, right.name, _generate_ast(right, TokenBinOperator('+'), LiteralAst(1, TokenType(Types.Int))))
    elif tok == TokenUnOperator('--') :
        right = _prefix_to_ast(tokens)
        return VarDecAst(right.type, right.name, _generate_ast(right, TokenBinOperator('-'), LiteralAst(1, TokenType(Types.Int))))
    elif tok == TokenUnOperator('!') :
        right = _prefix_to_ast(tokens)
        return _generate_ast(LiteralAst(0, TokenType(Types.Int)), TokenBinOperator('=='), right)
    elif tok.value[0] not in ['!', '='] and len(tok.value) >= 2 and tok.value[1] == '=' :
        left = _prefix_to_ast(tokens)
        right = _prefix_to_ast(tokens)
        return VarDecAst(left.type, left.name, _generate_ast(left, TokenBinOperator(tok.value[0]), right))

    left = _prefix_to_ast(tokens)
    right =_prefix_to_ast(tokens)

    return _generate_ast(left, tok, right)

def _infix_to_prefix(tokens) :
    precedence = {
        '+=': 2,
        '-=': 2,
        '*=': 2,
        '/=': 2,
        '^=': 2,
        '&=': 2,
        '|=': 2,
        '==': 3,
        '!=': 3,
        '<=': 3,
        '>=': 3,
        '<': 3,
        '>': 3,
        '&&': 4,
        '||': 4,
        '|': 5,
        '^': 6,
        '&': 7,
        '<<': 8,
        '>>': 8,
        '+': 9,
        '-': 9,
        '*': 10,
        '/': 10,
        '%': 10,
        '!': 11,
        '~': 11,
        '++': 11,
        '--': 11,
    }
    output = []
    operators = []
    for tok in tokens :
        if isinstance(tok, TokenBinOperator) or isinstance(tok, TokenUnOperator):
            while len(operators) > 0 and precedence[operators[-1].value] >= precedence[tok.value] :
                output.insert(0, operators.pop())
            operators.append(tok)
        else :
            output.insert(0, tok)
    while len(operators) > 0 :
        output.insert(0, operators.pop())
    print(output)
    return output

def evaluate(tokens) :
    return _prefix_to_ast(_infix_to_prefix(tokens))
