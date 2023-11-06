from tokens import Token,Literal,Comment,Type,Types

class Tokenizer :
    NAMING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    NUMBERS = '0123456789'
    BLANK = ' \n\t'
    PARAS = '()[]{}'
    QUOTES = '"\''
    CLOSING = {
        '\'': '\'',
        '"': '"',
        '(':')',
        '[':']',
        '{':'}'
    }
    PONCTUATION = ';.,'
    OPERATORS = '+-/*^|&=!<>?:'
    DOUBLE_OPERATORS = ['++', '--', '+=', '-=', '*=', '/=', '^=', '&=', '|=', '==', '!=', '<=', '>=', '&&', '||', '<<', '>>']

    def __init__(self, content) :
        self.content = content
        self.length = len(content)
        self.index=0

    def _peak_current(self) :
        if self.index >= self.length :
            return None
        print(self.content[self.index])
        return self.content[self.index]

    def _peak_next(self) :
        if self.index+1 >= self.length :
            return None
        return self.content[self.index + 1]

    def _eat_to_next(self) :
        self.index+= 1
        return self._peak_current()

    def _eat_nb__(self) :
        nb = self._peak_current()
        curr = self._eat_to_next()
        nb_type = int
        while curr in Tokenizer.NUMBERS:
            nb += curr
            curr = self._eat_to_next()
            if curr == '.' and nb_type == int :
                curr = self._eat_next()
                nb_type=float
        return Literal('NB', nb_type(nb))

    def _eat_name(self) :
        name = self._peak_current()
        curr = self._eat_to_next()
        while curr in Tokenizer.NUMBERS or curr in Tokenizer.NAMING:
            name += curr
            curr = self._eat_to_next()
        if name in Types.__members__ :
            return Type(Types(name))
        return Token('NAME', name)

    def _eat_quoted(self) :
        quote = self._peak_current()
        quoted = quote
        curr = self._eat_to_next()
        while curr != Tokenizer.CLOSING[quote]:
            quoted += curr
            curr = self._eat_to_next()
            if curr == '\\' :
                quoted += curr + self._eat_to_next()
                curr = self._eat_to_next()
        quoted += curr
        self._eat_to_next()
        return Literal('STRING', quoted)

    def _eat_comment_block(self) :
        comment = self._peak_current()
        curr = self._peak_current() + self._eat_to_next()
        while curr != '*/' :
            if self._peak_next() == None :
                return Comment(comment)
            comment += self._peak_current()
            curr = self._peak_current() + self._eat_to_next()
        comment += self._peak_current()
        self._eat_to_next()
        return Comment(comment)

    def _eat_comment_line(self) :
        comment = self._peak_current()
        curr = self._eat_to_next()
        while curr != None and curr != '\n' :
            comment += curr
            curr = self._eat_to_next()
        return Comment(f'/* {comment[2:].strip()} */')

    def _next(self):
        curr = self._peak_current()

        while curr != None and curr in Tokenizer.BLANK :
            curr = self._eat_to_next()
        if curr is None :
            return None

        if curr in Tokenizer.NUMBERS :
            return self._eat_nb__()
        elif curr in Tokenizer.NAMING :
            return self._eat_name()
        elif curr in Tokenizer.PARAS :
            self._eat_to_next()
            return Token('PARA', curr)
        elif curr in Tokenizer.QUOTES :
            return self._eat_quoted()
        elif curr in Tokenizer.PONCTUATION:
            self._eat_to_next()
            return Token('PONCUTATION', curr)
        elif curr in Tokenizer.OPERATORS :
            if curr == '/' and self._peak_next() == '/' :
                return self._eat_comment_line()
            if curr == '/' and self._peak_next() == '*' :
                return self._eat_comment_block()
            if curr + self._peak_next() in Tokenizer.DOUBLE_OPERATORS :
                curr += self._peak_next()
                self._eat_to_next()

            self._eat_to_next()
            return Token('OPERATOR', curr)

    def tokenize(self) :
        tokens = []
        tok= None
        while (tok:=self._next()) :
            tokens.append(tok)

        return tokens

    def __repr__(self) :
        return self.content[self.index:]
