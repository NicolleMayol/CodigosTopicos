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


covid_KB = KB([Clausula('no_contagio', ['en_casa']), #no contagio si en casa
               Clausula('en_casa'), #atómica
               Clausula('mas_trabajo', ['cuarentena', 'en_casa']), #si cuarenta y en casa, más trabajo
               Observable('fiebre'), #observable (se pregunta)
               Clausula('escalofrio', ['fiebre']), #si fiebre, escalofrío
               Clausula('cuarentena'), #atómica
               Clausula('no_contagio', ['cuarentena']), #si cuarentena, no contagio
               Clausula('kata_gata', ['mas_trabajo', 'sofa'])]) #si más trabajo y sofa, kata gata


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


lavamanos_kb= KB([Clausula('presurizacion_p1'),
                  Clausula('presurización_p2', ['on_t1','presurización_p1']),
                  Clausula('flujo_ducha', ['on_t2', 'presurizacion_p2']),
                  Clausula('mojado_bañera',['flujo_ducha']),
                  Clausula('flujo_d2', ['mojado_bañera','sin_tapon_bañera']),
                  Observable('on_t1'),
                  Observable('on_t2'),
                  Observable('sin_tapon_bañera'),
                  Clausula('presurización_p3', ['on_t1','presurización_p1']),
                  Observable('on_t3'),
                  Clausula('flujo_lavamanos',['on_t3', 'presurización_p3']),
                  Clausula('mojado_lavamanos',['flujo_lavamanos']),
                  Clausula('flujo_d3', ['mojado_lavamos','sin_tapon_lavamanos']),
                  Observable('sin_tapon_lavamanos'),
                  Observable('con_tapon_lavamanos'),
                  Observable('con_tapon_bañera'),
                  Observable('bañera_llena'),
                  Observable('lavamanos_lleno'),
                  Clausula('flujo_d1',['flujo_d2']),
                  Clausula('flujo_d1',['flujo_d3']),
                  Observable('tapon_lavamanos_f'),
                  Observable('tapon_bañera_f'),
                  Clausula('piso_mojado',['lavamanos_lleno','tapon_lavamanos_f', 'con_tapon_lavamanos']),
                  Clausula('piso_mojado',['bañera_llena','tapon_bañera_f','con_tapon_bañera']),
])
#print('piso_mojado' in punto_fijo(lavamanos_kb))


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
#print(arriba_abajo(plomeria_KB, ['piso_mojado']))

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

#print(arriba_abajo(naveKB, ['E']))


empuje_KB = KB([Clausula('t1'),
                Clausula('t2'),
                Clausula('v1a'),
                Clausula('v2a'),
                Clausula('v3a'),
                Clausula('v4a'),
                Clausula('v5a'),
                Clausula('v6a'),
                Clausula('v7a'),
                Clausula('v8a'),
                Clausula('v9a'),
                Clausula('v10a'),
                Clausula('v11a'),
                Clausula('v12a'),
                Clausula('v13a'),
                Clausula('v14a'),
                Clausula('v15a'),
                Clausula('v16a'),

                Clausula('v1ok'),
                Clausula('v2ok'),
                Clausula('v3ok'),
                Clausula('v4ok'),
                Clausula('v5ok'),
                Clausula('v6ok'),
                Clausula('v7ok'),
                Clausula('v8ok'),
                Clausula('v9ok'),
                Clausula('v10ok'),
                Clausula('v11ok'),
                Clausula('v12ok'),
                Clausula('v13ok'),
                Clausula('v14ok'),
                Clausula('v15ok'),
                Clausula('v16ok'),

                Clausula('v1p', ['t1']),
                Clausula('v2p', ['t2']),
                Clausula('v3p', ['t1']),
                Clausula('v4p', ['t2']),
                Clausula('v5p', ['v1p','v1a', 'v1ok']),
                Clausula('v6p', ['v1p', 'v1a', 'v1ok']),
                Clausula('v7p', ['v2p', 'v2a', 'v2ok']),
                Clausula('v8p', ['v2p', 'v2a', 'v2ok']),
                Clausula('v9p', ['v3p', 'v3a', 'v3ok']),
                Clausula('v10p', ['v3p', 'v3a', 'v3ok']),
                Clausula('v11p', ['v5p', 'v4a', 'v4ok']),
                Clausula('v12p', ['v4p', 'v4a', 'v4ok']),

                Clausula('v13p', ['v5p', 'v5a', 'v5ok']),
                Clausula('v13p', ['v6p', 'v6a', 'v6ok']),
                Clausula('v14p', ['v7p', 'v7a', 'v7ok']),
                Clausula('v14p', ['v8p', 'v8a', 'v8ok']),
                Clausula('v15p', ['v9p', 'v9a', 'v9ok']),
                Clausula('v15p', ['v10p', 'v10a', 'v10ok']),
                Clausula('v16p', ['v11p', 'v11a', 'v11ok']),
                Clausula('v16p', ['v12p', 'v12a', 'v12ok']),

                Clausula('e1', ['v13p', 'v13a', 'v13ok', 'v14p', 'v14a', 'v14ok']),
                Clausula('e2', ['v15p', 'v15a', 'v15ok', 'v16p', 'v16a', 'v16ok']),

                Clausula('e', ['e1']),
                Clausula('e', ['e2'])
])

