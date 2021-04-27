
class Restriccion():
    '''Una restricción consiste de:
    - alcance: tupla o lista de variables
    - condición: una función que puede ser aplicada a una tupla de valores para las variables.
    Debe ser una función Booleana'''

    def __init__(self, alcance, condicion):
        self.alcance = alcance
        self.condicion = condicion

    def __repr__(self):
        return str(self.alcance) + self.condicion.__name__

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


from Busqueda import Visualizable


class Solucionador_consistencia(Visualizable):
    '''Soluciona un CSP con consistencia de arco y división de dominio'''

    def __init__(self, csp, **kwargs):
        self.csp = csp
        super().__init__(**kwargs)

    def hacer_arcos_consistentes(self, dominios_originales = None, para_revisar = None):
        '''Hace que el CSP sea de arcos consistentes. dominios_originales son los dominios originales del CSP
        para_revisar es un conjunto de pares (variable, restriccion)'''

        if dominios_originales is None:
            dominios_originales = self.csp.dominios
        if para_revisar is None:
            para_revisar = {(variable, restriccion) for restriccion in self.csp.restricciones for variable in restriccion.alcance}
        else:
            para_revisar = para_revisar.copy()
        dominios = dominios_originales.copy()
        self.visualizar(1, 'Realizando AC con dominios: ', dominios)
        while para_revisar:
            variable, restriccion = self.seleccionar_arco(para_revisar)
            self.visualizar(1, 'Procesando arco ( ', variable, ',', restriccion, ')')
            otras_variables = [otras for otras in restriccion.alcance if otras != variable]
            nuevo_dominio = {valor for valor in dominios[variable] if self.se_mantiene(dominios, restriccion, {variable: valor},
                                                                                       otras_variables)}
            if nuevo_dominio != dominios[variable]:
                self.visualizar(1, 'El arco : (', variable, ',', restriccion, ') es inconsistente')
                self.visualizar(1, 'Hay poda de dominio ', 'dominio(', variable, ')=',nuevo_dominio, ' debido a ', restriccion)
                dominios[variable] = nuevo_dominio
                agregar_para_revisar = self.nuevo_para_revisar(variable, restriccion) - para_revisar
                para_revisar |= agregar_para_revisar #unión de conjuntos
                self.visualizar(1, ' agregando ', agregar_para_revisar if agregar_para_revisar else "nada", ' para revisar')
            self.visualizar(1, "El arco (", variable, ',', restriccion, ") ahora es consistente")
        self.visualizar(1, 'Consistencia de arcos terminada. Dominios reducidos ', dominios)
        return dominios

    def nuevo_para_revisar(self, variable, restriccion):
        '''retorna nuevos elementos para agregar a para_revisar después de asignar variable en restriccion'''
        return{(nvariable, nrestriccion) for nrestriccion in self.csp.variables_a_restricciones[variable]
               if nrestriccion != restriccion
               for nvariable in nrestriccion.alcance
               if nvariable != variable}

    def seleccionar_arco(self, para_revisar):
        '''selecciona el arco del conjunto para_revisar, donde un arco es un par (variable, restriccion).
        El arco seleccionado debe ser removido del conjunto para_revisar'''
        return para_revisar.pop()

    def se_mantiene(self, dominios, restriccion, asignacion, otras_variables, ind=0):
        '''retorna Verdadero si restriccion se mantiene para una asignacion que se extiene con las variables en otras_variables[ind:]
        asignacion es un diccionario.'''
        if ind == len(otras_variables):
            return restriccion.holds(asignacion)
        else:
            variable = otras_variables[ind]
            for valor in dominios[variable]:
                asignacion[variable] = valor
                if self.se_mantiene(dominios, restriccion, asignacion, otras_variables, ind+1):
                    return True
            return False

    def una_solucion(self, dominios = None, para_revisar = None):
        '''retorna una solución al CSP actual o retorna Falso si no hay soluciones. para_revisar es un conjunto de arcos que se deben revisar'''
        if dominios is None:
            dominios =  self.csp.dominios
        nuevos_dominios = self.hacer_arcos_consistentes(dominios, para_revisar)
        if any(len(nuevos_dominios[variable]) == 0 for variable in dominios): #alguna variable no tiene elementos en el dominio
            return False
        elif all(len(nuevos_dominios[variable]) == 1 for variable in dominios): #ya se tiene una solución
            self.visualizar(1, "solución: ", {variable: seleccionar(nuevos_dominios[variable]) for variable in nuevos_dominios})
            return {variable: seleccionar(nuevos_dominios[variable]) for variable in dominios}
        else:
            variable = self.seleccionar_variable(x for x in self.csp.variables if len(nuevos_dominios[x])>1)
            if variable:
                dominio1, dominio2 = particion_dominio(nuevos_dominios[variable])
                self.visualizar(1, "...particionando ", variable, " en ", dominio1, " y ", dominio2)
                nuevos_dominios1 = copiar_con_asignacion(nuevos_dominios, variable, dominio1)
                nuevos_dominios2 = copiar_con_asignacion(nuevos_dominios, variable, dominio2)
                para_revisar = self.nuevo_para_revisar(variable, None)
                self.visualizar(1, ' agregando ', para_revisar if para_revisar else " nada ", " para revisar ")
                return self.una_solucion(nuevos_dominios1, para_revisar) or self.una_solucion(nuevos_dominios2, para_revisar)

    def seleccionar_variable(self, siguiente_variable):
        '''retorna la siguiente variable para hacer la división'''
        return seleccionar(siguiente_variable)

def particion_dominio(dominio):
    '''partición del dominio en dos'''
    dividir = len(dominio)//2
    dominio1 = set(list(dominio)[:dividir])
    dominio2 = dominio - dominio1
    return dominio1, dominio2

def copiar_con_asignacion(dominios, variable = None, nuevo_dominio = {True, False}):
    '''crea una copia de los dominios con asignación variable = nuevo_dominio. Si variable = None quiere decir que solo es una copia'''
    nuevosdominios = dominios.copy()
    if variable is not None:
        nuevosdominios[variable] = nuevo_dominio
    return nuevosdominios

def seleccionar(iterable):
    '''selecciona un elemento de iterable, retorna None si no existe dicho elemento.'''
    for e in iterable:
        return e


csp_ejemplo = CSP({'A' : {1,2,3,4}, 'B':{1,2,3,4}, 'C':{1,2,3,4}},
                  [Restriccion(('A','B'), lt),
                  Restriccion(('B','C'), lt),
                  Restriccion(('B',), noes(2))])
print(Solucionador_consistencia(csp_ejemplo).una_solucion())