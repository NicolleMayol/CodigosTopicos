class Problema_busqueda():
    '''-nodo inicio
    - función de vecinos
    - meta (función booleana)
    - heurística'''

    def nodo_inicio(self):
        'retorna el nodo inicio'
        raise NotImplementedError('nodo_inicio')

    def es_meta(self, nodo):
        'retorna Verdadero si nodo es meta'
        raise NotImplementedError('es_meta')

    def heuristica(self, n):
        'retorna la heurística para el nodo n'
        return 0

    def vecinos(self, nodo):
        'retorna la lista de los arcos de los vecinos del nodo'
        raise NotImplementedError('vecinos')


class Arco():
    '''- nodo saliente
    - nodo entrante
    - costo (no negativo)'''

    def __init__(self, nodo_saliente, nodo_entrante, costo=1, accion=None):
        assert costo >= 0, ('El costo no puede ser negativo para'
                            + str(nodo_saliente) + ' -> ' + str(nodo_entrante))
        self.nodo_saliente = nodo_saliente
        self.nodo_entrante = nodo_entrante
        self.accion = accion
        self.costo = costo

    def __repr__(self):
        if self.accion:
            return str(self.nodo_saliente) + ' --' + str(self.accion) + ',' + str(self.costo) + '-> ' + str(
                self.nodo_entrante)
        else:
            return str(self.nodo_saliente) + ' --' + str(self.costo) + '-> ' + str(self.nodo_entrante)


class Busqueda_grafo(Problema_busqueda):
    '''- lista o conjunto de nodos
    - lista o conjunto de arcos
    - nodo inicio
    - lista o conjunto nodos meta
    - un diccionario que mapee cada nodo en un valor heurístico'''

    def __init__(self, nodos, arcos, inicio=None, metas=set(), hmap={}):
        self.veci = {}
        self.nodos = nodos
        for nodo in nodos:
            self.veci[nodo] = []
        self.arcos = arcos
        for arc in arcos:
            self.veci[arc.nodo_saliente].append(arc)
        self.inicio = inicio
        self.metas = metas
        self.hmap = hmap

    def nodo_inicio(self):
        '''retorna el nodo inicio'''
        return self.inicio

    def es_meta(self, nodo):
        '''retorna Verdadero si nodo es una meta'''
        return nodo in self.metas

    def heuristica(self, nodo):
        '''retorna un valor para la heurística de nodo'''
        if nodo in self.hmap:
            return self.hmap[nodo]
        else:
            return 0

    def vecinos(self, nodo):
        '''retorna los vecinos de nodo'''
        return self.veci[nodo]

    def __repr__(self):
        salida = ""
        costo_total = 0
        for arc in self.arcos:
            salida += str(arc) + " . "
        return salida


# -----------------------------------------------------------------

def nodos_vecinos(self, nodo):
    '''retorna un iterador sobre los vecinos de nodo'''
    return (camino.nodo_entrante for camino in self.veci[nodo])  # el nodo entrante es vecino del nodo saliente


class Camino():

    def __init__(self, inicial, arco=None):
        '''inicial puede ser un nodo o un camino'''
        self.inicial = inicial
        self.arco = arco
        if arco is None:
            self.costo = 0
        else:
            self.costo = inicial.costo + arco.costo

    def fin(self):
        '''retorna el nodo final del camino'''
        if self.arco is None:
            return self.inicial
        else:
            return self.arco.nodo_entrante  # retorna el nodo entrante del último arco

    def nodos(self):
        '''retorna los nodos del caimno de atrás hacia adelante'''
        actual = self
        while actual.arco is not None:
            yield actual.arco.nodo_entrante
            actual = actual.inicial
        yield actual.inicial

    def nodos_iniciales(self):
        '''retorna todos los nodos antes del nodo final'''
        if self.arco is not None:
            for nd in self.inicial.nodos(): yield nd

    def __repr__(self):
        if self.arco is None:
            return str(self.inicial)
        elif self.arco.accion:
            return (str(self.inicial) + "\n --" + str(self.arco.accion) + " --> " + str(self.arco.nodo_entrante))
        else:
            return (str(self.inicial) + "\n ----> " + str(self.arco.nodo_entrante))


class Visualizable():
    '''controla la cantidad de detalles por el nivel max_nivel_visual'''
    max_nivel_visual = 1

    def visualizar(self, nivel, *args, **nargs):
        if nivel <= self.max_nivel_visual:
            print(*args, **nargs)


