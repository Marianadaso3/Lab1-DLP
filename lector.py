#Autor: Mariana David 
#Carnet: 201055
#Diseño y lenguajes de algortimos 
#Laboratorio A

#Importaciones 
from tokens import *

# Letras/num/sim que pertenencen al lenguaje
LENGUAJE = 'εabcdefghijklmnopqrstuvwxyz01234567890.' 

#Clase lector: se encarga de leer la expresion regular y analizara
class Lector:
    #metodo constructor 
    def __init__(self, string: str):
        # reemplaza todos los espacios en blanco (" ") con una cadena vacía ("") utilizando el método replace() 
        self.string = iter(string.replace(' ', '')) # guarda el resultado en el atributo "string"
        self.input = set() # Crea un conjunto vacío y lo guarda en el atributo "input" 
        self.Next() # método Next() para avanzar el iterador al primer carácter de la cadena

    #funcion para obtener el siguiente carácter de la cadena
    def Next(self):
        try:
            self.curr_char = next(self.string) # Si el siguiente carácter se puede obtener correctamente, se asigna a self.curr_char.
        except StopIteration: #si alcanza el final de la cadena de texto (produce una excepción StopIteration)
            self.curr_char = None # se asigna None a self.cur r_char.
    #funcion para crear y devolver tokens paralelo analizar cadenas
    def Creacion_tokens(self):
        while self.curr_char != None: #bucle mientras no sea none

            if self.curr_char in LENGUAJE: #verifica que sea parte del lenguaje
                self.input.add(self.curr_char) #curr_char se agrega al input 
                yield Token(Tipo_token.IPAR, '(') #se devuelven dos tokens (parenteisis izq)
                yield Token(Tipo_token.LETRA, self.curr_char) # token de letra qeu representa el curr_char

                self.Next() #Metodo next para avanzar caracter
                added_parenthesis = False #variable bandera

                #While mientras el valor actual de "self.curr_char" no sea "None" y "self.curr_char" sea una letra, un asterisco, un signo más, o un signo de interrogación.
                while self.curr_char != None and \
                        (self.curr_char in LENGUAJE or self.curr_char in '*+?'):

                    if self.curr_char == '*': # si es asterisco devuleve 2 token 
                        yield Token(Tipo_token.KLEENE, '*') # token kleene
                        yield Token(Tipo_token.DPAR, ')') # token parentesis derecho
                        added_parenthesis = True

                    elif self.curr_char == '+': # si es suma devuleve 2 token 
                        yield Token(Tipo_token.SUMA, '+') # token suma
                        yield Token(Tipo_token.DPAR, ')') # token parentesisi derecho
                        added_parenthesis = True

                    elif self.curr_char == '?':  #si el caracter es interrogacion devuleve 2 token 
                        yield Token(Tipo_token.QUESTION, '?') # token suma
                        yield Token(Tipo_token.DPAR, ')') # token parentesisi derecho
                        added_parenthesis = True

                    elif self.curr_char in LENGUAJE: #si el valor es una letra
                        self.input.add(self.curr_char) #se agrega al input y devulve un token
                        yield Token(Tipo_token.APPEND) #token de concatenacion
                        yield Token(Tipo_token.LETRA, self.curr_char) # token de letra

                    self.Next() #avanza al sigueinte caracter

                    if self.curr_char != None and self.curr_char == '(' and added_parenthesis: #si curr_cahr es un parectesis izquierdo y se agrego un parenteisi derecho previamente
                        yield Token(Tipo_token.APPEND) # devulve token para concatenacion de tokens (parentesis cerrados)

                if self.curr_char != None and self.curr_char == '(' and not added_parenthesis: #si curr_char es un parentesis izquierdo y si se agrego antes 
                    yield Token(Tipo_token.DPAR, ')') #devuelve un token para el parentesis derecho
                    yield Token(Tipo_token.APPEND) # devuelve token para concatenacion de tokens

                elif not added_parenthesis: # si es un parentesis derecho y no se agrego parenteissi derecho 
                    yield Token(Tipo_token.DPAR, ')') # devuelve token para el parentesis derecho

            elif self.curr_char == '|': #si es una barra 
                self.Next() #llama al metodo para avanzar el caracter en la cadena 
                yield Token(Tipo_token.OR, '|') #devuvle un token OR

            elif self.curr_char == '(': # si es parentesis izquierdo 
                self.Next() # avanza caracter
                yield Token(Tipo_token.IPAR) #genera token 

            elif self.curr_char in (')*+?'): #si es una de estos simbolos 

                if self.curr_char == ')':
                    self.Next()  # avanza caracter
                    yield Token(Tipo_token.DPAR) #genera token parenteisi derecha

                elif self.curr_char == '*':
                    self.Next()  # avanza caracter
                    yield Token(Tipo_token.KLEENE) #genera token cerradura kleene

                elif self.curr_char == '+':
                    self.Next()  # avanza caracter
                    yield Token(Tipo_token.SUMA) #genera token suma

                elif self.curr_char == '?':
                    self.Next()  # avanza caracter
                    yield Token(Tipo_token.QUESTION) #genera token interrogacion

                # Finalmente, verifique si necesitamos agregar un token 
                if self.curr_char != None and \
                        (self.curr_char in LENGUAJE or self.curr_char == '('):
                    yield Token(Tipo_token.APPEND, '.') #genera token para concatenacion de tokens


            else: # si ninguna se cumple se genera una excpecion 
                raise Exception(f'La entrada ingresada invalida es:  {self.curr_char}')

    def GetSymbols(self): #alcanza el siumbolo 
        return self.input #regresa el input analizado

