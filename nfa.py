
#Autor: Mariana David 
#Carnet: 201055
#Diseño y lenguajes de algortimos 
#Laboratorio A

#---------------------Funtes de consulta------------------------
# https://graphviz.org/download/
# https://personales.unican.es/gomezd/teaching/lf/parsing.html
# https://whitemech.github.io/pythomata/


#Importaciones 
from graphviz import Digraph # Metodo que grafica
from graphviz import Source #Metodos que obtener el código fuente en DOT de un grafo generado por Graphviz
from tokens import * 
from graphics import *

#Clase del automata finito no determinista
class NFA:
    def __init__(self, exp_postfix, symbols, regex): #metodo constructor con argumentos simbolos, regex (expresion regular original), postfix
        # Propiedades de un autómata finito
        self.estadosAceptados = [] #almacena los estados de acpetacion en una lista vacia 
        self.symbols = symbols # iniciali la propiedad con el conjutno de simbolos de entrada
        self.trans_func = None #almacena la tabla de transiciones del NFA
        self.estado_actual = 1 # inicializa la porpieda con el estado inicial del NFA

        # Árbol de nodos y expresión regular
        self.regex = regex #inicializa la propiedad regex con la expresión regular original
        self.exp_postfix = exp_postfix #inicializa la propiedad exp_postfix con la expresión regular en notación postfija
        self.regexAccepted = None #Esta propiedad almacenará la versión procesada de la expresión regular para comparar con las cadenas de entrada

        # Propiedades para crear el diagrama
        self.dot = Digraph(comment='Diagrama NFA', strict=True) #inicializa la propiedad dot como un objeto de tipo Digraph de la biblioteca graphviz. Este objeto se utiliza para generar un diagrama del NFA
        self.dot.attr(rankdir='LR') #configura la dirección del diagrama como de izquierda a derecha
        self.dot.attr('node', shape='circle') #configura la forma de los nodos como círculos

        # Se ejecuta el algoritmo
        self.Render(exp_postfix) #Este método se encarga de construir el NFA
        self.trans_func = self.Tabla_trans_generada() # llama al método para generar la tabla de transiciones del NFA
        self.estadosAceptados = list([self.GetEstadoAceptacion()]) #llama al método GetEstadoAceptacion para obtener los estados de aceptación del NFA y los almacena en una lista que contiene un unico elemento que es el estao de acpetacion

    #Renderizacion del nodo en el diagrama del autamata
    def Render(self, node):
        self.prev_state = self.estado_actual  # Guarda el estado actual del autómata como estado previo
        method_name = node.__class__.__name__ + 'Node'  # Obtiene el nombre de la clase del nodo y le añade la palabra 'Node'
        method = getattr(self, method_name)  # Obtiene la referencia al método que coincide con el nombre obtenido
        return method(node)  # Ejecuta el método obtenido pasándole como argumento el nodo a renderizar
    
    #Letra que contenga el nodo 
    def LetraNode(self, node):
        return node.value #deuelve el valor del atirbuto del nodo; aqui se almacena el caracter correspondiente a la letra en la expresion regular

    #Concatenacion de lnodo 
    def AppendNode(self, node):

        self.dot.edge( #metodo de la libreria Graphviz que agrega una arita dirigida entre dos nodos  
            str(self.estado_actual - 1), #Convierte el estado actual menos uno a una cadena de texto para ser utilizado como origen de la arista
            str(self.estado_actual), #Convierte el estado actual a una cadena de texto para ser utilizado como destino de la arista
            self.Render(node.a) #Renderiza el subárbol izquierdo del nodo de concatenación
        )

        self.estado_actual += 1 #Incrementa el estado actual para ser utilizado como origen de la siguiente arista
        self.dot.edge( # Método de la librería Graphviz que agrega una arista dirigida entre dos nodos.
            str(self.estado_actual - 1), #Convierte el estado actual menos uno a una cadena de texto para ser utilizado como origen de la arista
            str(self.estado_actual), #Convierte el estado actual a una cadena de texto para ser utilizado como destino de la arista
            self.Render(node.b) #Renderiza el subárbol derecho del nodo de concatenación
        )

    #Si el nodo utiliza la expresion OR 
    def OrNode(self, node): #recibe un nodo como parámetro
        initial_node = self.estado_actual - 1 #almacenará el estado actual menos uno
        mid_node = None #Se declara la variable mid_node que se inicializa en None

        # inicial a primer épsilon
        self.dot.edge(
            str(initial_node), # Se crea una transición de initial_node al estado actual con el caracter epsilon utilizando el método edge() de la instancia de Digraph
            str(self.estado_actual), 
            'ε'
        )
        self.estado_actual += 1 #Se incrementa el estado actual

        # de epsilon a primera
        self.dot.edge( #llama al método edge() del objeto dot que representa el diagrama NFA. Este método crea una conexión entre dos estados en el diagrama
            str(self.estado_actual - 1), #esta cadena representa el estado actual, antes de crear la conexión
            str(self.estado_actual), #esta cadena representa el estado siguiente, después de crear la conexión
            self.Render(node.a) #renderizar el nodo a de la operación Append
            #La salida de este método es una cadena que representa la etiqueta de la transición entre los estados actuales y siguientes
        )

        mid_node = self.estado_actual #almacena el numero del estado acutal 
        self.estado_actual += 1 # incrementa la variable en 1 para preprarse para el sigueinte estado en la contruccion

        # de la inicial a la segunda epsilon
        self.dot.edge( # crea una nueva transición en el gráfico del autómata finito
            str(initial_node), #dentificador del estado de inicio de la transición
            str(self.estado_actual), # dentificador del estado final de la transición
            'ε' # este es el símbolo de transición que se utiliza para la transición
        )

        self.estado_actual += 1 #  incrementa el valor de la variable

        # de epsilon a segundo
        self.dot.edge( # crea una nueva transición en el diagrama, indicando el estado de inicio, estado final y símbolo de transición
            str(self.estado_actual - 1), # El estado de inicio de la transición es representado por una cadena que corresponde al valor del atributo (-1 para obtener el estaod anterior)
            str(self.estado_actual), # El estado final de la transición
            self.Render(node.b) # se renderiza el contenido del nodo "b" y se utiliza como símbolo de transición en la transición
        )

        self.estado_actual += 1 #incrementa en 1 para que el próximo estado tenga un valor distinto

        # del primero al último épsilon
        self.dot.edge( # creación de una transición en el diagrama
            str(mid_node), # Especifica el nodo de inicio de la transición, se guarda en mid_nod
            str(self.estado_actual), #Especifica el nodo de llegada de la transición
            'ε' #el símbolo de transición
        )

        # Del segundo al último epsilon
        self.dot.edge( #la creación de una segunda transición en el diagrama
            str(self.estado_actual - 1), #Especifica el nodo de inicio de la transición, que es el estado anterior al que acabamos de crear
            str(self.estado_actual), #specifica el nodo de llegada de la transición
            'ε' #Especifica el símbolo de transición
        )
    #---------------------------------------- lo mismo pero con Kleene

    def KleeneNode(self, node):
        
            # primer epsilon
            self.dot.edge(
                str(self.estado_actual - 1), # Convierte el estado actual en un string y lo usa como inicio del arco
                str(self.estado_actual), # Convierte el estado actual en un string y lo usa como final del arco
                'ε' # Etiqueta del arco, en este caso es un epsilon
            )

            first_node = self.estado_actual - 1 # Guarda el estado actual - 1 en first_node
            self.estado_actual += 1 # Aumenta el estado actual en 1

            # Renderrizacion del node
            self.dot.edge(
                str(self.estado_actual - 1), # Convierte el estado actual en un string y lo usa como inicio del arco
                str(self.estado_actual), # Convierte el estado actual en un string y lo usa como final del arco
                self.Render(node.a) # Etiqueta del arco, renderizada desde el nodo a
            )

            # nodo un último estado a primer épsilon
            self.dot.edge(
                str(self.estado_actual), # Convierte el estado actual en un string y lo usa como inicio del arco
                str(first_node + 1), # Convierte first_node + 1 en un string y lo usa como final del arco
                'ε' # Etiqueta del arco, en este caso es un epsilon
            )

            self.estado_actual += 1 # Aumenta el estado actual en 1

            # Segundo epsilon
            self.dot.edge(
                str(self.estado_actual - 1), # Convierte el estado actual en un string y lo usa como inicio del arco
                str(self.estado_actual), # Convierte el estado actual en un string y lo usa como final del arco
                'ε' # Etiqueta del arco, en este caso es un epsilon
            )

            # primer epsilon al ultimo estado
            self.dot.edge(
                str(first_node), # Convierte first_node en un string y lo usa como inicio del arco
                str(self.estado_actual), # Convierte el estado actual en un string y lo usa como final del arco
                'ε' # Etiqueta del arco, en este caso es un epsilon
            )
    def SumaNode(self, node):
        # Llama al método KleeneNode con el nodo actual
        self.KleeneNode(node)
        self.estado_actual += 1 # Incrementa el estado actual en 1
        # Conecta el último estado del nodo Kleene con el nuevo estado actual
        # usando la transición que representa el carácter 'a'
        self.dot.edge(
            str(self.estado_actual - 1),  # Desde el último estado del nodo Kleene
            str(self.estado_actual),      # Al nuevo estado actual
            self.Render(node.a)       # Usando la transición que representa el carácter 'a'
        )

    def QuestionNode(self, node):
        initial_node = self.estado_actual - 1  # Obtener el estado actual y restar uno para obtener el estado anterior
        mid_node = None

        # de inicial a primer épsilon
        self.dot.edge(
            str(initial_node),  # Estado inicial
            str(self.estado_actual),  # Nuevo estado
            'ε'  # Etiqueta de transición epsilon
        )
        self.estado_actual += 1  # Aumentar el estado actual

        # de epsilon a primera
        self.dot.edge(
            str(self.estado_actual - 1),  # Estado anterior
            str(self.estado_actual),  # Nuevo estado
            self.Render(node.a)  # Renderización del nodo 'a'
        )

        mid_node = self.estado_actual  # Almacenar el estado actual en la variable 'mid_node'
        self.estado_actual += 1  # Aumentar el estado actual

        # de inicial a segunda épsilone
        self.dot.edge(
            str(initial_node),  # Estado inicial
            str(self.estado_actual),  # Nuevo estado
            'ε'  # Etiqueta de transición epsilon
        )

        self.estado_actual += 1  # Aumentar el estado actual

        # de epsilon a segundo
        self.dot.edge(
            str(self.estado_actual - 1),  # Estado anterior
            str(self.estado_actual),  # Nuevo estado
            'ε'  # Etiqueta de transición epsilon
        )

        self.estado_actual += 1  # Aumentar el estado actual

        # del primero al último épsilon
        self.dot.edge(
            str(mid_node),  # Estado medio
            str(self.estado_actual),  # Nuevo estado
            'ε'  # Etiqueta de transición epsilon
        )

        # Del segundo al último epsilon
        self.dot.edge(
            str(self.estado_actual - 1),  # Estado anterior
            str(self.estado_actual),  # Nuevo estado
            'ε'  # Etiqueta de transición epsilon
        )

    #Funcion que genera la tabla de transicion 
    def Tabla_trans_generada(self):
        states = [i.replace('\t', '')
                        for i in self.dot.source.split('\n') if '->' in i and '=' in i]

        self.trans_func = dict.fromkeys(
            [str(s) for s in range(self.estado_actual + 1)])

        self.trans_func[str(self.estado_actual)] = dict()

        for state in states:
            splitted = state.split(' ')
            init = splitted[0]
            final = splitted[2]

            symbol_index = splitted[3].index('=')
            symbol = splitted[3][symbol_index + 1]

            try:
                self.trans_func[init][symbol].append(final)
            except:
                self.trans_func[init] = {symbol: [final]}

        return self.trans_func
    def EvalRegex(self):
        try:
            # Llama al metodo EvalNext con los siguientes argumentos
            # - el primer caracter de la regex
            # - el estado inicial ('0')
            # - la regex completa
            self.EvalNext(self.regex[0], '0', self.regex)
            
            # Si la regex es aceptada, retorna 'Yes', de lo contrario 'No'
            return 'Yes' if self.regexAccepted else 'No'
        
        # En caso de que se genere un error de recursion, se maneja el error
        except RecursionError:
            
            # Si el primer caracter de la regex es un simbolo, pero no es 'ε', se retorna 'Yes', de lo contrario 'No'
            if self.regex[0] in self.symbols and self.regex[0] != 'ε':
                return 'Yes'
            else:
                return 'No'

    #La funcion evalua el sigueinte simbolo de la ezpresion regular y busca el siguiente estado 
    def EvalNext(self, eval_symbol, estado_actual, eval_regex):
        
        # Si ya se ha aceptado la regex, se sale de la función
        if self.regexAccepted != None:
            return

        # Se obtienen las transiciones del estado actual
        transitions = self.trans_func[estado_actual]
        for trans_symbol in transitions:

            # Si la transición es por epsilon
            if trans_symbol == 'ε': 
                # Si no queda regex por evaluar y el estado actual es un estado de aceptación, se acepta la regex
                if not eval_regex and str(self.estadosAceptados) in transitions['ε']: 
                    self.regexAccepted = True
                    return

                # Para cada estado al que se llegue por epsilon, se llama recursivamente la función EvalNext con el mismo símbolo a evaluar
                for state in transitions['ε']:
                    if self.regexAccepted != None:
                        break
                    self.EvalNext(eval_symbol, state, eval_regex)

            # Si la transición es por el símbolo que se debe evaluar en este paso
            elif trans_symbol == eval_symbol:
                # Se obtiene la siguiente parte de la regex
                next_regex = eval_regex[1:] if eval_regex else None
                # Se obtiene el siguiente símbolo a evaluar
                next_symbol = next_regex[0] if next_regex else None

                # Si no queda ningún símbolo por evaluar, se verifica si se llegó a un estado de aceptación
                if not next_symbol:
                    if str(self.estadosAceptados) in transitions[trans_symbol]:
                        self.regexAccepted = True
                        return

                    # Si el estado actual no es un estado de aceptación, se llama recursivamente la función EvalNext con el símbolo epsilon para evaluar las transiciones por epsilon
                    elif str(self.estadosAceptados) != estado_actual:
                        for state in transitions[trans_symbol]:
                            self.EvalNext('e', state, None)
                        if self.regexAccepted != None:
                            return

                # Si aún queda parte de la regex por evaluar
                if self.regexAccepted != None:
                    return

                # Para cada estado al que se llega con la transición por el símbolo a evaluar, se llama recursivamente la función EvalNext con el siguiente símbolo de la regex a evaluar
                for state in transitions[trans_symbol]:
                    if not next_symbol and str(state) == self.estadosAceptados:
                        self.regexAccepted = True
                        return

                    self.EvalNext(next_symbol, state, next_regex)


    # Define un método llamado GetEstadoAceptacion en una clase.
    def GetEstadoAceptacion(self):
        # Crea un nodo en el diagrama DOT con forma de "doble círculo" y lo etiqueta con el número de estado actual.
        self.dot.node(str(self.estado_actual), shape='doublecircle')
        # Agrega el estado actual a la lista de estados de aceptación.
        self.estadosAceptados.append(self.estado_actual)
        # Devuelve el estado actual.
        return self.estado_actual

    #Funcion para escribir el diagrama NFAD
    def WriteNFADiagram(self):
        source = self.dot.source
        debug_string = f'''
        NFA:
        - Símbolos: {self.symbols}
        - Estado final: {self.estadosAceptados}
        - Tabla de transición:
                '''

        WriteToFile('./output/NFA.gv', source)
        self.dot.render('./output/NFA.gv', view=True)

    #Funcion que genera el diagrama 
    def GenerateDiagram(self):
        self.WriteNFADiagram()
        print("Generando diagrama...")
        output_file = os.path.join(os.getcwd(), "output", "NFA.gv")
        s = Source.from_file(output_file)
        s.render()
        s.view()
        print("Diagrama generado con éxito!")


#Creacion de archivos/actualiza archivos
def WriteToFile(filename: str, content: str):
    with open(filename, 'w', encoding='utf-8') as _file: #se agrego utf-8 para que lea correctamente el caracter de epsilon
        _file.write(content)

    return f'Archivo "{filename}" creado exitosamente'