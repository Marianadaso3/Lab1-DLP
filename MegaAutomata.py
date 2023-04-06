"""
Referencias:
1. https://github.com/Lukehilmes2/shunting-yard
2. https://rosettacode.org/wiki/Parsing/Shunting-yard_algorithm
3. https://machinelearningmastery.com/multi-output-regression-models-with-python/
4. https://www.geeksforgeeks.org/binarytree-module-in-python/
5. https://cc4.gitbook.io/cc4/laboratorios/lab-3
6. https://stackoverflow.com/questions/53075326/handling-chained-unary-operators-in-shunting-yard
7. https://groups.csail.mit.edu/mac/ftpdir/scheme-7.4/doc-html/scheme_6.html
8. https://github.com/topics/lexer-generator?l=python
9. https://github.com/topics/lexer-parser?l=python
10. Logica implementada de: https://github.com/JJHH06
"""
from graphviz import Digraph

class MegaAutomata:
    # Constructor de la clase
    def __init__(self, estado, alfabeto, transicion, estadoInicial, estadoFinal):
        self.estado = estado  # Conjunto de estados del autómata
        self.alfabeto = alfabeto  # Alfabeto del autómata
        self.transicion = transicion  # Transiciones del autómata
        self.estadoInicial = estadoInicial  # Estado inicial del autómata
        self.estadoFinal = estadoFinal  # Conjunto de estados finales del autómata
        self.estadoDeSimulacion = -1  # Estado actual de la simulación, inicializado en -1

    # Método que simula la entrada de un símbolo y devuelve el estado actual de la simulación
    def simulate(self, symbol):
        if self.estadoDeSimulacion == -1:  # Si el estado actual es -1, la simulación no se puede realizar
            return -1
        next_state = self.moverEstado(self.estadoDeSimulacion, symbol)
        if next_state == -1:  # Si no se encuentra una transición para el símbolo de entrada, la simulación no se puede realizar
            return -1
        # La simulación continúa si se encuentra una transición para el símbolo de entrada
        self.estadoDeSimulacion = next_state
        # Se verifica si el estado actual es un estado final y se devuelve el resultado correspondiente
        return 1 if self.estadoDeSimulacion in self.estadoFinal else 0

   # Método que mueve el estado actual a un estado siguiente dado un símbolo de entrada
    def moverEstado(self, state, symbol):
        for origin, dest, sym in self.transicion:
            if origin == state and sym == symbol:
                self.estadoDeSimulacion = dest
                return dest
        self.estadoDeSimulacion = -1
        return -1

    # Método que devuelve el estado siguiente al moverse desde un estado actual dado un símbolo de entrada
    def estadoMovimineto(self, estado, simbolo):
        return [transition[1] for transition in self.transicion if transition[0] == (estado, simbolo)]

        # Método que devuelve el cierre epsilon de un estado dado
    def ciereEpsilon(self, estado):
        # Inicializar el cierre con el estado dado
        cierre = [estado]

        # Mientras se sigan agregando nuevos estados al cierre
        i = 0
        while i < len(cierre):
            closure_state = cierre[i]
            # Buscar todas las transiciones con el símbolo epsilon que salen del estado actual
            for transicion in self.transicion:
                if transicion[0] == (closure_state, 'ε'):
                    nuevo_estado = transicion[1]
                    # Si el nuevo estado no está en el cierre, agregarlo y seguir buscando transiciones
                    if nuevo_estado not in cierre:
                        cierre.append(nuevo_estado)
            i += 1
        return cierre

    # Método que reinicia la simulación del autómata
    def reiniciarSimulacion(self):
        self.estadoDeSimulacion = self.estadoInicial

