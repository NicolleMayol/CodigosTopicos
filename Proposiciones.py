class Clausula():
    '''Una cláusula definida'''

    def __init__(self, cabeza, cuerpo =[]):
        self.cabeza =cabeza
        self.cuerpo = cuerpo

    def __str__(self):
        if self.cuerpo:
            return self.cabeza+ " <- " + "&" .join(self.cuerpo) + "."
        else:
            return self.cabeza + "."

class Observable():
    '''Proposicones que no quiero que sean atómicas. Poder preguntar por el estado de vwrdad de un atomo'''

    def __init__(self, atomo):
        self.atomo = atomo

    def __str__(self):
        return "Pregunta " + self.atomo + "."


def si(resp):
    '''retorna verdaddero si la respuesta es sí'''
    return resp.lower() in ['si', 'Si', 'sí', 'Sí', 's', 'y', 'S', 'Y', 'yes', 'Yes']

from Busqueda import Visualizable

class KB(Visualizable):
    '''La KB es un conjunto de cláusulas. También se crea un diccionario para dar acceso más rápido a las cláusulas con
    un átomo en la cabeza'''

    def __init__(self, declaraciones = []):
        self.declaraciones = declaraciones
        self.clausulas = [c for c in declaraciones if isinstance(c, Clausula)]
        self.observables = [c.atomo for c in declaraciones if isinstance(c, Observable)]
        self.atomo_a_clausula = {}
        for c in self.clausulas:
            if c.cabeza in self.atomo_a_clausula:
                self.atomo_a_clausula[c.cabeza].append(c)
            else:
                self.atomo_a_clausula[c.cabeza] = [c]

    def clausulas_de_atomo(self, a):
        '''retorna un conjunto de cláusulas con un átomo "a" como cabeza'''
        if a in self.atomo_a_clausula:
            return self.atomo_a_clausula[a]
        else:
            return set()

    def __str__(self):
        return '\n'.join([str(c) for c in self.declaraciones])


covid_KB = KB([Clausula('no_contagio', ['en_casa']),
               Clausula('en_casa'),
               Clausula('mas_trabajo', ['cuarentena', 'en_casa']),
               Observable('fiebre'),
               Clausula('escalofrio', ['fiebre']),
               Clausula('cuarentena'),
               Clausula('no_contagio', ['cuarentena']),
               Clausula('kata_gata', ['mas_trabajo', 'sofa'])])


def punto_fijo(kb):
    '''retorna el punto fijo de la base de conocimineto kb, i.e. el conjunto mínimo de consecuencias'''
    fp = pregunta_observables(kb)
    adicionado = True
    while adicionado:
        adicionado = False #se vuelve verdadero cuando se agrega un átomo al fp durante esta iteración
        for c in kb.clausulas:
            if c.cabeza not in fp and all(b in fp for b in c.cuerpo):
                fp.add(c.cabeza)
                adicionado = True
                kb.visualizar(2, c.cabeza, " adicionado al fp por la cláusula ", c)
    return fp


def pregunta_observables(kb):
    return{a for a in kb.observables if si(input(a + " es verdadero?"))}

plomeria_KB = KB([Clausula('presurizacion_p1'),
                  Clausula('presurizacion_p2', ['on_t1', 'presurizacion_p1']),
                  Clausula('flujo_ducha', ['on_t2', 'presurizacion_p2']),
                  Clausula('mojado_bañera', ['flujo_ducha']),
                  Clausula('flujo_d2', ['mojado_bañera', 'sin_tapon_bañera']),
                  Observable('on_t1'),
                  Observable('on_t2'),
                  Observable('sin_tapon_bañera'),
                  Clausula('flujo_d1', ['flujo_d2']),
                  Clausula('presurizacion_p3', ['on_t1', 'presurizacion_p1']),
                  Observable('on_t3'),
                  Clausula('flujo_lavamanos', ['on_t3', 'presurizacion_p3']),
                  Clausula('mojado_lavamanos', ['flujo_lavamanos']),
                  Clausula('flujo_d3', ['mojado_lavamanos', 'sin_tapon_lavamanos']),
                  Clausula('flujo_d1', ['flujo_d3']),
                  Clausula('sin_tapon_lavamanos'),
                  Clausula('piso_mojado', ['con_tapon_bañera', 'flujo_ducha', 'bañera_llena', 'no_flujo_d2']),
                  Clausula('piso_mojado', ['con_tapon_lavamanos', 'flujo_lavamanos', 'lavamanos_lleno', 'no_flujo_d3']),
                  Observable('con_tapon_bañera'),
                  Observable('con_tapon_lavamanos'),
                  Observable('bañera_llena'),
                  Observable('lavamanos_lleno'),
                  Clausula('no_flujo_d2', ['con_tapon_bañera', 'tapon_bañera_funcional']),
                  Clausula('no_flujo_d3', ['con_tapon_lavamanos', 'tapon_lavamanos_funcional']),
                  Observable('tapon_bañera_funcional'),
                  Observable('tapon_lavamanos_funcional')])

