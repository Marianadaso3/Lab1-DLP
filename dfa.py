from pprint import pprint
from pythomata import SimpleDFA
from graphviz import Digraph
from nfa import WriteToFile

#Definimos los estados
STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class DFA:
    def __init__(self, trans_table, symbols, states, final_nfa_state, regex):

        # Proveniente del NFA
        self.trans_table = trans_table
        self.final_nfa_state = final_nfa_state

        # Propiedades de un AF
        self.symbols = symbols
        self.trans_func = dict()
        self.states = dict()
        self.accepting_states = list()
        self.initial_state = 'A'

        try:
            self.symbols.remove('e')
        except:
            pass

        self.nodes = []
        self.iterations = 0
        self.regex = regex

    def MoveTo(self, node_id, eval_symbol='e', array=[], add_initial=False, move_once=False):

        arr = array
        node = self.nodes[node_id]
        # Recorremos el nodo si no está visitado
        if not node.visited and eval_symbol in node.next_states:

            # Marcamos el nodo
            node.Mark()
            # Obtenemos los siguientes estados
            next_states = [int(s) for s in node.next_states[eval_symbol]]
            if eval_symbol == 'e':
                arr = [*next_states]
            else:
                arr = [*next_states]

            # ¿Tenemos que agregar el nodo inicial?
            if add_initial:
                arr = [*next_states, node_id]

            # Si tenemos que movernos varias veces, habrá que hacerlo de forma recursiva
            if not move_once:
                for new_node_id in node.next_states[eval_symbol]:
                    arr += [*self.MoveTo(int(new_node_id), eval_symbol, arr)]

        return list(set(arr))

    def EvaluateClosure(self, closure, node,  curr_state):

        # Estado inicial no creado?
        if not closure:
            closure = self.MoveTo(0, add_initial=True)
            closure.append(0)
            self.states[curr_state] = closure
            if self.final_nfa_state in closure:
                self.accepting_states.append(curr_state)

        # Por cada símbolo dentro del set...
        for symbol in self.symbols:
            symbol_closure = list()
            new_set = list()

            # Clausura con el símbolo y el estado
            for value in closure:
                symbol_closure += self.MoveTo(value, symbol, move_once=True)
                [node.UnMark() for node in self.nodes]

            # Clausura con epsilon y el estado
            if symbol_closure:
                e_closure = list()
                for e_value in symbol_closure:
                    e_closure += self.MoveTo(e_value)
                    [node.UnMark() for node in self.nodes]

                new_set += list(set([*symbol_closure, *e_closure]))

                # Si este nuevo estado no existe es nuevo...
                if not new_set in self.states.values():
                    self.iterations += 1
                    new_state = STATES[self.iterations]

                    # Se crea la entrada en la función de transición
                    try:
                        curr_dict = self.trans_func[curr_state]
                        curr_dict[symbol] = new_state
                    except:
                        self.trans_func[curr_state] = {symbol: new_state}

                    try:
                        self.trans_func[new_state]
                    except:
                        self.trans_func[new_state] = {}

                    # Se agrega dicha entrada
                    self.states[new_state] = new_set

                    # Si posee el estado final del AFN, entonces agregarlo al set
                    if self.final_nfa_state in new_set:
                        self.accepting_states.append(new_state)

                    # Repetir con el nuevo set
                    self.EvaluateClosure(new_set, value, new_state)

                # Este estado ya existe, se agrega la transición.
                else:
                    for S, V in self.states.items():
                        if new_set == V:

                            try:
                                curr_dict = self.trans_func[curr_state]
                            except:
                                self.trans_func[curr_state] = {}
                                curr_dict = self.trans_func[curr_state]

                            curr_dict[symbol] = S
                            self.trans_func[curr_state] = curr_dict
                            break

    def EvalRegex(self):
        curr_state = 'A'

        for symbol in self.regex:
            # El símbolo no está dentro del set
            if not symbol in self.symbols:
                return 'No'
            # Intentamos hacer una transición a un nuevo estado
            try:
                curr_state = self.trans_func[curr_state][symbol]
            except:
                # Volvemos al inicio y verificamos que sea un estado de aceptacion
                if curr_state in self.accepting_states and symbol in self.trans_func['A']:
                    curr_state = self.trans_func['A'][symbol]
                else:
                    return 'No'

        return 'Yes' if curr_state in self.accepting_states else 'No'

    def GetDStates(self):
        for state, values in self.trans_table.items():
            self.nodes.append(Node(int(state), values))

    def TransformNFAToDFA(self):
        self.GetDStates()
        self.EvaluateClosure([], 0, 'A')

    def GraphDFA(self):
        states = set(self.trans_func.keys())
        alphabet = set(self.symbols)
        initial_state = 'A'

        dfa = SimpleDFA(states, alphabet, initial_state,
                        set(self.accepting_states), self.trans_func)

        graph = dfa.trim().to_graphviz()
        graph.attr(rankdir='LR')

        source = graph.source
        WriteToFile('./output/DFA.gv', source)
        graph.render('./output/DFA.gv', format='pdf', view=True)


class Node:
    def __init__(self, state, next_states):
        self.state = state
        self.visited = False
        self.next_states = next_states

    def Mark(self):
        self.visited = True

    def UnMark(self):
        self.visited = False

    def __repr__(self):
        return f'{self.state} - {self.visited}: {self.next_states}'

# DFA de manera directo -----------------------

RAW_STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class DDFA:
    def __init__(self, tree, symbols, regex):

        # Useful for syntax tree
        self.nodes = list()

        # FA properties
        self.symbols = symbols
        self.states = list()
        self.trans_func = dict()
        self.accepting_states = set()
        self.estado_inicial = 'A'

        # Class properties
        self.tree = tree
        self.regex = regex
        self.augmented_state = None
        self.iter = 1

        self.STATES = iter(RAW_STATES)
        try:
            self.symbols.remove('e')
        except:
            pass

        # Initialize dfa construction
        self.ParseTree(self.tree)
        self.CalcFollowPos()

    def CalcFollowPos(self):
        for node in self.nodes:
            if node.value == '*':
                for i in node.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.firstpos
            elif node.value == '.':
                for i in node.c1.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.c2.firstpos

        # Initiate state generation
        estado_inicial = self.nodes[-1].firstpos

        # Filter the nodes that have a symbol
        self.nodes = list(filter(lambda x: x._id, self.nodes))
        self.augmented_state = self.nodes[-1]._id

        # Recursion
        self.CalcNewStates(estado_inicial, next(self.STATES))

    def CalcNewStates(self, state, curr_state):

        if not self.states:
            self.states.append(set(state))
            if self.augmented_state in state:
                self.accepting_states.update(curr_state)

        # Iteramos por cada símbolo
        for symbol in self.symbols:

            # Get all the nodes with the same symbol in followpos
            same_symbols = list(
                filter(lambda x: x.value == symbol and x._id in state, self.nodes))

            # Create a new state with the nodes
            new_state = set()
            for node in same_symbols:
                new_state.update(node.followpos)

            # new state is not in the state list
            if new_state not in self.states and new_state:

                # Get this new state's letter
                self.states.append(new_state)
                next_state = next(self.STATES)

                # Add state to transition function
                try:
                    self.trans_func[next_state]
                except:
                    self.trans_func[next_state] = dict()

                try:
                    existing_states = self.trans_func[curr_state]
                except:
                    self.trans_func[curr_state] = dict()
                    existing_states = self.trans_func[curr_state]

                # Add the reference
                existing_states[symbol] = next_state
                self.trans_func[curr_state] = existing_states

                # Is it an acceptina_state?
                if self.augmented_state in new_state:
                    self.accepting_states.update(next_state)

                # Repeat with this new state
                self.CalcNewStates(new_state, next_state)

            elif new_state:
                # State already exists... which one is it?
                for i in range(0, len(self.states)):

                    if self.states[i] == new_state:
                        state_ref = RAW_STATES[i]
                        break

                # Add the symbol transition
                try:
                    existing_states = self.trans_func[curr_state]
                except:
                    self.trans_func[curr_state] = {}
                    existing_states = self.trans_func[curr_state]

                existing_states[symbol] = state_ref
                self.trans_func[curr_state] = existing_states

    def ParseTree(self, node):
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetraNode(self, node):
        new_node = Node(self.iter, [self.iter], [
                        self.iter], value=node.value, nullable=False)
        self.nodes.append(new_node)
        return new_node

    def OrNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.lastpos + node_b.lastpos

        self.nodes.append(Node(None, firstpos, lastpos,
                               is_nullable, '|', node_a, node_b))
        return Node(None, firstpos, lastpos, is_nullable, '|', node_a, node_b)

    def AppendNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable and node_b.nullable
        if node_a.nullable:
            firstpos = node_a.firstpos + node_b.firstpos
        else:
            firstpos = node_a.firstpos

        if node_b.nullable:
            lastpos = node_b.lastpos + node_a.lastpos
        else:
            lastpos = node_b.lastpos

        self.nodes.append(
            Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b))

        return Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b)

    def KleeneNode(self, node):
        node_a = self.ParseTree(node.a)
        firstpos = node_a.firstpos
        lastpos = node_a.lastpos
        self.nodes.append(Node(None, firstpos, lastpos, True, '*', node_a))
        return Node(None, firstpos, lastpos, True, '*', node_a)

    def SumaNode(self, node):
        node_a = self.ParseTree(node.a)

        self.iter += 1

        node_b = self.KleeneNode(node)

        is_nullable = node_a.nullable and node_b.nullable
        if node_a.nullable:
            firstpos = node_a.firstpos + node_b.firstpos
        else:
            firstpos = node_a.firstpos

        if node_b.nullable:
            lastpos = node_b.lastpos + node_a.lastpos
        else:
            lastpos = node_b.lastpos

        self.nodes.append(
            Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b))

        return Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b)

    def QuestionNode(self, node):
        # Node_a is epsilon
        node_a = Node(None, list(), list(), True)
        self.iter += 1
        node_b = self.ParseTree(node.a)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.lastpos + node_b.lastpos

        self.nodes.append(Node(None, firstpos, lastpos,
                               is_nullable, '|', node_a, node_b))
        return Node(None, firstpos, lastpos, is_nullable, '|', node_a, node_b)

    def EvalRegex(self):
        curr_state = 'A'
        for symbol in self.regex:

            if not symbol in self.symbols:
                return 'No'

            try:
                curr_state = self.trans_func[curr_state][symbol]
            except:
                if curr_state in self.accepting_states and symbol in self.trans_func['A']:
                    curr_state = self.trans_func['A'][symbol]
                else:
                    return 'No'

        return 'Yes' if curr_state in self.accepting_states else 'No'

    def GraphDFA(self):
        states = set(self.trans_func.keys())
        alphabet = set(self.symbols)

        dfa = SimpleDFA(states, alphabet, self.estado_inicial,
                        self.accepting_states, self.trans_func)

        graph = dfa.trim().to_graphviz()
        graph.attr(rankdir='LR')

        source = graph.source
        WriteToFile('./output/DirectDFA.gv', source)
        graph.render('./output/DirectDFA.gv', format='pdf', view=True)


class Node:
    def __init__(self, _id, firstpos=None, lastpos=None, nullable=False, value=None, c1=None, c2=None):
        self._id = _id
        self.firstpos = firstpos
        self.lastpos = lastpos
        self.followpos = list()
        self.nullable = nullable
        self.value = value
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return f'''
    id: {self._id}
    value: {self.value}
    firstpos: {self.firstpos}
    lastpos: {self.lastpos}
    followpos: {self.followpos}
    nullabe: {self.nullable}
    '''