def clean_transitions(MegaAutomata: MegaAutomata):
    # Lista de caracteres especiales que serán ignorados
    ignorarCaracteres = ['|', '(', ')', '*', '+', '?']
    # Inicialización de la nueva lista de transiciones
    nuevaTransicion = []
    # Inicialización del nuevo conjunto de caracteres del alfabeto
    nuevoAlfabeto = set()

    # Recorre cada transición en la lista de transiciones del MegaAutomata
    for transicion in MegaAutomata.transicion:
        # Si la longitud de la etiqueta es 2 y el primer caracter es '\' y el segundo caracter está en la lista de caracteres a ignorar
        if len(transicion[0][1]) == 2 and transicion[0][1][0] == '\\' and transicion[0][1][1] in ignorarCaracteres:
            # Agrega una nueva transición con la misma salida pero con el segundo caracter de la etiqueta original como entrada
            nuevaTransicion.append(((transicion[0][0], transicion[0][1][1]), transicion[1]))
        else:
            # Agrega la transición original a la nueva lista de transiciones
            nuevaTransicion.append(transicion)

        # Si la etiqueta original no está en la lista de caracteres a ignorar
        if transicion[0][1] not in ignorarCaracteres:
            # Agrega la etiqueta original al nuevo conjunto de caracteres del alfabeto
            nuevoAlfabeto.add(transicion[0][1])

    # Actualiza el alfabeto del MegaAutomata con el nuevo conjunto de caracteres del alfabeto
    MegaAutomata.alfabeto = nuevoAlfabeto

    # Actualiza la lista de transiciones del MegaAutomata con la nueva lista de transiciones
    MegaAutomata.transicion = nuevaTransicion

def operando_MegaAutomata(subexpression, current_state):
    # operando thomspon MegaAutomata
    estados = [current_state, current_state+1]
    alfabeto = {subexpression}
    estadoInicial = current_state
    estadoFinal = [current_state+1]
    transiciones = [((current_state, subexpression), current_state+1)]
    return MegaAutomata(estados, alfabeto, transiciones, estadoInicial, estadoFinal)

def DFA_simulacion(automata: MegaAutomata, cadena: str) -> bool:
    # Empezamos en el estado inicial del autómata
    estado_actual = automata.estadoInicial
    
    # Procesamos cada símbolo de la cadena de entrada
    for simbolo in cadena:
        # Movemos al siguiente estado según el símbolo actual
        siguiente_estado = automata.estadoMovimineto(estado_actual, simbolo)
        
        # Si el siguiente estado es vacío, la cadena no es aceptada
        if not siguiente_estado:
            return False
        
        # Actualizamos el estado actual al siguiente estado
        estado_actual = siguiente_estado[0]
    
    # Si llegamos al final de la cadena, chequeamos si el estado actual es final
    return estado_actual in automata.estadoFinal

def direct_construction(tablaPos, estadoInicial, estadoFinal, alfabetoLista):
    # Inicializar el conjunto de símbolos del alfabeto determinista
    deterministaAlfabeto = set(alfabetoLista)
    
    # Inicializar el estado equivalente con el estado inicial
    estadoEquivalente = [estadoInicial]
    
    # Inicializar la lista de transiciones directas
    transicionDirecta = []
    
    # Crear un diccionario que almacene la posición de cada símbolo del alfabeto en alfabetoLista
    hojaPosicion = {}
    for character in deterministaAlfabeto:
        hojaPosicion[character] = [i for i in range(len(alfabetoLista)) if alfabetoLista[i] == character]
    
    # Iterar sobre todos los estados equivalentes actuales
    for estado in estadoEquivalente:
        # Iterar sobre todos los símbolos del alfabeto determinista
        for simbolo in deterministaAlfabeto:
            # Inicializar el conjunto de estados que son transiciones directas del estado actual por el símbolo actual
            siguienteEstado = set()
            
            # Iterar sobre todos los estados NFA que están en el estado actual y tienen el símbolo actual
            for nfa_estado in estado:
                if nfa_estado in hojaPosicion[simbolo]:
                    siguienteEstado |= set(tablaPos[nfa_estado])
            
            # Si el conjunto de estados siguientes no está vacío
            if siguienteEstado:
                # Si el conjunto de estados siguientes no está en estadoEquivalente, agregarlo
                if siguienteEstado not in estadoEquivalente:
                    estadoEquivalente.append(siguienteEstado)
                
                # Agregar la transición directa al nuevo estado siguiente
                transicionDirecta.append(((estadoEquivalente.index(estado), simbolo), estadoEquivalente.index(siguienteEstado)))
    
    # Identificar el estado equivalente final
    estadoEquivalenteFinal = set()
    for i, eq_estado in enumerate(estadoEquivalente):
        if any(estado in estadoFinal for estado in eq_estado):
            estadoEquivalenteFinal.add(i)
    
    # Crear el automata
    return MegaAutomata([i for i in range(len(estadoEquivalente))], deterministaAlfabeto, transicionDirecta, 0, list(estadoEquivalenteFinal))