#print(arriba_abajo(empuje_KB, ['e1']))
#print(punto_fijo(empuje_KB))
nave_kb = KB([Clausula('t1'),
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

              Clausula('v13p', ['v5p', 'v5_abierto', 'v5_ok']),
              Clausula('v13p', ['v6p', 'v6_abierto', 'v6_ok']),
              Clausula('v14p', ['v8p', 'v8_abierto', 'v8_ok']),
              Clausula('v14p', ['v7p', 'v7_abierto', 'v7_ok']),
              Clausula('v15p', ['v9p', 'v9_abierto', 'v9_ok']),
              Clausula('v15p', ['v10p', 'v10_abierto', 'v10_ok']),
              Clausula('v16p', ['v11p', 'v11_abierto', 'v11_ok']),
              Clausula('v16p', ['v12p', 'v12_abierto', 'v12_ok']),

              Clausula('e1', ['v13p', 'v13_abierto', 'v13_ok', 'v14p', 'v14_abierto', 'v14_ok']),
              Clausula('e2', ['v15p', 'v15_abierto', 'v15_ok', 'v16p', 'v16_abierto', 'v16_ok']),

              Clausula('E', ['e1']),
              Clausula('E', ['e2'])
              ])

#print(punto_fijo(nave_kb))

red_KB = KB([
    # 𝑒𝑛𝑣𝑖𝑎𝑟_𝑠𝑒ñ𝑎𝑙_𝐺_𝑠𝑐  es verdadero si se envía una señal por el enlace 𝐺.
    Clausula('enviar_señal_G_sc', ['no_dist', 'ok_sc_G']),
    # 𝑜𝑘_𝑠𝑐_𝐺  es verdadero si el enlace 𝐺 está bien.
    Clausula('ok_sc_G', ['ok_sc_lg_trans', 'ok_a3']),
    # 𝑟𝑒𝑐𝑖𝑏𝑖𝑟_𝑠𝑒ñ𝑎𝑙_𝑆  es verdadero si se recibe una señal del satélite  𝑆 .
    Clausula('recibir_señal_s1', ['ok_a1', 'ok_s1ant']),
    Clausula('recibir_señal_s1', ['ok_sc_hg_trans', 'ok_s1ant']),
    Clausula('recibir_señal_s2', ['ok_a2', 'ok_s2ant']),
    Clausula('recibir_señal_s2', ['ok_sc_hg_trans', 'ok_s2ant']),
    # 𝑒𝑛𝑣𝑖𝑎𝑟_𝑠𝑒ñ𝑎𝑙_𝑆  es verdad si se envía una señal al satélite 𝑆.
    Clausula('enviar_señal_s1', ['ok_s1_trans', 'ok_a1']),
    Clausula('enviar_señal_s1', ['ok_s1_trans', 'ok_sc_hg_ant']),
    Clausula('enviar_señal_s2', ['ok_s2_trans', 'ok_a2']),
    Clausula('enviar_señal_s2', ['ok_s2_trans', 'ok_sc_hg_ant']),
    # enviar_señal_gc es verdad si los enlaces entre gc y A están bien
    Clausula('gc_a1'),
    Clausula('gc_a2'),
    # 𝑟𝑒𝑐𝑖𝑏𝑖𝑟_𝑠𝑒ñ𝑎𝑙_𝑔𝑐  es verdad si se recibe una señal de 𝑔𝑐.
    Clausula('recibir_señal_gc', ['gc_a1', 'recibir_señal_s1', 'enviar_señal_s1']),
    Clausula('recibir_señal_gc', ['gc_a2', 'recibir_señal_s2', 'enviar_señal_s2']),
    Clausula('recibir_señal_gc', ['no_dist', 'ok_a3']),
    # 𝑜𝑘_𝐴  es verdadero si la antena  𝐴  está bien.
    Clausula('ok_a1'),
    Clausula('ok_a2'),
    Clausula('ok_a3'),
    # 𝑜𝑘_𝑆𝑎𝑛𝑡  es verdadero si la antena del satélite  𝑆  está bien.
    Clausula('ok_s1ant'),
    Clausula('ok_s2ant'),
    Clausula('ok_sc_hg_ant'),
    # 𝑜𝑘_𝑆_𝑡𝑟𝑎𝑛𝑠  es verdadero si el transmisor del satélite  𝑆  está bien.
    Clausula('ok_s1_trans'),
    Clausula('ok_s2_trans'),
    Clausula('ok_sc_lg_trans'),
    Clausula('ok_sc_hg_trans'),
    # 𝑜𝑘_𝑆  es verdadero si el satélite  𝑆  está bien.
    Clausula('ok_s1', ['ok_S1ant', 'ok_S1_trans']),
    Clausula('ok_s2', ['ok_S2ant', 'ok_S2_trans']),
    # 𝑛𝑜_𝑑𝑖𝑠𝑡  es verdadero si no hay perturbaciones.
    Clausula('no_dist'),

    # comunicación es verdadero si existe comunicación bidireccional
    Clausula('comunicacion',
             ['gc_a1', 'recibir_señal_s1', 'enviar_señal_s1', 'gc_a2', 'recibir_señal_s2', 'enviar_señal_s2',
              'enviar_señal_G_sc', 'recibir_señal_gc'])
])

print(arriba_abajo(red_KB, ['comunicacion']))

print(punto_fijo(red_KB))
