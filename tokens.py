#Autor: Mariana David 
#Carnet: 201055
#Diseño y lenguajes de algortimos 
#Laboratorio A

#----------------------Referencias-------------
# https://docs.python.org/es/3/library/enum.html#:~:text=Permite%20que%20los%20atributos%20de,los%20nombres%20value%20y%20name%20.


#Importaciones
from enum import Enum #libreria para enumeraciones de datos 

#Clase de enumeraciones tipo enum (libreria)
class Tipo_token(Enum): #numeramos para la facilitacion del manejo de tokens
    LETRA = 0
    APPEND = 1
    OR = 2
    KLEENE = 3
    SUMA = 4
    QUESTION = 5
    IPAR = 6
    DPAR = 7
# Clase de creacion de tokens en el analizador lexico 
class Token:
    def __init__(self, type: Tipo_token, value=None): # Definir contructot 
        self.type = type #Asigna el valor del argumento type
        self.value = value #Asigna el valor del argumento value 
        self.precedence = type.value #Asigna el valor de la propiedad value 

    def __repr__(self): #Define un metodo para mostrar una represenacion en cadena
        return f'{self.type.name}: {self.value}' #Devuelve una cadena que representa la instancia de la clase token 
        #formato ejemplo: ENTERO: 42


#Cualidades de los nodos en clases 
#clase de letra representando una del alfabeto 
class Letra:
    def __init__(self, value): #nueva instancia 
        self.value = value

    def __repr__(self): #metodo para representar la instancia en forma de cadena
        return f'{self.value}' #devuelve la cadena que contiene el valor de "value"


class Append(): 
    def __init__(self, a, b): #metodo de inicializacion 
        self.a = a # establece el atributo a de la instancia en el valor del parámetro a
        self.b = b # establece el atributo b de la instancia en el valor del parámetro b

    def __repr__(self): # devuelve una representación en cadena de la instancia de la clase
        return f'({self.a}.{self.b})' # devuelve una cadena que representa la instancia de la clase 
        #Separado por puntos y rodeados por parentesis = a es hola y b es como la cadena es: (hola.como)

class Or():
    def __init__(self, a, b): # constructor 
        self.a = a #atributos
        self.b = b

    def __repr__(self): #  representación de cadena de la instancia de la clase 
        return f'({self.a}|{self.b})' # devuelve  una cadena que representa la expresión "o" entre las dos expresiones
        #separados por el caracter |

class Kleene():
    def __init__(self, a): #inicializa la instancia 
        self.a = a #asigan el valor al atributo

    def __repr__(self): #  devolver una representación en cadena de la instancia 
        return f'{self.a}*' #devuelve una cadena en la que el elemento a se repite cero o más veces
        #La cadena resultante es del tipo aa*, donde a es la representación en cadena del elemento que se va a repetir cero o más veces

class Suma():
    def __init__(self, a): #inicializa la instancia 
        self.a = a #asigan el valor al atributo

    def __repr__(self): #representar el objeto como una cadena de caracteres
        return f'{self.a}+' # representación de la expresión regular a, seguida por el símbolo +


class Question():
    def __init__(self, a):#inicializa la instancia 
        self.a = a  #asigan el valor al atributo

    def __repr__(self): # devuelve una representación de cadena del objeto
        return f'{self.a}?' #Devuelve una cadena que representa la expresión regular opcional, utilizando el operador ?


class Expression():
    def __init__(self, a, b=None): #inicializa la instancia 
        self.a = a #asigan el valor al atributo
        self.b = b #asigan el valor al atributo

    def __repr__(self): #representar la expresión regular en forma de cadena
        if self.b != None: # Si b no es None
            return f'{self.a}{self.b}' #  se asume que se trata de una expresión binaria y se devuelve la concatenación de a y b
        return f'{self.a}'#En caso contrario, solo se devuelve a
        #En ambos casos, la cadena se devuelve sin espacios



