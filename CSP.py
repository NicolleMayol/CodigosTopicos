class Restriccion():
    '''Una restricción consiste de:
    - alcance: tupla o lista de variables
    - condición: una función que puede ser aplicada a una tupla de valores para las variables.
    Debe ser una función Booleana'''

    def __init__(self, alcance, condicion):
        self.alcance = alcance
        self.condicion = condicion

    def __repr__(self):
        return self.condicion.__name__  # + str(self.condicion)

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
        self.variables_a_restricciones = {var: set() for var in self.variables}
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

csp0 = CSP({'X': {1, 2, 3}, 'Y': {1, 2, 3}, 'Z': {1, 2, 3}},
           [Restriccion(('X', 'Y'), lt),
            Restriccion(('Y', 'Z'), gt)])

'''Tenemos un CSP con variables A,B,C, cada una con dominio {1,2,3,4}. Las restricciones son:
A<B, B !=2, B<C'''

csp1 = CSP({'A': {1, 2, 3, 4}, 'B': {1, 2, 3, 4}, 'C': {1, 2, 3, 4}},
           [Restriccion(('A', 'B'), lt),
            Restriccion(('B',), noes(2)),
            Restriccion(('B', 'C'), lt)])

csp2 = CSP({'A': {1, 2, 3, 4}, 'B': {1, 2, 3, 4}, 'C': {1, 2, 3, 4},
            'D': {1, 2, 3, 4}, 'E': {1, 2, 3, 4}},
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


def test(solucionador_csp, csp, soluciones=[{'A': 1, 'B': 3, 'C': 4}, {'A': 2, 'B': 3, 'C': 4}]):
    print('Evaluando el csp con ', solucionador_csp.__doc__)
    sol = solucionador_csp(csp)
    print("Se encontró una solución: ", sol)
    assert sol in soluciones, "La solución no es correcta para " + str(csp)
    print('Pasó el test unitario')


from Busqueda import Arco, Problema_busqueda
from utilidades import union_diccionarios


class Busqueda_CSP(Problema_busqueda):
    '''Un nodo es variable: valor diccionario'''

    def __init__(self, csp, orden_variable=None):
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

        var = self.variables[len(nodo)]  # la siguiente variable
        res = []
        for val in self.csp.dominios[var]:
            nuevo = union_diccionarios(nodo, {var: val})
            if self.csp.consistencia(nuevo):
                res.append(Arco(nodo, nuevo))
        return res


from Busqueda import Buscador

# print(Buscador(Busqueda_CSP(csp0)).buscar_profundidad())

csp_actividad = CSP({

               'Diseño de Software':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Formulacion de Proyectos':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Pensamiento Cientifico':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Competencias Ciudadanas':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Lectura Critico':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Ingles':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Comunicacion Escrita':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'} ,
               'Competencias Ciudadanas 2':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Formulacion de Proyectos':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m','Domingo 10 a.m','Domingo 02 p.m','Domingo 04 p.m'},
               'Razonamiento Cuantitativo':{'Sabado 8 a.m','Sabado 10 a.m','Sabado 02 p.m' ,'Sabado 04 p.m','Domingo 8 a.m' ,'Domingo 10 a.m','Domingo 02 p.m' ,'Domingo 04 p.m'}},
               [Restriccion(('Diseño de Software',), noes('Domingo 8 a.m')),
                Restriccion(('Diseño de Software',), noes('Domingo 10 a.m')),
                Restriccion(('Diseño de Software',), noes('Domingo 02 p.m')),
                Restriccion(('Diseño de Software',), noes('Domingo 04 p.m')),
                Restriccion(('Diseño de Software','Comunicacion Escrita'), ne),
                Restriccion(('Diseño de Software','Ingles'), ne),
                Restriccion(('Diseño de Software','Competencias Ciudadanas 2'), ne),
                Restriccion(('Diseño de Software','Formulacion de Proyectos'), ne),
                Restriccion(('Diseño de Software','Razonamiento Cuantitativo'), ne),
                Restriccion(('Diseño de Software','Lectura Critico'), ne),
                Restriccion(('Diseño de Software','Competencias Ciudadanas'), ne),
                Restriccion(('Formulacion de Proyectos',), noes('Sabado 02 p.m')),
                Restriccion(('Formulacion de Proyectos',), noes('Sabado 04 p.m')),
                Restriccion(('Formulacion de Proyectos',), noes('Domingo 02 p.m')),
                Restriccion(('Formulacion de Proyectos',), noes('Domingo 04 p.m')),
                Restriccion(('Competencias Ciudadanas',), noes('Sabado 8 a.m')),
                Restriccion(('Competencias Ciudadanas',), noes('Sabado 10 a.m')),
                Restriccion(('Competencias Ciudadanas',), noes('Domingo 8 a.m')),
                Restriccion(('Competencias Ciudadanas',), noes('Domingo 10 a.m')),
                Restriccion(('Competencias Ciudadanas','Diseño de Software'), ne),
                Restriccion(('Competencias Ciudadanas','Comunicacion Escrita'), ne),
                Restriccion(('Competencias Ciudadanas','Ingles'), ne),
                Restriccion(('Competencias Ciudadanas','Competencias Ciudadanas 2'), ne),
                Restriccion(('Competencias Ciudadanas','Formulacion de Proyectos'), ne),
                Restriccion(('Competencias Ciudadanas','Razonamiento Cuantitativo'), ne),
                Restriccion(('Competencias Ciudadanas','Lectura Critico'), ne),
                Restriccion(('Lectura Critico',), noes('Sabado 8 a.m')),
                Restriccion(('Lectura Critico',), noes('Domingo 8 a.m')),
                Restriccion(('Lectura Critico',), noes('Sabado 04 p.m')),
                Restriccion(('Lectura Critico',), noes('Domingo 04 p.m')),
                Restriccion(('Lectura Critico','Diseño de Software'), ne),
                Restriccion(('Lectura Critico','Comunicacion Escrita'), ne),
                Restriccion(('Lectura Critico','Ingles'), ne),
                Restriccion(('Lectura Critico','Competencias Ciudadanas 2'), ne),
                Restriccion(('Lectura Critico','Formulacion de Proyectos'), ne),
                Restriccion(('Lectura Critico','Razonamiento Cuantitativo'), ne),
                Restriccion(('Lectura Critico','Competencias Ciudadanas'), ne),
                Restriccion(('Ingles',), noes('Sabado 02 p.m')),
                Restriccion(('Ingles',), noes('Sabado 04 p.m')),
                Restriccion(('Ingles',), noes('Domingo 02 p.m')),
                Restriccion(('Ingles',), noes('Domingo 04 p.m')),
                Restriccion(('Ingles','Diseño de Software'), ne),
                Restriccion(('Ingles','Comunicacion Escrita'), ne),
                Restriccion(('Ingles','Competencias Ciudadanas 2'), ne),
                Restriccion(('Ingles','Formulacion de Proyectos'), ne),
                Restriccion(('Ingles','Razonamiento Cuantitativo'), ne),
                Restriccion(('Ingles','Lectura Critico'), ne),
                Restriccion(('Ingles','Competencias Ciudadanas'), ne),
                Restriccion(('Comunicacion Escrita',), noes('Domingo 8 a.m')),
                Restriccion(('Comunicacion Escrita',), noes('Domingo 10 a.m')),
                Restriccion(('Comunicacion Escrita',), noes('Domingo 02 p.m')),
                Restriccion(('Comunicacion Escrita',), noes('Domingo 04 p.m')),
                Restriccion(('Comunicacion Escrita','Diseño de Software'), ne),
                Restriccion(('Comunicacion Escrita','Ingles'), ne),
                Restriccion(('Comunicacion Escrita','Competencias Ciudadanas 2'), ne),
                Restriccion(('Comunicacion Escrita','Formulacion de Proyectos'), ne),
                Restriccion(('Comunicacion Escrita','Razonamiento Cuantitativo'), ne),
                Restriccion(('Comunicacion Escrita','Lectura Critico'), ne),
                Restriccion(('Comunicacion Escrita','Competencias Ciudadanas'), ne),
                Restriccion(('Competencias Ciudadanas 2','Diseño de Software'), ne),
                Restriccion(('Competencias Ciudadanas 2','Comunicacion Escrita'), ne),
                Restriccion(('Competencias Ciudadanas 2','Ingles'), ne),
                Restriccion(('Competencias Ciudadanas 2','Formulacion de Proyectos'), ne),
                Restriccion(('Competencias Ciudadanas 2','Razonamiento Cuantitativo'), ne),
                Restriccion(('Competencias Ciudadanas 2','Lectura Critico'), ne),
                Restriccion(('Competencias Ciudadanas 2','Competencias Ciudadanas'), ne),
                Restriccion(('Formulacion de Proyectos','Diseño de Software'), ne),
                Restriccion(('Formulacion de Proyectos','Comunicacion Escrita'), ne),
                Restriccion(('Formulacion de Proyectos','Ingles'), ne),
                Restriccion(('Formulacion de Proyectos','Competencias Ciudadanas 2'), ne),
                Restriccion(('Formulacion de Proyectos','Razonamiento Cuantitativo'), ne),
                Restriccion(('Formulacion de Proyectos','Lectura Critico'), ne),
                Restriccion(('Formulacion de Proyectos','Competencias Ciudadanas'), ne),
                Restriccion(('Razonamiento Cuantitativo','Diseño de Software'), ne),
                Restriccion(('Razonamiento Cuantitativo','Comunicacion Escrita'), ne),
                Restriccion(('Razonamiento Cuantitativo','Ingles'), ne),
                Restriccion(('Razonamiento Cuantitativo','Competencias Ciudadanas 2'), ne),
                Restriccion(('Razonamiento Cuantitativo','Formulacion de Proyectos'), ne),
                Restriccion(('Razonamiento Cuantitativo','Lectura Critico'), ne),
                Restriccion(('Razonamiento Cuantitativo','Competencias Ciudadanas'), ne),
                Restriccion(('Razonamiento Cuantitativo',), noes('Sabado 02 p.m')),
                Restriccion(('Razonamiento Cuantitativo',), noes('Sabado 04 p.m')),
                Restriccion(('Razonamiento Cuantitativo',), noes('Domingo 02 p.m')),
                Restriccion(('Razonamiento Cuantitativo',), noes('Domingo 04 p.m'))])

print(Buscador(Busqueda_CSP(csp_actividad)).buscar_profundidad())