def InterrogacionAutomata(MegaAutomata, current_state):
    # Creamos un nuevo MegaAutomata con un estado inicial de epsilon
    epsilon_MegaAutomata = operando_MegaAutomata('ε', 0)
    # Sumamos el estado actual por 2 para evitar conflictos de estado y unimos los MegaAutomatas usando una operación OR
    MegaAutomata_con_epsilon = or_MegaAutomata(MegaAutomata, epsilon_MegaAutomata, current_state+2)
    # Retornamos el nuevo MegaAutomata con epsilon incluido
    return MegaAutomata_con_epsilon

def or_MegaAutomata(right_MegaAutomata, left_MegaAutomata, current_state):
    # Create a new list with the states of both MegaAutomata plus two new states
    new_states = left_MegaAutomata.states + right_MegaAutomata.states + [current_state, current_state+1]
    # Create a new list with the transitions of both MegaAutomata plus new transitions
    new_transitions = left_MegaAutomata.transitions + right_MegaAutomata.transitions + [((current_state, 'ε'), left_MegaAutomata.initial_state), ((current_state, 'ε'), right_MegaAutomata.initial_state)]
    # Add new transitions from the final states of both MegaAutomata to a new final state
    new_transitions += [((final_state, 'ε'), current_state+1) for final_state in left_MegaAutomata.final_states] + [((final_state, 'ε'), current_state+1) for final_state in right_MegaAutomata.final_states]
    # Create a new set with the alphabet of both MegaAutomata plus the empty string
    new_alphabet = left_MegaAutomata.alphabet.union(right_MegaAutomata.alphabet) | {'ε'}
    # Set the initial state to the current state
    new_initial_state = current_state
    # Set the final state to a new state
    new_final_state = [current_state+1]
    # Create and return the new MegaAutomata
    return MegaAutomata(new_states, new_alphabet, new_transitions, new_initial_state, new_final_state)

def kleene_MegaAutomata(M):
    import copy
   # crea copia profunda del MegaAutomata original
    M_copy = copy.deepcopy(M)
    # obtiene los estados actuales
    estados = M.states
    # define nuevos estados
    estadoInicial = max(estados) + 1
    estadoFinal = estadoInicial + 1
    nuevos_estados = [estadoInicial, estadoFinal]
    # añade los nuevos estados al MegaAutomata
    estados.extend(nuevos_estados)
    # añade transiciones para la cerradura de Kleene
    for estado in M.final_states:
        M_copy.transitions.append(((estado, 'ε'), M.initial_state))
    M_copy.transitions.append(((estadoInicial, 'ε'), M.initial_state))
    for estado in M.final_states:
        M_copy.transitions.append(((estado, 'ε'), estadoFinal))
    M_copy.transitions.append(((estadoInicial, 'ε'), estadoFinal))
    # añade estado inicial y final
    M_copy.initial_state = estadoInicial
    M_copy.final_states = [estadoFinal]
    return M_copy

def cerraduraPositivaAutomata(MegaAutomata, current_state):
    import copy
    # Se obtiene una copia del automata y un offset para los estados
    MegaAutomata_copy, state_offset = MegaAutomataEstadoCambio(MegaAutomata)
    # Se obtiene el automata de Kleene del automata original empezando en el estado actual
    kleene_automata = kleene_MegaAutomata(MegaAutomata_copy, current_state + state_offset)
    # Se concatena el automata original con el automata de Kleene para obtener la cerradura positiva
    resultado_automata = concatenation_MegaAutomata(MegaAutomata, kleene_automata)
    # Se ajusta el offset para los estados
    state_offset += 2
    return resultado_automata, state_offset

