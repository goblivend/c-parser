from tokens import Token,Literal

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
    OPERATORS = '+-/*^|&'

    def __init__(self, content) :
        self.content = content
        self.length = len(content)
        self.index=0
    
    def __peak_current__(self) :
        if self.index >= self.length :
            return None
        return self.content[self.index]
    
    def __peak_next__(self) :
        if self.index+1 >= self.length :
            return None
        return self.content[self.index + 1]

    def __eat_to_next__(self) :
        self.index+= 1
        return self.__peak_current__()

    def __eat_nb__(self) :
        nb = self.__peak_current__()
        curr = self.__eat_to_next__()
        nb_type = int
        while curr in Tokenizer.NUMBERS:
            nb += curr
            curr = self.__eat_to_next__()
            if curr == '.' and nb_type == int :
                curr = self.__eat_next__()
                nb_type=float
        return Literal('NB', nb_type(nb))

    def __eat_name__(self) :
        name = self.__peak_current__()
        curr = self.__eat_to_next__()
        while curr in Tokenizer.NUMBERS or curr in Tokenizer.NAMING:
            name += curr
            curr = self.__eat_to_next__()
        return Token('NAME', name)

    def __eat_quoted__(self) :
        quote = self.__peak_current__()
        quoted = quote
        curr = self.__eat_to_next__()
        while curr != Tokenizer.CLOSING[quote]:
            quoted += curr
            curr = self.__eat_to_next__()
            if curr == '\\' :
                quoted += curr + self.__eat_to_next__()
                curr = self.__eat_to_next__()
        quoted += curr
        self.__eat_to_next__()
        return Literal('STRING', quoted)

    def __skip_comment__(self) :
        curr = self.__peak_current__() + self.__eat_to_next__()
        while curr != '*/' :
            if self.__peak_next__() == None :
                return
            curr = self.__peak_current__() + self.__eat_to_next__()
            

    def __next__(self):
        curr = self.__peak_current__()
        if curr is None :
            return None
        while curr in Tokenizer.BLANK :
            curr = self.__eat_to_next__()

        if curr in Tokenizer.NUMBERS :
            return self.__eat_nb__()
        elif curr in Tokenizer.NAMING :
            return self.__eat_name__()
        elif curr in Tokenizer.PARAS :
            self.__eat_to_next__()
            return Token('PARA', curr)
        elif curr in Tokenizer.QUOTES :
            return self.__eat_quoted__()
        elif curr in Tokenizer.PONCTUATION: 
            self.__eat_to_next__()
            return Token('PONCUTATION', curr)
        elif curr in Tokenizer.OPERATORS :
            if curr == '/' and self.__peak_next__() == '*' :
                self.__skip_comment__()
                return self.__next__()
            self.__eat_to_next__()
            return self.__next__()

    def tokenize(self) :
        tokens = []
        tok= None
        while (tok:=self.__next__()) :
            tokens.append(tok)

        return tokens

    def __repr__(self) :
        return self.content[self.index:]

