#Importaciones 
from graphviz import Digraph
import sys
from MegaAutomata import *

def funciones (izquierdaMegaAutomata,separadorMegaAutomata,idMegaAutomata,IgualMegaAutomata,abrirSetMegaAutomata,cerrarSetMegaAutomata,abrirParentesisMegaAutomata,cerrarParentesisMegaAutomata,operadoresMegaAutomata,caracterMegaAutomata,cadenaMegaAutomata,uncaracterMegaAutomata,rangoMegaAutomata,reglaMegaAutomata,desabilitadosMegaAutomata):
    izquierdaMegaAutomata.reiniciarSimulacion()
    separadorMegaAutomata.reiniciarSimulacion()
    idMegaAutomata.reiniciarSimulacion()
    IgualMegaAutomata.reiniciarSimulacion()
    abrirSetMegaAutomata.reiniciarSimulacion()
    cerrarSetMegaAutomata.reiniciarSimulacion()
    abrirParentesisMegaAutomata.reiniciarSimulacion()
    cerrarParentesisMegaAutomata.reiniciarSimulacion()
    operadoresMegaAutomata.reiniciarSimulacion()
    caracterMegaAutomata.reiniciarSimulacion()
    cadenaMegaAutomata.reiniciarSimulacion()
    uncaracterMegaAutomata.reiniciarSimulacion()
    rangoMegaAutomata.reiniciarSimulacion()
    reglaMegaAutomata.reiniciarSimulacion()
    desabilitadosMegaAutomata.reiniciarSimulacion()