def concatenation_MegaAutomata(right_MegaAutomata, left_MegaAutomata):
    # Obtener los estados del primer MegaAutomata excepto los estados finales
    estados_primer_automata = [estado for estado in left_MegaAutomata.states if estado not in left_MegaAutomata.final_states]
    # Obtener todos los estados del segundo MegaAutomata
    estados_segundo_automata = right_MegaAutomata.states
    # Combinar los estados de ambos MegaAutomatas
    estados = estados_primer_automata + estados_segundo_automata
    # Obtener el estado inicial del primer MegaAutomata
    estadoInicial = left_MegaAutomata.initial_state
    # Obtener los estados finales del segundo MegaAutomata
    estadoFinal = right_MegaAutomata.final_states
    # Obtener la unión de los alfabetos de ambos MegaAutomatas
    alfabeto = left_MegaAutomata.alphabet.union(right_MegaAutomata.alphabet)
    # Obtener las transiciones del primer MegaAutomata
    transiciones = left_MegaAutomata.transitions.copy()
    # Agregar las transiciones del segundo MegaAutomata
    for transicion in right_MegaAutomata.transitions:
        transiciones.append(transicion)
    # Actualizar las transiciones para que los estados finales del primer MegaAutomata 
    # transicionen al estado inicial del segundo MegaAutomata
    for i, transicion in enumerate(transiciones):
        origen, simbolo = transicion[0]
        destino = transicion[1]
        if origen in left_MegaAutomata.final_states:
            transiciones[i] = ((origen, simbolo), right_MegaAutomata.initial_state)
    # Crear el nuevo MegaAutomata con los valores obtenidos
    nuevo_MegaAutomata = MegaAutomata(estados, alfabeto, transiciones, estadoInicial, estadoFinal)
    # Devolver el nuevo MegaAutomata
    return nuevo_MegaAutomata

def MegaAutomataEstadoCambio(MegaAutomata):
    # Creamos una copia del autómata original
    MegaAutomataTemp = MegaAutomata.copy()
    # Definimos el estado apagado como el máximo estado actual + 1
    estadoApagado = max(MegaAutomataTemp.states) + 1
    # Actualizamos los estados del autómata sumando el estado apagado
    MegaAutomataTemp.states = [estado + estadoApagado for estado in MegaAutomataTemp.states]
    MegaAutomataTemp.initial_state += estadoApagado
    MegaAutomataTemp.final_states = [state + estadoApagado for state in MegaAutomataTemp.final_states]
    # Actualizamos las transiciones sumando el estado apagado a los estados correspondientes
    nuevas_transiciones = []
    for transicion, destino in MegaAutomataTemp.transitions:
        estado_origen, simbolo = transicion
        nuevas_transiciones.append(((estado_origen + estadoApagado, simbolo), destino + estadoApagado))
    MegaAutomataTemp.transitions = nuevas_transiciones
    # Retornamos la copia actualizada del autómata y el estado apagado
    return MegaAutomataTemp, estadoApagado

def construccionMegaAutomata(postfix_expression):
    operadores = ['*','+','?']
    operadoresBinarios = ['|','.']
    pila = []
    estados = [0]  # lista de estados disponibles, el primer estado siempre es 0
    for token in postfix_expression:
        if token not in operadores and token not in operadoresBinarios:
            # si el token es un operando, se crea un nuevo estado y se agrega al árbol
            nuevo_estado = estados[-1] + 1  # el nuevo estado es el último más uno
            pila.append(operando_MegaAutomata(token, nuevo_estado))
            estados.append(nuevo_estado)
        elif token == '|':
            # si el token es una barra, se combinan los dos árboles más recientes con un nuevo estado
            nuevo_estado = estados[-1] + 1
            arbol1 = pila.pop()
            arbol2 = pila.pop()
            pila.append(or_MegaAutomata(arbol1, arbol2, nuevo_estado))
            estados.append(nuevo_estado)
        elif token == '.':
            # si el token es un punto, se combinan los dos árboles más recientes sin crear un nuevo estado
            arbol1 = pila.pop()
            arbol2 = pila.pop()
            pila.append(concatenation_MegaAutomata(arbol1, arbol2))
        elif token == '*':
            # si el token es un asterisco, se agrega un nuevo estado y se aplica la cerradura de Kleene
            nuevo_estado = estados[-1] + 1
            arbol = pila.pop()
            pila.append(kleene_MegaAutomata(arbol, nuevo_estado))
            estados.append(nuevo_estado)
        elif token == '?':
            # si el token es una interrogación, se agregan dos nuevos estados y se aplica la operación de opción
            nuevo_estado1 = estados[-1] + 1
            nuevo_estado2 = estados[-1] + 2
            arbol = pila.pop()
            pila.append(InterrogacionAutomata(arbol, nuevo_estado1, nuevo_estado2))
            estados.append(nuevo_estado1)
            estados.append(nuevo_estado2)
        elif token == '+':
            # si el token es un signo más, se agregan dos nuevos estados y se aplica la cerradura positiva
            nuevo_estado1 = estados[-1] + 1
            nuevo_estado2 = estados[-1] + 2
            arbol = pila.pop()
            plus_closure_element, estadoApagadoSet = cerraduraPositivaAutomata(arbol, nuevo_estado1, nuevo_estado2)
            pila.append(plus_closure_element)
            estados.append(nuevo_estado1)
            estados.append(estadoApagadoSet)
    return pila.pop()

#Creamos clase arbol para aut
class Arbol:
    def __init__(self, raiz, primeraPosicion = None, ultimaPosicion = None, null = None):
        self.key = raiz
        self.hijoIzquierdo = None
        self.hijoDerecho = None
        self.primeraPosicion = primeraPosicion
        self.ultimaPosicion = ultimaPosicion
        self.nullable = null

def crearArbol(postfix_expression):
    operadores_unarios = ['*', '+', '?']
    operadores_binarios = ['|', '•']
    pila = []
    for token in postfix_expression:
        # si el token es un operando válido, se crea un árbol con su valor y se apila
        if token not in operadores_unarios and token not in operadores_binarios:
            pila.append(Arbol(token))
        # si el token es un operador binario, se sacan los dos últimos elementos de la pila y se cre un árbol con el operador como raíz y los elementos como hijos
        elif token in operadores_binarios:
            hijo_derecho = pila.pop()
            hijo_izquierdo = pila.pop()
            operador = Arbol(token)
            operador.hijoIzquierdo = hijo_izquierdo
            operador.hijoDerecho = hijo_derecho
            pila.append(operador)
        # si el token es un operador unario, se saca el último elemento de la pila y se crea un árbol con el operador como raíz y el elemento como hijo
        elif token in operadores_unarios:
            hijo = pila.pop()
            operador = Arbol(token)
            operador.hijoIzquierdo = hijo
            pila.append(operador)
    # al final queda solo un elemento en la pila, que es el árbol de toda la expresión
    return pila.pop()

def ConstruirArbolDirecto(postfix_expression):
    posicionHojas = []
    operadores = {
        '*': lambda x: (x.nullable, x.primeraPosicion.copy(), x.ultimaPosicion.copy(), [
            tablaDePosiciones[i].union(x.primeraPosicion) for i in x.ultimaPosicion]),
        '+': lambda x: (x.hijoIzquierdo.nullable, x.hijoIzquierdo.primeraPosicion.copy(), x.hijoIzquierdo.ultimaPosicion.copy(), [
            tablaDePosiciones[i].union(x.hijoIzquierdo.primeraPosicion) for i in x.hijoIzquierdo.ultimaPosicion]),
        '?': lambda x: (True, x.hijoIzquierdo.primeraPosicion.copy(), x.hijoIzquierdo.ultimaPosicion.copy(), [])
    }

    def armar_operador(operando1, operando2, operador):
        arbol_operador = Arbol(operador)
        arbol_operador.hijoDerecho = operando2
        arbol_operador.hijoIzquierdo = operando1
        return arbol_operador

    pila = []
    tablaDePosiciones = []

    for token in postfix_expression:
        if token == 'ε':
            pila.append(Arbol(token, set(), set(), True))
        elif token not in operadores.keys():
            hoja = Arbol(token, {len(posicionHojas)}, {len(posicionHojas)}, False)
            posicionHojas.append(token)
            tablaDePosiciones.append(set())
            pila.append(hoja)
        else:
            operador = operadores[token]
            operando2 = pila.pop()
            operando1 = pila.pop()
            arbol_operador = armar_operador(operando1, operando2, token)
            arbol_operador.nullable, arbol_operador.primeraPosicion, arbol_operador.ultimaPosicion, tabla_nuevas_posiciones = operador(arbol_operador)
            tablaDePosiciones.extend(tabla_nuevas_posiciones)
            pila.append(arbol_operador)

    resultadoArbol = armar_operador(pila.pop(), Arbol('#', {len(posicionHojas)}, {len(posicionHojas)}, False), '•')
    resultadoArbol.nullable = resultadoArbol.hijoIzquierdo.nullable and resultadoArbol.hijoDerecho.nullable
    resultadoArbol.primeraPosicion = resultadoArbol.hijoIzquierdo.primeraPosicion.union(resultadoArbol.hijoDerecho.primeraPosicion) if resultadoArbol.hijoIzquierdo.nullable else resultadoArbol.hijoIzquierdo.primeraPosicion.copy()
    resultadoArbol.ultimaPosicion = resultadoArbol.hijoDerecho.ultimaPosicion.union(resultadoArbol.hijoIzquierdo.ultimaPosicion) if resultadoArbol.hijoDerecho.nullable else resultadoArbol.hijoDerecho.ultimaPosicion.copy()

    return resultadoArbol, tablaDePosiciones

