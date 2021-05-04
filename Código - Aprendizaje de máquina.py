#!/usr/bin/env python
# coding: utf-8

# $\mathbf{X}$ matriz de características de entrada\
# $\mathbf{Y}$ matriz de características objetivo o etiquetas

# In[2]:


import math, random
import csv
from Busqueda import Visualizable

booleana = [False, True]

class Data(Visualizable):
    '''Un conjunto de datos consiste en una lista de datos de entrenamiento (train) y una lista de validación (test)'''
    seed = None #la idea es que se haga None si queremos un conjunto diferente cada vez
    
    def __init__(self, train, test = None, prob_test = 0.30, indice_target = 0, encabezado = None):
        '''Train es una lista de tuplas representando las observaciones o ejemplos de entrenamiento.
        Test es una lista de tuplas representando las observaciones o ejemplos de validación. Si test = None
        se crea un conjunto de validacióln seleccionando muestras con probabilidad prob_test.
        indice_target es el índice de la característica objetivo. Si  es mayor que el número de propiedades, quiere
        decir que no hay característica objetivo.
        encabezado es una lista de los nombres de las características'''
        
        if test is None:
            train, test = particionamiento_data(train, prob_test, seed = self.seed)
        self.train = train
        self.test = test
        self.visualizar(2, "Tuplas leidas. \nConjunto de entrenamiento ", len(train), " ejemplos. Número de columnas: ",
                       {len(e) for e in train}, "\nConjunto de validación ", len(test), " ejemplos. Número de columnas: ",
                       {len(e) for e in test})
        self.prob_test = prob_test
        self.numero_propiedades = len(self.train[0])
        if indice_target < 0:
            indice_target = self.numero_propiedades + indice_target
        self.indice_target = indice_target
        self.encabezado = encabezado
        self.crear_caracteristicas()
        self.visualizar(2, "Hay ", len(self.caracteristicas_entrada), " caracteristicas de entrada")
        
    def crear_caracteristicas(self):
        '''genera las características de entrada y la característica objetivo. Aquí se asume que todas las características
        tienen rango {0,1}. Si tienen rangos diferentes se debe sobre-escribir'''
        self.caracteristicas_entrada = []
        for i in range(self.numero_propiedades):
            def caracteristica(e, index = i):
                return e[index]
            if self.encabezado:
                caracteristica.__doc__ = self.encabezado[i]
            else:
                caracteristica.__doc__ = "e[" + str(i) + "]"
            caracteristica.rango = [0,1]
            if i == self.indice_target:
                self.target = caracteristica
            else:
                self.caracteristicas_entrada.append(caracteristica)
                
    criterios_evaluacion = ["suma_cuadrados", "suma_absoluta", "logloss"]
    
    def evaluar_dataset(self, data, predictor, criterio_evaluacion):
        '''evalúa el predictor sobre los datos de acuerdo a algún criterio de evaluación. predictor es una función
        que toma un ejemplo y retorna una predicción sobre las características.'''
        assert criterio_evaluacion in self.criterios_evaluacion, str(criterio_evaluacion)
        
        if data:
            try:
                error = sum(error_ejemplo(predictor(ejemplo), self.target(ejemplo), criterio_evaluacion) for ejemplo in data)/len(data)
            except ValueError:
                return float("inf")
            return error
        


# In[ ]:


def particionamiento_data(data, prob_test = 0.30, seed = None):
    '''particiona los datos en conjuntos de entrenamiento (train) y validación (test), donde prob_test es la probabilidad
    de que un ejemplo pertenezca al grupo de validación. Una alternativa es usar random.sample() para garantizar que
    se tenga una proporción de prob_test en los datos de validación.'''
    import numpy as np
    
    train = []
    test = []
    if seed:
        random.seed(seed)
   # perm = np.random.permutation(len(data))
   # print(perm)
    
   # test = list(data[i] for i in perm[:int(prob_test*len(data))])
   # train = list(data[i] for i in perm[int(prob_test*len(data)):])
                
    for ejemplo in data:
        if random.random() < prob_test:
            test.append(ejemplo)
        else: 
            train.append(ejemplo)
    return train, test


# In[ ]:


datos = Data([(0.2, 0.3, 1), (0.4,0.7,2), (0.2,0.4,0.6), (0.2,0.4,3)], indice_target = -1)


# In[ ]:


datos.__dict__


# In[ ]:


def error_ejemplo(prediccion, real, criterio_evaluacion):
    '''retorna el error de la predicción actual dado el valor real de acuerdo a criterio_evaluacion.'''
    
    if criterio_evaluacion == "suma_cuadrados":
        return (prediccion - real)**2
    elif criterio_evaluacion == "suma_absoluta":
        return abs(prediccion - real)
    elif criterio_evalucion == "logloss":
        assert real in [0,1], "real = " + str(real)
        if real == 0:
            return -math.log2(1 - prediccion)
        else:
            return -math.log2(prediccion)
            
    else:
        raise RuntimeError(str(criterio_evaluacion), " no es un criterio de evaluación")


# In[ ]:


class Data_archivo(Data):
    
    def __init__(self, archivo, separador = ',', num_train = None, prob_test = 0.3, tiene_encabezado = False,
                indice_target = 0, caracteristicas_booleanas = True, categoricas = [], incluir = None):
        '''crea un dataset de un archivo.
        separador es el caracter que separa los atributos.
        num_train es un número n que especifica si las primeras n tuplas son entrenamiento o no.
        tiene_encabezado indica si la primera línea del archivo es un encabezado.
        caracteristicas_booleanas indica si queremos crear caracteristicas booleanas. Si es falso se usan las características
        originales.
        categoricas es una lista de características que deben ser tratadas como categóricas.
        incluir es unal ista de índices de columnas para incluir.'''
        
        self.caracteristicas_booleanas = caracteristicas_booleanas
        with open(archivo, 'r', newline = '') as archivo_csv:
            data_all = (linea.strip().split(separador) for linea in archivo_csv)
            if incluir is not None:
                data_all = ([v for (i,v) in enumerate(linea) if i in incluir] for linea in data_all)
            if tiene_encabezado:
                encabezado = next(data_all)
            else:
                encabezado = None
            data_tuplas = (hacer_numeros(d) for d in data_all if len(d)>1) #queda pendiente
            if num_train is not None:
                train = []
                for i in range(num_train):
                    train.append(next(data_tuplas))
                test = list(data_tuplas)
                Data.__init__(self, train, test = test, indice_target = indice_target, encabezado = encabezado)
            else:
                Data.__init__(self, data_tuplas, prob_test = prob_test, indice_target = indice_target, encabezado = encabezado)
          
    
    def __str__(self):
            return("Data: " + str(len(self.train)) + " ejemplos de entrenamiento, " + str(self.test) + " ejemplos de test")
        
        
    '''para la creación de características Booleanas consideraremos tres casos:
    
    1. Cuando el rango solamente tiene dos valores. En ese caso uno se asume como Verdadero.
    2. Cuando todos los valores son numéricos y están ordenados. Se construyen las características Booleanas por intervalos,
    i.e., la característica es e[ind] < corte. Se elije corte si sobrepasar max_cortes.
    3. Cuando los valores no son todos numéricos, se asumen no ordenados y se crea una función indicadora para cada valor.
    '''
    
    def crear_caracteristica(self, max_cortes = 8):
        '''crea características Booleanas a partir de las características de entrada.'''
        
        rangos = [set() for i in range(self.num_propiedades)]
        for ejemplo in self.train:
            for ind,val in enumerate(ejemplo):
                rangos[ind].add(val)
        if self.indice_target <= self.num_propiedades:
            def target(e, indice = self.indice_target):
                return e[indice]
            if self.encabezado:
                target.__doc__ = self.encabezado[self.indice_target]
            else:
                target.__doc__ = "e[" + str(self.indice_target) + "]"
            target.rango = rangos[self.indice_target]
        if self.caracteristicas_booleanas:
            self.caracteristicas_entrada = []
            for ind, rango in enumerate(rangos):
                if len(rango) == 2: # dos valores, uno de los dos se asume como verdadero
                    valor_verdad = list(rango)[1] #asigna uno como verdadero
                    def caracteristica(e, i = ind, tv = valor_verdad):
                        return e[i] == tv
                    if self.encabezado:
                        caracteristica.__doc__ = self.encabezado[ind] + " == " + str(valor_verdad)
                    else:
                        caracteristica.__doc__ = "e[" + str(ind) + "] == " + str(valor_verdad)
                    caracteristica.rango = booleana
                    self.caracteristicas_entrada.append(caracteristica)
                elif all(isinstance(val,(int,float)) for val in rango): # todos los valores en el rango son numéricos y ordenados
                    rango_ordenado = sorted(rango)
                    numero_cortes = min(max_cortes, len(rango))
                    posiciones_cortes = [len(rango)*i//numero_cortes for i in range(1,numero_cortes)]
                    for corte in posiciones_cortes:
                        corte_en = rango_ordenado[corte]
                        def caracteristica(e, ind_ = ind, corte_en = corte_en):
                            return e[ind_] < corte_en
                        if self.encabezado:
                            caracteristica.__doc__ = self.encabezado[ind] + " < " + str(corte_en)
                        else:
                            caracteristica.__doc__ = "e[" + str(ind) + "] < " + str(corte_en)
                        caracteristica.rango = booleana
                        self.caracteristicas_entrada.append(caracteristica)
                else: #se crea una variable indicadora para cada valor
                    for val in rango:
                        def caracteristica(e, ind_ = ind, val_ = val):
                            return e[ind_] == val_
                        if self.encabezado:
                            caracteristica.__doc__ = self.encabezado[ind] + " == " + str(val)
                        else:
                            caracteristica.__doc__ = "e[" + str[ind] + "] == " + str(val)
        else: # si caracteristicas_booleanas == False
            self.caracteristicas_entrada = []
            for i in range(self.num_propiedades):
                def caracteristica(e, index = i):
                    return e[index]
                if self.encabezado:
                    caracteristica.__doc__ = self.encabezado[i]
                else:
                    caracteristica.__doc__ = "e[" + str(i) + "]"
                if i == self.indice_target:
                    self.target = caracteristica
                else:
                    self.caracteristicas_entrada.append(caracteristica)
                    

def hacer_numeros(str_list):
    '''hace los elementos de una lista  de strings numéricos si es posible. De otra forma se remueven los espacios iniciales
    y finales'''
    res = []
    for e in str_list:
        try:
            res.append(int(e))
        except ValueError:
            try:
                res.append(float(e))
            except ValueError:
                res.append(e.strip())
    return res
            


# In[ ]:


data = Data_archivo('archivo_prueba.csv', indice_target = -1, tiene_encabezado = True)


# In[ ]:


data.__dict__


# In[ ]:




