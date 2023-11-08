#!/usr/bin/python3.11

from lexer import Lexer
from lnlparser import Parser
from nodes import NodeEncoder
from json import dumps

INCLUDES = [
    '#include <stdio.h>\n',
    '#include <stdlib.h>\n',
    '#include <string.h>\n'
]

def transpile(inputFile:str, outputFile:str):
    with open(inputFile, 'r') as f :
        lines = f.readlines()

    print(lines)
    if not checkFeatures(lines) :
        exit(2)

    content = ''.join(getContent(lines))
    lexer = Lexer(content)
    tokens = lexer.lex()
    print(tokens)
    print(' '.join(str(token.value) for token in tokens))
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
    if ast == None :
        print('Error while parsing')
        exit(1)
    js = ast.to_json()
    res = dumps(js, indent=4, cls=NodeEncoder)
    with open(outputFile, 'w') as f :
        f.write(res)


def getContent(lines) :
    return [line for line in lines if line not in INCLUDES]

def checkFeatures(lines) :
    valid = True
    for line in lines :
        if line.startswith('#include') and not line in INCLUDES :
            valid = True
            print('Include ', line, 'Not yet handled')
    return valid

if __name__ == '__main__' :
    import sys
    if len(sys.argv) != 3 :
        print('Usage: ')
        print(f'./{sys.argv[0]} <input file> <output file>')
        exit(1)
    transpile(sys.argv[1], sys.argv[2])