# Algoritmo Shunting Yard. Referencia:
def shuntingYard(user_input):
    # Tabla de precedencia para los operadores
    tablaDePresedencia = {'|': 1, '•': 2, '*': 3, '+': 3, '?': 3, '(': -1, ')': -1}
    # Lista de operadores
    operadores = ['|', '*', '+', '?', '•']
    # Lista de salida (los tokens en notación polaca inversa)
    salida = []
    # Pila de operadores
    pilaOperador = []
    
    # Iteramos sobre cada token de la entrada del usuario
    for token in user_input:
        # Si el token es un operador
        if token in operadores:
            # Despachamos los operadores de la pila hasta encontrar un operador con menor o igual precedencia
            while (len(pilaOperador) > 0 and tablaDePresedencia[token] <= tablaDePresedencia[pilaOperador[-1]]):
                salida.append(pilaOperador.pop())
            # Agregamos el operador actual a la pila
            pilaOperador.append(token)
        # Si el token no es un operador
        else:
            # Si el token no es un paréntesis, lo agregamos a la lista de salida
            if token != '(' and token != ')':
                salida.append(token)
            # Si el token es un paréntesis de apertura, lo agregamos a la pila
            elif token == '(':
                pilaOperador.append(token)
            # Si el token es un paréntesis de cierre
            elif token == ')':
                # Despachamos los operadores de la pila hasta encontrar el paréntesis de apertura correspondiente
                while (len(pilaOperador) > 0 and pilaOperador[-1] != '('):
                    salida.append(pilaOperador.pop())
                # Quitamos el paréntesis de apertura de la pila
                pilaOperador.pop()
                
    # Despachamos los operadores restantes en la pila
    while (len(pilaOperador) > 0):
        salida.append(pilaOperador.pop())
    return salida  # Devolvemos la lista de salida

# recorrido postorden del árbol para dibujar
def postorderTransversalDibujo(arbol, digraph):
    # si el árbol no está vacío
    if arbol:
        # recorre el subárbol izquierdo y derecho en orden inverso
        postorderTransversalDibujo(arbol.hijoIzquierdo, digraph)
        postorderTransversalDibujo(arbol.hijoDerecho, digraph)
        # agrega el nodo actual al gráfico con una etiqueta de cadena formateada que representa la llave
        nodeLabel = r"'{}'".format(arbol.key)
        digraph.node(str(id(arbol)), nodeLabel)
        # si hay un hijo derecho, crea una arista al nodo actual
        if arbol.hijoDerecho:
            digraph.edge(str(id(arbol)), str(id(arbol.hijoDerecho)))
        # si hay un hijo izquierdo, crea una arista al nodo actual
        if arbol.hijoIzquierdo:
            digraph.edge(str(id(arbol)), str(id(arbol.hijoIzquierdo)))
    # si el árbol está vacío, simplemente regresa sin hacer nada
    else:
        return