#print('piso_mojado' in punto_fijo(plomeria_KB))

def arriba_abajo(kb, cuerpo_respuesta, indentacion = ""):
    '''retorna Verdadero si kb |- cuerpo_respuesta.
    cuerpo_respuesta con los átomos a probar'''
    kb.visualizar(1, indentacion, 'si <-', ' ^ '.join(cuerpo_respuesta))
    if cuerpo_respuesta:
        seleccion = cuerpo_respuesta[0] # selecciona el primer átomo de cuerpo_respuesta
        if seleccion in kb.observables:
            return(si(input(seleccion + " es verdadero? ")) and arriba_abajo(kb, cuerpo_respuesta[1:], indentacion + " "))
        else:
            return any(arriba_abajo(kb, cl.cuerpo + cuerpo_respuesta[1:] , indentacion + " ") for cl in kb.clausulas_de_atomo(seleccion))
    else:
        return True #cuando el cuerpo_respuesta queda vacío


ejemplo_KB = KB([Clausula('a', ['b', 'c']),
                Clausula('b', ['g', 'e']),
                Clausula('b', ['d', 'e']),
                Clausula('c', ['e']),
                Clausula('d'),
                Clausula('e'),
                Clausula('f', ['a', 'g'])])
print(arriba_abajo(plomeria_KB, ['piso_mojado']))

naveKB = KB([Clausula('t1'),
             Clausula('t2'),
             Clausula('v1_abierto'),
             Clausula('v2_abierto'),
             Clausula('v3_abierto'),
             Clausula('v4_abierto'),
             Clausula('v5_abierto'),
             Clausula('v6_abierto'),
             Clausula('v7_abierto'),
             Clausula('v8_abierto'),
             Clausula('v9_abierto'),
             Clausula('v10_abierto'),
             Clausula('v11_abierto'),
             Clausula('v12_abierto'),
             Clausula('v13_abierto'),
             Clausula('v14_abierto'),
             Clausula('v15_abierto'),
             Clausula('v16_abierto'),
             Clausula('v1_ok'),
             Clausula('v2_ok'),
             Clausula('v3_ok'),
             Clausula('v4_ok'),
             Clausula('v5_ok'),
             Clausula('v6_ok'),
             Clausula('v7_ok'),
             Clausula('v8_ok'),
             Clausula('v9_ok'),
             Clausula('v10_ok'),
             Clausula('v11_ok'),
             Clausula('v12_ok'),
             Clausula('v13_ok'),
             Clausula('v14_ok'),
             Clausula('v15_ok'),
             Clausula('v16_ok'),
             Clausula('v1p', ['t1']),
             Clausula('v2p', ['t2']),
             Clausula('v3p', ['t1']),
             Clausula('v4p', ['t2']),
             Clausula('v5p', ['v1_abierto', 'v1_ok', 'v1p']),
             Clausula('v6p', ['v1_abierto', 'v1_ok', 'v1p']),
             Clausula('v7p', ['v2_abierto', 'v2_ok', 'v2p']),
             Clausula('v8p', ['v2_abierto', 'v2_ok', 'v2p']),
             Clausula('v9p', ['v3_abierto', 'v3_ok', 'v3p']),
             Clausula('v10p', ['v3_abierto', 'v3_ok', 'v3p']),
             Clausula('v11p', ['v4_abierto', 'v4_ok', 'v4p']),
             Clausula('v12p', ['v4_abierto', 'v4_ok', 'v4p']),
             Clausula('v13p', ['v5_abierto', 'v5_ok', 'v5p']),
             Clausula('v13p', ['v6_abierto', 'v6_ok', 'v6p']),
             Clausula('v14p', ['v7_abierto', 'v7_ok', 'v7p']),
             Clausula('v14p', ['v8_abierto', 'v8_ok', 'v8p']),
             Clausula('v15p', ['v9_abierto', 'v9_ok', 'v9p']),
             Clausula('v15p', ['v10_abierto', 'v10_ok', 'v10p']),
             Clausula('v16p', ['v11_abierto', 'v11_ok', 'v11p']),
             Clausula('v16p', ['v12_abierto', 'v12_ok', 'v12p']),
             Clausula('e1', ['v13_abierto', 'v13_ok', 'v13p', 'v14_abierto', 'v14_ok', 'v14p']),
             Clausula('e2', ['v15_abierto', 'v15_ok', 'v15p', 'v16_abierto', 'v16_ok', 'v16p']),
             Clausula('E', ['e1']),
             Clausula('E', ['e2']),
             ])

print(arriba_abajo(naveKB, ['E']))
print(punto_fijo(naveKB))

