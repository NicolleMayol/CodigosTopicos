
class Restriccion():
    '''Una restricción consiste de:
    - alcance: tupla o lista de variables
    - condición: una función que puede ser aplicada a una tupla de valores para las variables.
    Debe ser una función Booleana'''

    def __init__(self, alcance, condicion):
        self.alcance = alcance
        self.condicion = condicion

    def __repr__(self):
        return self.condicion.__name__ #+ str(self.condicion)

    def holds(self, asignacion):
        '''retorna el valor de la restricción evaluada en la asignación'''
        return self.condicion(*tuple(asignacion[v] for v in self.alcance))

from operator import lt, ne, eq, gt

'''Para el siguiente ejemplo, la función noes, dado un número retorna una función que
es verdadero cuando su argumento no es ese número. f = noes(3). f(2) es verdadero y f(3) es falso'''

def noes(valor):
    '''no es igual a....'''
    noes_valor = lambda x: x != valor
    noes_valor.__name__ = str(valor) + "!="
    return noes_valor

def es(valor):
    '''es igual a...'''
    es_valor = lambda x: x == valor
    es_valor.__name__ = str(valor) + "=="
    return es_valor

class CSP:
    '''Un CSP requiere:
    - dominios : un diccionario que mapea las variables al conjunto de posibles valores.
    dominio[var] es el dominio de la variable var.
     - restricciones: conjunto o lista de objetos de clase Restricción'''

    def __init__(self, dominios, restricciones):
        self.variables = set(dominios)
        self.dominios = dominios
        self.restricciones = restricciones
        self.variables_a_restricciones = {var:set() for var in self.variables}
        for con in restricciones:
            for var in con.alcance:
                self.variables_a_restricciones[var].add(con)

    def __str__(self):
        '''representación del CSP'''
        return str(self.dominios)


    def __repr__(self):
        '''representación más detallada del CSP'''
        return "CSP( " + str(self.dominios) + " , " + str([str(c) for c in self.restricciones]) + " )"

    def consistencia(self, asignacion):
        '''asignación es variable: valor diccionario
        retorna Verdadero si todas las restricciones que pueden ser evaluadas, son evaluadas
        verdaderas dada una asignación'''
        return all(con.holds(asignacion) for con in self.restricciones if all(v in asignacion for v in con.alcance))

'''Tenemos un CSP con variables X, Y, Z, cada una con dominio {1,2,3}. Las restricciones son X<Y, Y>Z'''

csp0 = CSP({'X':{1,2,3}, 'Y':{1,2,3}, 'Z':{1,2,3}},
           [Restriccion(('X', 'Y'), lt),
            Restriccion(('Y', 'Z'), gt)])

'''Tenemos un CSP con variables A,B,C, cada una con dominio {1,2,3,4}. Las restricciones son:
A<B, B !=2, B<C'''

csp1 = CSP({'A': {1,2,3,4}, 'B': {1,2,3,4}, 'C':{1,2,3,4}},
           [Restriccion(('A', 'B'), lt),
            Restriccion(('B', ), noes(2)),
            Restriccion(('B', 'C'), lt)])

csp2 = CSP({'A':{1,2,3,4}, 'B':{1,2,3,4}, 'C':{1,2,3,4},
           'D':{1,2,3,4}, 'E':{1,2,3,4}},
          [Restriccion(('B',), noes(3)),
          Restriccion(('C',), noes(2)),
          Restriccion(('A', 'B'), ne),
          Restriccion(('B', 'C'), ne),
          Restriccion(('C', 'D'), lt),
          Restriccion(('A', 'D'), eq),
          Restriccion(('A', 'E'), gt),
          Restriccion(('B', 'E'), gt),
          Restriccion(('C', 'E'), gt),
          Restriccion(('D', 'E'), gt),
          Restriccion(('B', 'D'), ne)])

'''Tenemos un CSP con 5 variables, de la 'A' a la 'E'. Cada una con dominio {1,2,3,4,5}. Las restricciones son:
A y B deben ser adyacentes, B y C deben ser adyacentes, C y D deben ser adyantes, D y E deben ser adyacentes,
A diferente de C, B diferente de D y C diferente de E.
'''

'''Test unitario para comprobar la solución'''

def test(solucionador_csp, csp, soluciones = [{'A': 1, 'B': 3, 'C': 4}, {'A': 2, 'B': 3, 'C' : 4}]):
    print('Evaluando el csp con ', solucionador_csp.__doc__)
    sol= solucionador_csp(csp)
    print("Se encontró una solución: ", sol)
    assert sol in soluciones,"La solución no es correcta para " +str(csp)
    print('Pasó el test unitario')

from Busqueda import Arco, Problema_busqueda
from utilidades import union_diccionarios

class Busqueda_CSP(Problema_busqueda):
    '''Un nodo es variable: valor diccionario'''

    def __init__(self, csp, orden_variable = None):
        self.csp = csp
        if orden_variable:
            assert set(orden_variable) == set(csp.variables)
            assert len(orden_variable) == len(csp.variables)
            self.variables = orden_variable
        else:
            self.variables = list(csp.variables)

    def es_meta(self, nodo):
        return len(nodo) == len(self.csp.variables)

    def nodo_inicio(self):
        return {}

    def vecinos(self, nodo):
        ''''este método usa el hecho de que la longitud del nodo, que es el número de variables
        asignadas, es el índice de la siguiente variable para hacer la división del grafo.
        Note que no se necesita revisar si hay más variables para hacer la división,
        dado que todos los nodos son consistentes por construcción y que no se tienen
        más variables  si hay una solución'''

        var = self.variables[len(nodo)] # la siguiente variable
        res = []
        for val in self.csp.dominios[var]:
            nuevo = union_diccionarios(nodo, {var:val})
            if self.csp.consistencia(nuevo):
                res.append(Arco(nodo, nuevo))
        return res


from Busqueda import Buscador

print(Buscador(Busqueda_CSP(csp0)).buscar_profundidad())