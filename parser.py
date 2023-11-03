#!/usr/bin/python3

from tokenizer import Tokenizer

INCLUDES = [
    '#include <stdio.h>',
    '#include <stdlib.h>',
    '#include <string.h>'
]

def parse(filename:str): 
    with open(filename, 'r') as f :
        lines = f.readlines()

    print(lines)
    cleanLines = clean(lines)
    print(cleanLines)
    if not checkFeatures(cleanLines) :
        exit(2)

    content = ''.join(getContent(cleanLines))
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


def clean(lines) :
    return  [line for line in [line.strip() for line in lines] if not line.startswith('//')]

if __name__ == '__main__' :
    import sys
    if len(sys.argv) != 2 :
        print('Usage: ')
        print(f'./{sys.argv[0]} <filename>')
        exit(1)
    parse(sys.argv[1])
