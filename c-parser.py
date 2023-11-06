#!/usr/bin/python3.11

from tokenizer import Tokenizer

INCLUDES = [
    '#include <stdio.h>\n',
    '#include <stdlib.h>\n',
    '#include <string.h>\n'
]

def parse(filename:str):
    with open(filename, 'r') as f :
        lines = f.readlines()

    print(lines)
    if not checkFeatures(lines) :
        exit(2)

    content = ''.join(getContent(lines))
    tokenizer = Tokenizer(content)
    print(tokenizer)
    tokens = tokenizer.tokenize()
    print(tokens)
    print(' '.join(str(token.value) for token in tokens))

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
    if len(sys.argv) != 2 :
        print('Usage: ')
        print(f'./{sys.argv[0]} <filename>')
        exit(1)
    parse(sys.argv[1])
