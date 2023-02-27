#Autor: Mariana David 
#Carnet: 201055
#Diseño y lenguajes de algortimos 
#Laboratorio A

#Importaciones
from tokens import * #Impotamos clase tipo_token que nos ayuda a identificar


#Clase de parseo para anlizar y procesar tokens de entrada 
class Parsing:
    def __init__(self, tokens): #inicializa la clase con una lista de tokens 
        self.tokens = iter(tokens) #inicializa el iterador con la lista de tokes 
        self.Next() #metodo next para leer siguiente token

    def Next(self): #asiga el sigueinte token en la lista de tokes 
        self.curr_token = next(self.tokens, None)

    def NewSymbol(self): #procesa los tokens que representan simpolos o letras
        token = self.curr_token #asigan el token actual a la variable
        if token.type == Tipo_token.IPAR: #si el token es parentesis izq
            self.Next() #avanza al sigueinte token
            resultado = self.Expresion() #llama la funcion recursivamente para procesar la expresion dentor del parentesis 

            if self.curr_token.type != Tipo_token.DPAR: #si el token es diferente al parentesis derecho
                #print("Error no hay parentesis derecho.")
                raise Exception("[ERROR] No hay paréntesis derecho en la expresión") #no es valido porque no estan completos 
            self.Next() #lee siguiente token
            return resultado #devuelve el resultado 

        elif token.type == Tipo_token.LETRA: #si el tipo de token es una letra 
            self.Next() # avanza porque si es parte del lenguaje 
            return Letra(token.value) # se devuelve un objeto leta que representa la letra del token actual 

    def NewOperator(self): #procesa los tokens que representan operadores 
        resultado = self.NewSymbol() #se llama la funcion para procesar el primer simbolo o letra 

        #condicion mientras el tojen acutal no sea none y sea uno de los tipos kleen, suma o signo de interrugacion se ejecuta 
        while self.curr_token and self.curr_token.type in (Tipo_token.KLEENE, Tipo_token.SUMA, Tipo_token.QUESTION): 
            if self.curr_token.type == Tipo_token.KLEENE: #si es token kleene
                self.Next() #pasa al sigiente token porque si es aceptado 
                resultado = Kleene(resultado) # se asigna resultado a un nuevo objeto kleene que represeta la operacicon 
            elif self.curr_token.type == Tipo_token.QUESTION:# si el token es pregunta
                self.Next() #pasa al siguiente token porque si es aceptado 
                resultado = Question(resultado) # se asigna resultado a un nuevo objeto que representa la operacion 
            else: #si el token es suma 
                self.Next() #avanza al sigueiknte token 
                resultado = Suma(resultado) #asigna reultado a un nuevo objeto suma representado por la operacion 

        return resultado #se devueve la operacion final en objeto resultado

    def Expresion(self): #procesar los tokens que representan una expresion
        resultado = self.NewOperator() #se llama la funcion para procesar los tokens que represan un operador 

        while self.curr_token and self.curr_token.type in (Tipo_token.APPEND, Tipo_token.OR): #mientras el token no sea non y sea uno de lot ipos de token appen o or se ejecuta
            if self.curr_token.type == Tipo_token.OR: # si el token es tipo or
                self.Next() #pasa al sigueinte token porque es acpetado 
                resultado = Or(resultado, self.NewOperator()) #nuevo objeto que representa la operacion or

            elif self.curr_token.type == Tipo_token.APPEND: # si el token es tipo append
                self.Next() #pasa al siguiente token porque es acpetado 
                resultado = Append(resultado, self.NewOperator()) #nuevo objeto que representa la operacion append

        return resultado #se devuelve el resultado que representa la expresion final 
    # Funcion que procesa la secuencia de tokens para construir una estructura sintáctica
    def Parse(self):#Verificando si hay un token actual disponible para procesar
        return self.Expresion() if self.curr_token else None #Si si hay llama la funcion Expresion que almacena en var resultad oultado