class Buscador(Visualizable):
    '''retorna un buscador para un problema.
    Los caminos se pueden encontrar llamando repetidamente "buscar()"'''

    def __init__(self, problema):
        '''crea un buscador para el problema'''
        self.problema = problema
        self.inicializar_frontera()
        self.num_expansion = 0
        self.agregar_a_frontera(Camino(problema.nodo_inicio()))
        super().__init__()  # llama los atributos de la clase padre sin tener que conocer el nombre de la misma

    def inicializar_frontera(self):
        self.frontera = []

    def frontera_vacia(self):
        return self.frontera == []

    def agregar_a_frontera(self, camino):
        self.frontera.append(camino)

    # @visualizacion #decorador para modificar o replantear una función ya existente
    def buscar_profundidad(self):
        '''retorna el (siguiente) camino para el nodo inicio del problema
        al nodo meta. Retorna None si no existe el camino'''
        while not self.frontera_vacia():
            camino = self.frontera.pop()
            self.visualizar(3, "Expandiendo :", camino, "(costo: ", camino.costo, ")")
            self.num_expansion += 1
            if self.problema.es_meta(camino.fin()):  # se encontró la solución
                self.visualizar(3, self.num_expansion,
                                "caminos se han expandido y quedan ",
                                len(self.frontera), "caminos en la frontera")
                return camino
            else:
                vecis = self.problema.vecinos(camino.fin())
                self.visualizar(3, "Los vecinos son", vecis)
                for arco in reversed(list(vecis)):
                    self.agregar_a_frontera(Camino(camino, arco))
                self.visualizar(3, "Frontera", self.frontera)
            self.visualizar(3, "No hay más soluciones. Se expandieron un total de ",
                            self.num_expansion, "caminos")

    def buscar_anchura(self):
        '''retorna el (siguiente) camino para el nodo inicio del problema
        al nodo meta. Retorna None si no existe el camino'''
        while not self.frontera_vacia():
            camino = self.frontera.pop(0)
            self.visualizar(3, "Expandiendo :", camino, "(costo: ", camino.costo, ")")
            self.num_expansion += 1
            if self.problema.es_meta(camino.fin()):  # se encontró la solución
                self.visualizar(3, self.num_expansion,
                                "caminos se han expandido y quedan ",
                                len(self.frontera), "caminos en la frontera")
                return camino
            else:
                vecis = self.problema.vecinos(camino.fin())
                self.visualizar(3, "Los vecinos son", vecis)
                for arco in list(vecis):
                    self.agregar_a_frontera(Camino(camino, arco))
                self.visualizar(3, "Frontera", self.frontera)
            self.visualizar(3, "No hay más soluciones. Se expandieron un total de ",
                            self.num_expansion, "caminos")


# frontera como una cola prioritaria
import heapq


class FronteraCP():
    '''Una frontera consiste de una cola prioritaria (heap), de
      tripletas (valor, index, camino), donde valor es el valor
      que se desea minimizar, index es el índice único para cada elemento
      y camino es el camino de la cola. Note que la cola prioritaria
      siempre retorna el elemento más pequeño'''

    def __init__(self):
        '''constructor de la frontera, inicialmente una cola
        prioritaria vacía'''
        self.frontera_index = 0  # número de items que se agregan a la frontera
        self.fronteracp = []  # la frontera como cola prioritaria

    def vacia(self):
        '''es Verdadero si la cola prioritaria está vacía'''
        return self.fronteracp == []

    def agregar(self, camino, valor):
        '''agrega un camino a la cola prioritaria'''
        self.frontera_index += 1
        heapq.heappush(self.fronteracp, (valor, self.frontera_index, camino))

    def pop(self):
        '''retorna y remueve el camino de la frontera con el mínimo valor'''
        (_, _, camino) = heapq.heappop(self.fronteracp)
        return camino

    def conteo(self, val):
        '''retorna el número de elementos de la frontera con valor=val'''
        return sum(1 for i in self.fronteracp if i[0] == val)

    def __repr__(self):
        '''Representación string de la frontera'''
        return str([n, c, str(p)] for (n, c, p) in self.fronteracp)

    def __len__(self):
        '''longitud de la frontera'''
        return len(self.fronteracp)

    def __iter__(self):
        '''itera a través de los caminos en la frontera'''
        for (_, _, camino) in self.fronteracp:
            yield camino


# Algoritmo A*

class AEstrella(Buscador):
    '''Retorna un buscador para un problema. Se pueden encontrar los caminos
    llamando a buscador_profundidad'''

    def __init__(self, problema):
        super().__init__(problema)

    def inicializar_frontera(self):
        self.frontera = FronteraCP()

    def frontera_vacia(self):
        return self.frontera.vacia()

    def agregar_a_frontera(self, camino):
        '''agrega a la frontera un camino con su respectivo costo'''
        valor = camino.costo + self.problema.heuristica(camino.fin())
        self.frontera.agregar(camino, valor)


problema_entregas_aciclico = Busqueda_grafo(
    {'mail', 'ts', 'o103', 'b3', 'b1', 'c2', 'c1', 'c3', 'b2', 'b4', 'o109',
     'o111', 'o119', 'storage', 'o123', 'r123', 'o125'},
    [Arco('ts', 'mail', 6), Arco('o103', 'ts', 8), Arco('o103', 'b3', 4),
     Arco('b3', 'b1', 4), Arco('b1', 'c2', 3), Arco('c2', 'c1', 4),
     Arco('c1', 'c3', 8), Arco('c2', 'c3', 6), Arco('b1', 'b2', 6),
     Arco('b2', 'b4', 3), Arco('b3', 'b4', 7), Arco('b4', 'o109', 7),
     Arco('o103', 'o109', 12), Arco('o109', 'o111', 4), Arco('o109', 'o119', 16),
     Arco('o119', 'storage', 7), Arco('o119', 'o123', 9), Arco('o123', 'r123', 4),
     Arco('o123', 'o125', 4)], inicio='o103', metas={'r123'}, hmap={
        'mail': 26, 'ts': 23, 'o103': 21, 'o109': 24, 'o111': 27, 'o119': 11,
        'o123': 4, 'o125': 6, 'r123': 0, 'b1': 13, 'b2': 15, 'b3': 17,
        'b4': 18, 'c1': 6, 'c2': 10, 'c3': 12, 'storage': 12
    })

#print(problema_entregas_aciclico)
#print(AEstrella(problema_entregas_aciclico).buscar_profundidad())