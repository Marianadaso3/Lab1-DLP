#Autor: Mariana David 
#Carnet: 201055
#Diseño y lenguajes de algortimos 
#Laboratorio A

#Importaciones
from tokens import * #Impotamos clase tipo_token que nos ayuda a identificar


#Clase de parseo para anlizar y procesar tokens de entrada 
class Parsing:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.Next()

    def Next(self):
        try:
            self.curr_token = next(self.tokens)
        except StopIteration:
            self.curr_token = None

    def NewSymbol(self):
        token = self.curr_token

        if token.type == Tipo_token.IPAR:
            self.Next()
            res = self.Expression()

            if self.curr_token.type != Tipo_token.DPAR:
                raise Exception('No right parenthesis for expression!')

            self.Next()
            return res

        elif token.type == Tipo_token.LETRA:
            self.Next()
            return Letra(token.value)

    def NewOperator(self):
        res = self.NewSymbol()

        while self.curr_token != None and \
                (
                    self.curr_token.type == Tipo_token.KLEENE or
                    self.curr_token.type == Tipo_token.SUMA or
                    self.curr_token.type == Tipo_token.QUESTION
                ):
            if self.curr_token.type == Tipo_token.KLEENE:
                self.Next()
                res = Kleene(res)
            elif self.curr_token.type == Tipo_token.QUESTION:
                self.Next()
                res = Question(res)
            else:
                self.Next()
                res = Suma(res)

        return res

    def Expression(self):
        res = self.NewOperator()

        while self.curr_token != None and \
                (
                    self.curr_token.type == Tipo_token.APPEND or
                    self.curr_token.type == Tipo_token.OR
                ):
            if self.curr_token.type == Tipo_token.OR:
                self.Next()
                res = Or(res, self.NewOperator())

            elif self.curr_token.type == Tipo_token.APPEND:
                self.Next()
                res = Append(res, self.NewOperator())

        return res

    def Parse(self):
        if self.curr_token == None:
            return None

        res = self.Expression()

        return res
