#Autor: Mariana David 
#Carnet: 201055
#Diseño y lenguajes de algortimos 
#Laboratorio A1

#---------------------Refererncias-------------------
# https://whitemech.github.io/pythomata/
# Bueno 

#Importaciones 
from lector import * #Importamos clase que nos ayuda a leer la expresion regular/valicion
from parseo import Parsing #Importamos clase para parseo de la expresion
from nfa import NFA #Importamos clase Autómata Finito No-Deterministico
from dfa import * #Importamos todo lo que contenga la clase DFA y DDFA (directo)
from direct_reader import DirectReader
from lexer import *

#Inicio del programa (Menu)
if __name__ == "__main__":
    print("#        Laboratorio A      # \n" )
    print("Generador automata")  #Imprimimos el titulo de entrada
    #Definimos variables
    opt = None #opcion
    regex = None # variable para el input
    method = None #metodos
    LENGUAJE = "εabcdefghijklmnopqrstuvwxyz01234567890."
    validarCerradura=False
    #Inputs del menu
    while opt != 0:
        #Imprimir menu
        print(" Seleccione la opcion que desea ejecutar: \n" +
            "1. Validar la expresion regular  \n" + 
            "2. Conversion con el metodo de thompson\n"+
            "3. Construcción directa de AFD\n"+
            "4. Lector de Yalex\n"+
            "5. Salir del programa \n") 
        opt = input('> ') #Input de opciones
        
        if opt == '1':
            print("Ingrese la expresion regular que quiere que sea validada: ") #Impresion mensaje de validacion de entrada exp. r
            regex = input('> ') #Input
            varpiz=regex.count("(")
            varpid=regex.count(")")

            try:
                posicion = regex.find("*")
                caracter_antes = regex[posicion-1]
                
                validarCerradura=False
                # validar si los caracteres estan dentro de los permitidos
                if caracter_antes in LENGUAJE:
                    valirCerradura=True
                else:
                    vadalidarCerradura1=False
                if (posicion==0): #Valido si * esta al inicio o al final.
                    validarCerradura=False
                else:
                    validarCerradura=True
                #validacion or
                posicion = regex.find("|")
                caracter_antes = regex[posicion-1]
                caracter_despues = regex[posicion+1]

                if (caracter_antes in LENGUAJE) and (caracter_despues in LENGUAJE) and (caracter_antes in "*"):#Se valida que la posicion antes
                    #y la posicion despues tenga que ser un * o algo dentro del lenguaje.
                    validarOR=True
                else:
                    validarOR=False
                if (posicion==0): #Valido si | esta al inicio o al final.
                    validarOR=False
                else:
                    validarOR=True
            

                posicion = regex.find(".")
                caracter_antes = regex[posicion-1]
                caracter_despues = regex[posicion+1]
                
                validarConcatenacion=False
                # validar si los caracteres estan dentro de los permitidos
                if (caracter_antes in LENGUAJE) and (caracter_despues in LENGUAJE) and (caracter_antes in "*"):
                    validarConcatenacion=True
                else:
                    validarConcatenacion=False
                if (posicion==0): #Valido si . esta al inicio o al final.
                    validarConcatenacion=False
                else:
                    validarConcatenacion=True

            except:
                print("x")
                validarCerradura=False
                validarOR=False
                validarConcatenacion=False

            if(validarCerradura==True and validarOR==True and validarConcatenacion==True): ##Si cumple las validaciones se deja continuar.
                if(varpid!=varpiz):
                    print("[Error] Expresion invalida (Falta parentesis, porfavor revisar tu input)")
                else:
                    regex="("+regex+")"
                    print(regex)
                    try: 
                        
                        reader = Lector(regex) #guardo en la variable reader la lectura del input ingresado  
                        tokens = reader.Creacion_tokens() #guardo en la var tokens la lectura aplicando la funcion crecion tockens para validar 
                        parseo = Parsing(tokens) #llevo la variable de tokens para aplicar la clase de parsin
                        exp_postfix = parseo.Parse() #llevo var parseo a ser ejecutada por funcion Parse (secuencia de tokens)
                        
                        #-------------------------------NEW            
                        direct_reader = DirectReader(regex)
                        direct_tokens = direct_reader.CreateTokens()
                        direct_parser = Parsing(direct_tokens)
                        direct_tree = direct_parser.Parse()
                        


                        print("¡Aprobado! La expresion regular es correcta") #impresiones 
                        print('\tParsed tree:', exp_postfix)
                        validarCerradura=True
                        
                        if(str(exp_postfix)[0:1]=="("):
                            final=(str(exp_postfix)[1:-1])
                        else:
                            final=exp_postfix
                        
                        #-----------------------IF DEL NEW
                        if(str(direct_tree)[0:1]=="("):
                            final=(str(direct_tree)[1:-1])
                        else:
                            final=direct_tree

                    except AttributeError as ε: #si la lectura es incorrecta por paretesis
                        print("[Error] Expresion invalida (Falta parentesis, porfavor revisar tu input)")
                        #print("Error es",ε)
                        validarCerradura=False

                    except Exception as ε: #si la lectura es incorrecta por simbolo no perteneciente 
                        print(f'\n\t[ERROR 333] {ε}')
                        validarCerradura=False
            else:
                print("[Error] Expresion invalida")
        if opt == '2': # Opcion que tomar la expresion para conversion por thompson
            if not regex: #si no paso por la validacion lo obliga 
                print('\n\t[ERROR 1] Asegurate de validar tu expresion regular primero')
                opt = None
            if validarCerradura==False:
                print('\n\t[ERROR 2] Asegurate de validar tu expresion regular primero')
                opt = None
            else:
                print("# Conversion con metodo de Thompson# \n") 
                print("Escribe la expresion regular:") # ingrese la expresion regular 
                regex_input = input('> ') #input de la expresion regular 

                nfa = NFA(exp_postfix, reader.GetSymbols(), regex_input)  #crea objeto NFA de la expresion regular 
                nfa_regex = nfa.EvalRegex() #llama al metodo que generar un AFN a partir de la expresión regular proporcionada

                print("¿Desea generar el diagrama de la expresion regular ingresada? [si/no]") #pregunta si quiere generar grafica
                opt = input('> ') #input de la respuesta
                if opt == 'si': #genera grafica 
                    print("Espere un momento...")
                    nfa.GenerateDiagram()
                elif opt == 'no': #no genera grafica, retorna al menu
                    print("Regresando al menu...")
                else: # opcion invalida, retorna a la pregunta de grafica
                    print("[Error] Entrada no valida, revise porfavor")
                    print("¿Desea generar el diagrama de la expresion regular ingresada? [si/no]")
                    opt = input('> ')
                    if opt == 'si':
                        print("Espere un momento...")
                        nfa.GenerateDiagram()
                    elif opt == 'no':
                        print("Regresando al menu...")
                    else: 
                        print("[Error] Entrada no valida, revise porfavor")
            validarCerradura=False


        if opt == '3': # Opcion que tomar la expresion para conversion por thompson
            if not regex: #si no paso por la validacion lo obliga 
                print('\n\t[ERROR 1] Asegurate de validar tu expresion regular primero')
                opt = None
            if validarCerradura==False:
                print('\n\t[ERROR 2] Asegurate de validar tu expresion regular primero')
                opt = None
            else:
                print("# Construcción directa AFD (con subconjuntos) # \n") 
                print("Escribe la expresion regular:") # ingrese la expresion regular 
                regex_input = input('> ') #input de la expresion regular 

                ddfa = DDFA(direct_tree, direct_reader.GetSymbols(), regex_input)  #crea objeto NFA de la expresion regular 
                ddfa_regex = ddfa.EvalRegex() #llama al metodo que generar un AFN a partir de la expresión regular proporcionada

                print("¿Desea generar el diagrama de la expresion regular ingresada? [si/no]") #pregunta si quiere generar grafica
                opt = input('> ') #input de la respuesta
                if opt == 'si': #genera grafica 
                    print("Espere un momento...")
                    ddfa.GraphDFA()
                elif opt == 'no': #no genera grafica, retorna al menu
                    print("Regresando al menu...")
                else: # opcion invalida, retorna a la pregunta de grafica
                    print("[Error] Entrada no valida, revise porfavor")
                    print("¿Desea generar el diagrama de la expresion regular ingresada? [si/no]")
                    opt = input('> ')
                    if opt == 'si':
                        print("Espere un momento...")
                        ddfa.GraphDFA()
                    elif opt == 'no':
                        print("Regresando al menu...")
                    else: 
                        print("[Error] Entrada no valida, revise porfavor")
            validarCerradura=False

        elif opt == '4': #Yalex
            print("Realizando yalex")
            lexermain()

        elif opt == '5': #sale del menu
            print('Has salido del menu exitosamente')
            exit(1)