def lexermain():
    #para tener todos los caracteres ascii en string y char
    caracterAsciiComplemento = concatenearOr(conjuntoDeRangoCaracteres(chr(33), chr(38))) +'|'+ concatenearOr(conjuntoDeRangoCaracteres(chr(44), chr(47)))+'|'+concatenearOr(conjuntoDeRangoCaracteres(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenearOr(conjuntoDeRangoCaracteres(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenearOr(conjuntoDeRangoCaracteres(chr(125), chr(126)))
    cadenaAsciiComplement ='('+chr(33) + ')|' + concatenearOr(conjuntoDeRangoCaracteres(chr(35), chr(39)))+ '|'+ concatenearOr(conjuntoDeRangoCaracteres(chr(44), chr(47)))+'|'+concatenearOr(conjuntoDeRangoCaracteres(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenearOr(conjuntoDeRangoCaracteres(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenearOr(conjuntoDeRangoCaracteres(chr(125), chr(126)))
    IdentificadorDeCaracter = IdentificadorDeCaracter +['|']+ list(caracterAsciiComplemento)
    IdentificadorDeCadena = IdentificadorDeCadena +['|']+ list(cadenaAsciiComplement)
    identificadorDeOperadoresDesabilitados = ["'"] + IdentificadorDeOperador + ["'"]
    anychar_regex = ['('] + IdentificadorDeCaracter + ['|'] +list(caracterAsciiComplemento)+[')']
    
    path = sys.argv[1] if len(sys.argv) > 1 else input('Introduzca una ruta de archivo yal:')
    izquierdaIdentificador = ['let']
    separadorIdentificador = ['\n', '\t', ' ']
    idIdentificador = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + [chr(i) for i in range(ord('0'), ord('9')+1)] + ['_']
    igualIdentificador = ['=']
    abrirSetIdentificador = ['[']
    cerrarSetIdentificador = [']']
    abrirParentesisIdentificador = ['(']
    cerrarParentesisIdentificador = [')']
    IdentificadorDeOperador = ['(', '*', '|', '+', '?', '|', '(', ')']
    IdentificadorDeCaracter = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + [chr(i) for i in range(ord('0'), ord('9')+1)] + ['\n', '\t', ' '] + IdentificadorDeOperador
    IdentificadorDeCadena = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + [chr(i) for i in range(ord('0'), ord('9')+1)] + ['\n', '\t', ' '] + IdentificadorDeOperador
    caracterAsciiComplemento = [chr(i) for i in range(33, 39)] + [chr(i) for i in range(40, 48)] + [chr(i) for i in range(58, 63)] + ['@'] + [chr(i) for i in range(91, 97)] + ['{'] + [chr(i) for i in range(125, 127)]
    cadenaAsciiComplemento = ['!', chr(35), chr(36), chr(37), chr(38), chr(40), chr(41), chr(42), chr(43), chr(44), chr(45), chr(46), chr(47), chr(58), chr(59), chr(60), chr(61), chr(62), '@'] + [chr(i) for i in range(91, 97)] + ['{'] + [chr(i) for i in range(125, 127)]
    cualquierCaracterIdentificador = ['_'] + IdentificadorDeCaracter + caracterAsciiComplemento
    IdentificadorDeCaracter = ["'", '(', any(cualquierCaracterIdentificador), ')', "'"]
    IdentificadorDeCadena = ['"', '(', '(', any(IdentificadorDeCadena), '|', any(cadenaAsciiComplemento), ')', '+', ')', '"']
    cualquierCaracterIdentificador = ['_']
    rangoDeIdentificacion = ['(', any(IdentificadorDeCaracter), ')', '-', '(', any(IdentificadorDeCaracter), ')']
    reglaIdentificacion = ['rule']


    #Construcciones
    idMegaAutomata = construirAutomataDirecto(idIdentificador)
    izquierdaMegaAutomata = construirAutomataDirecto(izquierdaIdentificador)
    separadorMegaAutomata = construirAutomataDirecto(separadorIdentificador)

    desabilitadosMegaAutomata = construirAutomataDirecto(identificadorDeOperadoresDesabilitados)
    operadoresMegaAutomata = construirAutomataDirecto(IdentificadorDeOperador)
    caracterMegaAutomata = construirAutomataDirecto(IdentificadorDeCaracter)
    cadenaMegaAutomata = construirAutomataDirecto(IdentificadorDeCadena)
    

    IgualMegaAutomata = construirAutomataDirecto(igualIdentificador)

    abrirSetMegaAutomata = construirAutomataDirecto(abrirSetIdentificador)
    abrirParentesisMegaAutomata = construirAutomataDirecto(abrirParentesisIdentificador)

    cerrarSetMegaAutomata = construirAutomataDirecto(cerrarSetIdentificador)
    cerrarParentesisMegaAutomata = construirAutomataDirecto(cerrarParentesisIdentificador)

    uncaracterMegaAutomata = construirAutomataDirecto(cualquierCaracterIdentificador)

    rangoMegaAutomata = construirAutomataDirecto(rangoDeIdentificacion)
    reglaMegaAutomata = construirAutomataDirecto(reglaIdentificacion)

    #recuerda reiniciar la simulación antes de intentar simular
    funciones (izquierdaMegaAutomata,separadorMegaAutomata,idMegaAutomata,IgualMegaAutomata,abrirSetMegaAutomata,cerrarSetMegaAutomata,abrirParentesisMegaAutomata,cerrarParentesisMegaAutomata,operadoresMegaAutomata,caracterMegaAutomata,cadenaMegaAutomata,uncaracterMegaAutomata,rangoMegaAutomata,reglaMegaAutomata,desabilitadosMegaAutomata)

    try:
        ArchivoContenidoSinProcesar = leerNombreFile(path)
        contenidoDeArchivo = limpiarComentarios(ArchivoContenidoSinProcesar)
        TAMANIOARCHIVO = len(contenidoDeArchivo)
        ultimaPosicionInicial = 0
        ultimaPosicionAceptable = 0
        izquierdaDereclaraciones = {}
        salidaActual = []
        actualId = str()
        declararId = False
        conteDeParentesis = 0
        primeroEnLlegar = False
        # Aquí guardamos los tipos de los tokens, como una regla de retorno.
        ultimoTipoAceptable = []
        # Aquí vamos a estar guardando los tokens.
        organizadorTokens = []
        actualPosicion = 0
        ultimaPosicionInicial = 0
        
        while (actualPosicion < TAMANIOARCHIVO):
            tipoDeAceptacion = []
            
            idMegaAutomataSimulacionEstado = idMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            operadoresMegaAutomataSimulacionEstado = operadoresMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
            caracterMegaAutomataSimulacionEstado = caracterMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
            cadenaMegaAutomataSimulacionEstado = cadenaMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            izquierdaMegaAutomataSimulacionEstado = izquierdaMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
            separadorMegaAutomataSimulacionEstado = separadorMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            IgualMegaAutomataSimulacionEstado = IgualMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            abrirParentesisMegaAutomataSimulacionEstado = abrirParentesisMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
            abrirSetMegaAutomataSimulacionEstado = abrirSetMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            cerrarSetMegaAutomataSimulacionEstado = cerrarSetMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
            cerrarParentesisMegaAutomataSimulacionEstado = cerrarParentesisMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            uncaracterMegaAutomataSimulacionEstado = uncaracterMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            rangoMegaAutomataSimulacionEstado = rangoMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
            reglaMegaAutomataSimulacionEstado = reglaMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            desabilitadosMegaAutomataSimulacionEstado = desabilitadosMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

            if separadorMegaAutomataSimulacionEstado == 1:
                if(actualPosicion+1<= TAMANIOARCHIVO):
                    ultimaPosicionInicial = actualPosicion+1
                    ultimaPosicionAceptable = actualPosicion+1
                    
            if separadorMegaAutomataSimulacionEstado == -1:
                if ultimaPosicionAceptable == actualPosicion:
                    #reiniciar MegaAutomatas y volver a simular
                    funciones (izquierdaMegaAutomata,separadorMegaAutomata,idMegaAutomata,IgualMegaAutomata,abrirSetMegaAutomata,cerrarSetMegaAutomata,abrirParentesisMegaAutomata,cerrarParentesisMegaAutomata,operadoresMegaAutomata,caracterMegaAutomata,cadenaMegaAutomata,uncaracterMegaAutomata,rangoMegaAutomata,reglaMegaAutomata,desabilitadosMegaAutomata)

                    #simular
                    idMegaAutomataSimulacionEstado = idMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    operadoresMegaAutomataSimulacionEstado = operadoresMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
                    caracterMegaAutomataSimulacionEstado = caracterMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
                    cadenaMegaAutomataSimulacionEstado = cadenaMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    izquierdaMegaAutomataSimulacionEstado = izquierdaMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
                    separadorMegaAutomataSimulacionEstado = separadorMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    IgualMegaAutomataSimulacionEstado = IgualMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    abrirParentesisMegaAutomataSimulacionEstado = abrirParentesisMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
                    abrirSetMegaAutomataSimulacionEstado = abrirSetMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    cerrarSetMegaAutomataSimulacionEstado = cerrarSetMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
                    cerrarParentesisMegaAutomataSimulacionEstado = cerrarParentesisMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    uncaracterMegaAutomataSimulacionEstado = uncaracterMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    rangoMegaAutomataSimulacionEstado = rangoMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
                    reglaMegaAutomataSimulacionEstado = reglaMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])

                    desabilitadosMegaAutomataSimulacionEstado = desabilitadosMegaAutomata.simulate(contenidoDeArchivo[actualPosicion])
            
            if izquierdaMegaAutomata.simulate(contenidoDeArchivo[actualPosicion]) == izquierdaMegaAutomata.get_accepting_state():
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('LET')

            if reglaMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('RULE')

            if uncaracterMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('ANYCHAR')
            
            if idMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('ID')
            
            if IgualMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('EQUAL')

            if abrirSetMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('OPEN_SET')
            
            if cerrarSetMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('CLOSE_SET')
            
            if abrirParentesisMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('OPEN_PARENTHESIS')
            
            if cerrarParentesisMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('CLOSE_PARENTHESIS')
            
            if operadoresMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('OPERATOR')

            if desabilitadosMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('DISABLED_OPERATOR')
                
            if caracterMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('CHAR')
            
            if cadenaMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('STRING')

            if rangoMegaAutomataSimulacionEstado == 1:
                ultimaPosicionAceptable = actualPosicion
                tipoDeAceptacion.append('RANGE')

            if len(tipoDeAceptacion) > 0:
                ultimoTipoAceptable = tipoDeAceptacion.copy()

            if((izquierdaMegaAutomataSimulacionEstado==-1)and (separadorMegaAutomataSimulacionEstado==-1) and (idMegaAutomataSimulacionEstado==-1) and (IgualMegaAutomataSimulacionEstado==-1) and (abrirSetMegaAutomataSimulacionEstado==-1) and (cerrarSetMegaAutomataSimulacionEstado==-1) and (abrirParentesisMegaAutomataSimulacionEstado==-1) and (cerrarParentesisMegaAutomataSimulacionEstado==-1) and (operadoresMegaAutomataSimulacionEstado==-1) and (caracterMegaAutomataSimulacionEstado==-1) and (cadenaMegaAutomataSimulacionEstado==-1) and (uncaracterMegaAutomataSimulacionEstado==-1) and (rangoMegaAutomataSimulacionEstado==-1)):
                # agregar token
                organizadorTokens.append((contenidoDeArchivo[ultimaPosicionInicial:ultimaPosicionAceptable+1], ultimoTipoAceptable[0]))
                
                # resetear MegaAutomatas
                funciones (izquierdaMegaAutomata,separadorMegaAutomata,idMegaAutomata,IgualMegaAutomata,abrirSetMegaAutomata,cerrarSetMegaAutomata,abrirParentesisMegaAutomata,cerrarParentesisMegaAutomata,operadoresMegaAutomata,caracterMegaAutomata,cadenaMegaAutomata,uncaracterMegaAutomata,rangoMegaAutomata,reglaMegaAutomata,desabilitadosMegaAutomata)
                ultimaPosicionInicial = actualPosicion

            else:
                actualPosicion += 1
            
            if (actualPosicion == len(contenidoDeArchivo) and separadorMegaAutomataSimulacionEstado !=1 ): #esto es valido cuando el string no termina con delims
                organizadorTokens.append((contenidoDeArchivo[ultimaPosicionInicial:ultimaPosicionAceptable+1], ultimoTipoAceptable[0]))


        for token in organizadorTokens:
            if token[1] in ['LET', 'RULE']:
                if len(salidaActual) > 0:
                    izquierdaDereclaraciones[actualId] = salidaActual
                salidaActual = []
                actualId = str()
                declararId = True

            elif token[1] == 'ID':
                if declararId:
                    actualId = token[0]
                else:
                    salidaActual += izquierdaDereclaraciones[token[0]]

            elif token[1] == 'EQUAL':
                declararId = False
            
            elif token[1] in ['OPEN_PARENTHESIS', 'OPEN_SET']:
                salidaActual.append('(')
                if token[1] == 'OPEN_SET':
                    primeroEnLlegar = True
                    conteDeParentesis += 1
            
            elif token[1] in ['CLOSE_PARENTHESIS', 'CLOSE_SET']:
                salidaActual.append(')')
                if token[1] == 'CLOSE_SET':
                    conteDeParentesis -= 1
            
            elif token[1] in ['OPERATOR', 'DISABLED_OPERATOR']:
                if token[1] == 'DISABLED_OPERATOR' and conteDeParentesis > 0:
                    if primeroEnLlegar:
                        primeroEnLlegar = False
                        salidaActual.append('\\'+token[0][1])
                    else:
                        salidaActual += ['|', '\\'+token[0][1]]
                else:
                    salidaActual.append(token[0])#Como es un char tambien y asumimos que todo esta bien, podemos asegurar que la posicion 1 es el char
            
            elif token[1] == 'CHAR':
                if conteDeParentesis > 0:
                    if primeroEnLlegar:
                        primeroEnLlegar = False
                        salidaActual.append(token[0][1])
                    else:
                        salidaActual.append('|')
                        salidaActual.append(token[0][1])
                else:
                    salidaActual.append(token[0][1]) #Como es un char y asumimos que todo esta bien, podemos asegurar que la posicion 1 es el char
            
            elif token[1] == 'STRING':
                string_size = len(token[0])
                recognized_string = token[0][1:string_size-1]
                if conteDeParentesis > 0:
                    if primeroEnLlegar:
                        primeroEnLlegar = False
                        salidaActual = salidaActual + concatenearListaOr(list(recognized_string))
                    else:
                        salidaActual.append('|')
                        salidaActual = salidaActual + concatenearListaOr(list(recognized_string))

                else:
                    salidaActual.append(recognized_string)
            elif token[1] == 'RANGE':
                    rangoDeCaracteres = concatenearListaOr(conjuntoDeRangoCaracteres(token[0][1], token[0][-2]))
                    if conteDeParentesis > 0:
                        if primeroEnLlegar:
                            primeroEnLlegar = False
                            salidaActual += rangoDeCaracteres
                        else:
                            salidaActual += ['|'] + rangoDeCaracteres
                    else:
                        salidaActual += rangoDeCaracteres
            elif token[1] == 'ANYCHAR':
                if conteDeParentesis > 0:
                    if primeroEnLlegar:
                        primeroEnLlegar = False
                        salidaActual += anychar_regex
                    else:
                        salidaActual += ['|'] + anychar_regex
                else:
                    salidaActual += anychar_regex
                            
            print('\n\nRegla: ')
            print(actualId, ':', concatenate_strings(salidaActual))

    except:
        print("ERROR: El path fue mal ingresado. Intente de nuevo.")


def leerNombreFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        contenidoDelArchivo = file.read()
        secuenciaSaltoLinea = file.newlines
        file.close()
    return contenidoDelArchivo

def formato(entrada):
    simbolos = ['|', '*', '+', '?']  # lista de operadores
    resultado = []  # lista para guardar el resultado
    entrada = '(' + entrada + ')'  # añade paréntesis al principio y final para facilitar el procesamiento
    
    for i in range(len(entrada)):
        if entrada[i] in simbolos or entrada[i] == '(' or entrada[i] == ')':
            resultado.append(entrada[i])
        else:
            resultado.append('•' + entrada[i] + '•')
    
    resultado = ''.join(resultado)  # une los caracteres en una sola cadena
    resultado = resultado.replace('(•', '(')  # elimina puntos intermedios redundantes
    resultado = resultado.replace('•)', ')')
    resultado = resultado.replace('••', '•')  # elimina dobles puntos intermedios
    resultado = resultado[1:-1]  # elimina los paréntesis añadidos al principio y final
    return resultado

def validar(entrada):
    # Validamos que la entrada no sea vacía
    if not entrada:
        print('ERROR: Input invalido, la entrada es vacia')
        return False
    # Validamos que el caracter "." no se encuentre en la entrada
    if '.' in entrada:
        print('ERROR: Input invalido, . es un caracter reservado')
        return False
    # Validamos que no existan dos o más símbolos OR consecutivos
    if any(a == b == '|' for a, b in zip(entrada, entrada[1:])):
        print('ERROR: Input invalido, dos o mas OR consecutivos |')
        return False
    # Validamos que no comience con símbolos inválidos
    if entrada[0] in ('*', '+', '?', '|', '.'):
        print('ERROR: Input invalido, simbolos al inicio no son validos')
        return False
    # Validamos que no termine con símbolos inválidos
    if entrada.endswith(('|', '.')):
        print('ERROR: Input invalido, simbolos no validos')
        return False
    # Validamos que no existan parentesis vacíos
    if '()' in entrada:
        print('ERROR: Input invalido, no parentesis')
        return False
    # Validamos que no haya operadores inmediatamente después de un paréntesis abierto
    if any((entrada[i] == '(' and entrada[i+1] in '+*?|.') for i in range(len(entrada)-1)):
        print('ERROR: Input invalido, los operadores despues de un parentisis abierto no son validos.')
        return False
    # Validamos que no haya símbolos OR o concatenación inmediatamente antes o después de un paréntesis
    if any((entrada[i] in '|.' and (i == 0 or entrada[i-1] in '|(' or entrada[i+1] in '|)')) for i in range(len(entrada))):
        print('ERROR: Input invalido: {} no valido'.format(entrada[i]))
        return False
    # Validamos que los paréntesis estén balanceados
    contadorParentesis = 0
    for i, c in enumerate(entrada):
        if c == '(':
            contadorParentesis += 1
        elif c == ')':
            contadorParentesis -= 1
        if contadorParentesis < 0:
            print(f'ERROR: Input invalido. Los parentesis no coinciden: no puede cerrar parentesis que no fue abrierto. Error en posición: {i}')
            return False
    if contadorParentesis != 0:
        print('ERROR: Input invalido, los parentesis no coinciden.')
        return False
    # Si pasa todas las validaciones, retorna True
    return True

def concatenate_strings(string_list):
    # inicializa una cadena vacía como resultado
    result = ""
    # itera sobre cada cadena en la lista de cadenas
    for string in string_list:
        # agrega la cadena actual al resultado
        result += string
    # devuelve el resultado final
    return result


def limpiarComentarios(raw_input):
    """
    Esta función recibe una cadena de texto y devuelve la misma cadena sin comentarios.
    """
    sin_comentarios = []  # Inicializa una lista vacía donde se irán almacenando los caracteres sin comentarios
    i = 0  # Inicializa el contador de posición en cero
    while i < len(raw_input):  # Mientras no se llegue al final de la cadena
        if raw_input[i:i+2] == '/*':  # Si se encuentra un inicio de comentario
            i += 2  # Se salta los caracteres '/*'
            while raw_input[i:i+2] != '*/':  # Se busca el final del comentario
                i += 1
                if i == len(raw_input):  # Si se llega al final de la cadena y no se encontró el final del comentario
                    raise ValueError('Error: comentario no cerrado')  # Se lanza una excepción
            i += 2  # Se salta los caracteres '*/'
        else:
            sin_comentarios.append(raw_input[i])  # Si no se encuentra un inicio de comentario, se agrega el caracter a la lista
            i += 1  # Y se avanza al siguiente caracter
    return removerEntreLlaves(''.join(sin_comentarios))  # Se convierte la lista de caracteres en una cadena y se remueven los comentarios internos

#Referencia: https://www.digitalocean.com/community/tutorials/python-ord-chr
def conjuntoDeRangoCaracteres(caracter1, caracter2):
    # Validamos que los caracteres sean de longitud 1
    if len(caracter1) != 1 or len(caracter2) != 1:
        print('ERROR: Input invalido, caracteres deben ser de longitud 1')
        return False
    # Obtenemos los valores ASCII de los caracteres
    pos1 = ord(caracter1)
    pos2 = ord(caracter2)
    # Si los caracteres están en desorden, los intercambiamos
    if pos1 > pos2:
        pos1, pos2 = pos2, pos1
    # Creamos una lista de caracteres a partir de los valores ASCII en el rango
    # entre pos1 y pos2, y la devolvemos.
    lista_caracteres = [chr(pos) for pos in range(pos1, pos2 + 1)]
    # Si la lista resultante es vacía, es porque el rango no es válido
    if not lista_caracteres:
        print('ERROR: Input invalido, rango de caracteres no valido')
        return False
    # Si la lista resultante contiene más de un caracter, es porque el rango
    # incluye más de un caracter, lo cual no es válido para esta función
    if len(lista_caracteres) > 1:
        print('ERROR: Input invalido, rango debe ser de un solo caracter')
        return False
    # Si pasa todas las validaciones, retorna True
    return True

# Esta función toma un texto como entrada y devuelve una versión del texto sin contenido entre llaves { }
def removerEntreLlaves(text):
    resultado = ""  # Se inicializa una variable vacía para almacenar el texto resultante
    ignorar = False  # Se inicializa una variable booleana que indica si se debe ignorar el contenido entre llaves
    escapar = False  # Se inicializa una variable booleana que indica si el carácter actual debe ser escapado
    for char in text:  # Se itera a través de cada carácter del texto de entrada
        if escapar:  # Si el carácter anterior fue una barra invertida, se agrega el carácter actual escapado al resultado
            resultado += {"n": "\n", "t": "\t", "s": " "}.get(char, "\\" + char)
            escapar = False
        elif char == "\\":  # Si el carácter actual es una barra invertida, se activa el modo de escape
            escapar = True
        elif char == "{":  # Si el carácter actual es una llave abierta, se activa el modo de ignorar contenido
            ignorar = True
        elif char == "}":  # Si el carácter actual es una llave cerrada, se desactiva el modo de ignorar contenido
            ignorar = False
        elif not ignorar:  # Si no se está ignorando contenido, se agrega el carácter actual al resultado
            resultado += char
    return resultado  # Se devuelve el texto resultante sin contenido entre llaves

def construirArbolDesdeInfix(entradaUsuario):
    # formatear la entrada del usuario (eliminar espacios en blanco y agregar multiplicación implícita)
    entradaUsuario = formato(entradaUsuario)
    # convertir la expresión infix en postfix usando el algoritmo shunting yard
    output = shuntingYard(entradaUsuario)
    # imprimir la expresión postfix
    print('Postfix: ', output)

    # Crear el árbol de expresión a partir de la expresión postfix
    pila = []
    for elemento in output:
        if esOperando(elemento):
            pila.append(Nodo(elemento))
        else:
            nodo_der = pila.pop()
            nodo_izq = pila.pop()
            nodo_operador = Nodo(elemento, nodo_izq, nodo_der)
            pila.append(nodo_operador)

    tree = pila.pop()
    # crear un objeto de gráfico para visualizar el árbol de expresión
    digraph = Digraph(graph_attr={'dpi': str(200)})
    # recorrido transversal en postorden para dibujar el árbol en el objeto digraph
    postorderTransversalDibujo(tree, digraph)
    # renderizar el gráfico como imagen png en el directorio output con el nombre "ArboldeExpresion"
    digraph.render('output/ArboldeExpresion', format='png')
    # devolver el árbol de expresión
    return tree

def esOperando(elemento):
    return elemento.isalpha() or elemento.isdigit()

class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

def construirAutomataDirecto(entrada):
    # Formatear la entrada en una lista de caracteres y convertir a postfix con el algoritmo Shunting Yard
    entrada = formato(entrada)
    output = shuntingYard(entrada)
    # Construir el árbol de sintaxis directamente desde el postfix generado por Shunting Yard
    arbol, followpos, listaCaracteres = ConstruirArbolDirecto(output)
    # Construir un autómata determinista a partir del árbol de sintaxis directamente
    det_MegaAutomata = direct_construction(followpos, arbol.primeraPosicion, arbol.ultimaPosicion, listaCaracteres)
    clean_transitions(det_MegaAutomata) # Limpiar transiciones innecesarias en el autómata generado
    return det_MegaAutomata # Retornar el autómata construido

def postorderTransversalDibujo(nodo, digraph):
    if nodo is not None: # Si el nodo no es nulo, se procede con el recorrido transversal en postorden
        postorderTransversalDibujo(nodo.izq, digraph) # Se realiza el recorrido transversal en postorden del subárbol izquierdo.
        postorderTransversalDibujo(nodo.der, digraph)# Se realiza el recorrido transversal en postorden del subárbol derecho.
        digraph.node(str(nodo), str(nodo.valor)) # Se agrega un nodo al objeto Digraph con el valor del nodo actual.
        if nodo.izq is not None: # Si el nodo tiene un hijo izquierdo, se agrega una arista desde el nodo actual hacia el hijo izquierdo.
            digraph.edge(str(nodo), str(nodo.izq))
        if nodo.der is not None:# Si el nodo tiene un hijo derecho, se agrega una arista desde el nodo actual hacia el hijo derecho
            digraph.edge(str(nodo), str(nodo.der))

def concatenearListaOr(lista):
    result = ['('] # se inicializa la lista con un paréntesis izquierdo
    if len(lista) > 0: # si la lista no está vacía, se añade el primer elemento a la lista de resultado
        result.append(lista[0])
        for i in range(1, len(lista)): # se itera sobre los demás elementos de la lista
            result.append('|') # se añade el operador lógico OR
            result.append(lista[i]) # se añade el elemento actual a la lista de resultado
    result.append(')') # se añade el paréntesis derecho al final
    return result # se devuelve la lista de resultado

def concatenearOr(lista):
    return '(' + '|'.join(lista) + ')'

    
