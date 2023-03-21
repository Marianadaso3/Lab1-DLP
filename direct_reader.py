from tokens import Token, Tipo_token

LETTERS = 'εabcdefghijklmnopqrstuvwxyz01234567890.'


class DirectReader:

    def __init__(self, string: str):
        self.string = iter(string.replace(' ', ''))
        self.input = set()
        self.rparPending = False
        self.Next()

    def Next(self):
        try:
            self.curr_char = next(self.string)
        except StopIteration:
            self.curr_char = None

    def CreateTokens(self):
        while self.curr_char != None:

            if self.curr_char in LETTERS:
                self.input.add(self.curr_char)
                yield Token(Tipo_token.LETRA, self.curr_char)

                self.Next()

                # Finally, check if we need to add an append token
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(Tipo_token.APPEND, '.')

            elif self.curr_char == '|':
                yield Token(Tipo_token.OR, '|')

                self.Next()

                if self.curr_char != None and self.curr_char not in '()':
                    yield Token(Tipo_token.IPAR)

                    while self.curr_char != None and self.curr_char not in ')*+?':
                        if self.curr_char in LETTERS:
                            self.input.add(self.curr_char)
                            yield Token(Tipo_token.LETRA, self.curr_char)

                            self.Next()
                            if self.curr_char != None and \
                                    (self.curr_char in LETTERS or self.curr_char == '('):
                                yield Token(Tipo_token.APPEND, '.')

                    if self.curr_char != None and self.curr_char in '*+?':
                        self.rparPending = True
                    elif self.curr_char != None and self.curr_char == ')':
                        yield Token(Tipo_token.DPAR, ')')
                    else:
                        yield Token(Tipo_token.DPAR, ')')

            elif self.curr_char == '(':
                self.Next()
                yield Token(Tipo_token.IPAR)

            elif self.curr_char in (')*+?'):

                if self.curr_char == ')':
                    self.Next()
                    yield Token(Tipo_token.DPAR)

                elif self.curr_char == '*':
                    self.Next()
                    yield Token(Tipo_token.KLEENE)

                elif self.curr_char == '+':
                    self.Next()
                    yield Token(Tipo_token.SUMA)

                elif self.curr_char == '?':
                    self.Next()
                    yield Token(Tipo_token.QUESTION)

                if self.rparPending:
                    yield Token(Tipo_token.DPAR)
                    self.rparPending = False

                # Finally, check if we need to add an append token
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(Tipo_token.APPEND, '.')

            else:
                raise Exception(f'Invalid entry: {self.curr_char}')

        yield Token(Tipo_token.APPEND, '.')
        yield Token(Tipo_token.LETRA, '#')

    def GetSymbols(self):
        return self.input
