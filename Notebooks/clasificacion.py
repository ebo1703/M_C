
#Librerias necesarias

import numpy as np
import pandas as pd

#Music21 y su configuración para musescore

from music21 import *  #Importar todas las funciones de music21
us = environment.UserSettings()
us['musescoreDirectPNGPath'] = '/usr/bin/mscore'  #Ruta de musescore
us['directoryScratch'] = '/tmp'

#Función para encontrar que intervalos tienen el 6/4 (Garantizando que sea 4 justa)


def encontrar_64(dataframe):

  """
  Función que me devuelve los indices de las filas que contienen los acordes
  6/4, donde se verifica que la cuarta sea justa(P4) y la sexta sea mayor o menor (M6 o m6)

  Parameters
  ----------
  dataframe : DataFrame
      DataFrame con todos los acordes de la partitura

  Returns
  -------
  indices : list
      Lista con los indices de las filas que cumplen con la condición de tener
      el acorde 6/4.
  
  df_filtrado : DataFrame
      DataFrame con los acordes que cumplen con la condición de tener el acorde 6/4
  """
  
  nuevalista = dataframe['Nombre intervalo simplificado']
  indices = []
  for indice, lista in enumerate(nuevalista):
    if ('M6' in lista or 'm6' in lista) and 'P4' in lista:
      
      indice_fila = indice
      indices.append(indice_fila)

    df_filtrado = dataframe.iloc[indices]

  return indices, df_filtrado


def extraer_bajo(dataframe):

    """ 
    Función que extrae las notas del bajo de los acordes 6/4 del dataframe
    
    Parameters
    ----------
    dataframe : DataFrame
        Dataframe filtrado de los acordes de la partitura 
        
    Returns
    -------
    bajos : list
        Lista con las notas del bajo de los acordes 6/4
    
    """
    
    nuevalista = dataframe['Notas']
    bajos = []
    for lista in nuevalista:
        bajos.append(lista[0][0])

    return bajos

def voces_64(df):

    """
    Función que encuentra las voces que contienen el intervalo 6/4 en un dataframe de pandas

    Parameters
    ----------
    df : dataframe
        Dataframe de pandas con información de los acordes de la partitura

    Returns

    n_indice4 : list
        Lista con los índices de las voces que contienen el intervalo de cuarta justa
    n_indice6 : list
        Lista con los índices de las voces que contienen el intervalo de sexta mayor o menor

        
    """
    # nuevalista = df['Nombre intervalo simplificado']
    n_indice4 = []
    n_indice6 = []
    a = df['Nombre intervalo simplificado'].tolist()
    for j in a:
        
            voz = j
            indice4 = voz.index('P4') +1
            
            if 'm6' in voz:
                indice6 = voz.index('m6') + 1
            if 'M6' in voz:
                indice6 = voz.index('M6') + 1
            n_indice4.append(indice4)
            n_indice6.append(indice6)
        

    return n_indice4 , n_indice6




def notas_bajos(df,lista_indice):
    
    """ 
    Función que extrae las notas del bajo de los acordes de una lista de índices de un dataframe
    la lista es la correspondiente a los acordes 6/4
    El dataframe es el dataframe de todos los acordes de la partirura 
    que se está analizando. Devuelve una lista con las notas del bajo antes y después de los acordes 6/4 

    Parameters
    ----------
    df : DataFrame
        Dataframe de los acordes de la partitura

    lista_indice : list
        Lista de índices de los acordes 6/4

    Returns
    -------
    BB_n : list
        Lista con las notas del bajo de los acordes antes de los acordes 6/4

    BA_n : list
        Lista con las notas del bajo de los acordes después de los acordes 6/4


    """
    
    
    BB_n = []
    BA_n = []

    for j in lista_indice:

        BB_notas = []
        for i in range(1,5):
            NB = df.iloc[j]['Notas'][0][0]
            BB = df.iloc[j-i]['Notas'][0][0]
            
            # BB_notas.append(NB)
            BB_notas.append(BB)
            if NB != BB:
                break
        BB_n.append(BB_notas)

        BA_notas = []

        for i in range(1,5):
            NB = df.iloc[j]['Notas'][0][0]
            BA = df.iloc[j+i]['Notas'][0][0]

            # BB_notas.append(NB)
            BA_notas.append(BA)
            if NB != BA:
                break
        BA_n.append(BA_notas)

    return BB_n, BA_n

    # df.iloc[lista_64[j]-i]['Notas'][ind4[j]][0]
        

def notas_voces(df,ind4,ind6,BB_n,BA_n,lista_64):
    
    """ 
    Función que extrae las notas de las voces (4 y 6) de los acordes antes y después de los acordes 6/4
    El dataframe es el dataframe de todos los acordes de la partirura 
    que se está analizando. Devuelve una lista con las notas de las voces antes y después de los
    acordes 6/4 para la cuarta y la sexta

    Parameters
    ----------
    df : DataFrame
        Dataframe de los acordes de la partitura

    ind4 : list
        Lista de índices de las voces 4

    ind6 : list
        Lista de índices de las voces 6

    BB_n : list
        Lista con las notas del bajo de los acordes antes de los acordes 6/4

    BA_n : list
        Lista con las notas del bajo de los acordes después de los acordes 6/4

    lista_64 : list
        Lista de índices de los acordes 6/4

    Returns
    -------
    voces4b : list
        Lista con las notas de la cuarta antes de los acordes 6/4

    voces4a : list
        Lista con las notas de la cuarta  después de los acordes 6/4

    voces6b : list
        Lista con las notas de la sexta  antes de los acordes 6/4

    voces6a : list
        Lista con las notas de la sexta después de los acordes 6/4


        

    """

    voces4b = []
    voces4a = []
    voces6b = []
    voces6a = []


    for j in range(len(ind4)):
        notas4b = []
        notas6b = []
        Notas4 = []
        Notas6 = []

        
        
        for i in range(1,len(BB_n[j])+1):
            N4b = df.iloc[lista_64[j]-i]['Notas'][ind4[j]][:-1]
            N6b = df.iloc[lista_64[j]-i]['Notas'][ind6[j]][:-1]
            
            notas4b.append(N4b)
            notas6b.append(N6b)

            
        voces4b.append(notas4b)
        voces6b.append(notas6b)

        notas4a = []
        notas6a = []

        for i in range(1,len(BA_n[j])+1):
            N4a = df.iloc[lista_64[j]+i]['Notas'][ind4[j]][:-1]
            N6a = df.iloc[lista_64[j]+i]['Notas'][ind6[j]][:-1]
            notas4a.append(N4a)
            notas6a.append(N6a)
    
            
        voces4a.append(notas4a)
        voces6a.append(notas6a)

    return voces4b, voces4a, voces6b, voces6a

#Extraer nota del bajo de los acordes 

def extraer_n4_n6(dataframe,indice4,indice6):

    """ 
    Función que extrae las notas de la cuarta y sexta de los acordes 6/4 del dataframe filtrado

    Parameters

    ----------

    dataframe : DataFrame

        Dataframe filtrado de los acordes de la partitura

    indice4 : list

        Lista con los índices de las voces que contienen el intervalo de cuarta justa

    indice6 : list

        Lista con los índices de las voces que contienen el intervalo de sexta mayor o menor

    Returns

    -------

    cuartas : list

        Lista con las notas de la cuarta de los acordes 6/4


    sextas : list

        Lista con las notas de la sexta de los acordes 6/4
         
    
    """
   
    cuartas = []
    sextas = []
    for i in range(0,len(indice4)):
        not4 = dataframe.iloc[i]['Notas'][indice4[i]][:-1]
        not6 = dataframe.iloc[i]['Notas'][indice6[i]][:-1]
        cuartas.append(not4) 
        sextas.append(not6)  
        
    return cuartas, sextas 


def condiciones_paso(bajos, BB_n, BA_n, N4sb, N6sb, V4b, V6b, V4a, V6a):
    """
    Esta función calcula los intervalos entre bb y nb y ba y nb, y verifica dos condiciones.

    Parámetros:
    bajos, BB_n, BA_n, N4sb, N6sb, V4b, V6b, V4a, V6a: listas de notas o valores relacionados con las notas.

    Devuelve:
    seg_m_b, seg_m_a, cond3, cond4: numpy arrays con los resultados de las verificaciones.

    suma: numpy array con la suma de las verificaciones.
    
    """

    inter_BA = []
    inter_BB = []
    cond3 = []
    cond4 = []

    for i in range(len(bajos)):

        bb = BB_n[i][-1]   # Nota del bajo antes del acorde 6/4, con BB != NB 
        ba = BA_n[i][-1]    # Nota del bajo después del acorde 6/4, con BA != NB
        nb = bajos[i]       # Nota del bajo del acorde 6/4

        n4sb = N4sb[i]   # Nota de la voz de la cuarta del acorde 6/4 
        n6sb = N6sb[i]   # Nota de la voz de la sexta del acorde 6/4

        n4bb = V4b[i][-1]  # Nota de la cuarta antes del acorde 6/4
        n6bb = V6b[i][-1]  # Nota de la sexta antes del acorde 6/4

        n4ba = V4a[i][-1]  # Nota de la cuarta después del acorde 6/4
        n6ba = V6a[i][-1]  # Nota de la sexta después del acorde 6/4

        #Definir las notas con music21

        bb = note.Note(bb)  
        ba = note.Note(ba)
        nb = note.Note(nb)

        #Definir los intervalos con music21

        int_b = interval.notesToInterval(bb,nb)
        int_a = interval.notesToInterval(ba,nb)

        #Agregar los intervalos a las listas 
        inter_BA.append(int_a.semiSimpleName)
        inter_BB.append(int_b.semiSimpleName)

        if (bb<nb and ba>nb) or (bb>nb and ba<nb):   #Condición 3
            cond3.append(True)
        else:
            cond3.append(False)

        if (n4sb == n4bb) and (n4sb == n4ba):   #Condición 4
            cond4.append(True)
        else:
            cond4.append(False)

    seg_m_b = [i == 'm2' for i in inter_BB]  #Verificar si son segunda menor (primera condición)
    seg_m_a = [i == 'm2' for i in inter_BA]  #Verificar si son segunda menor (segunda condición)

    #Convertir a numpy array
    seg_m_b, seg_m_a = np.array(seg_m_b), np.array(seg_m_a) 
    cond3 = np.array(cond3)   
    cond4 = np.array(cond4)

    #Sumar todas las condiciones

    suma = np.sum([cond3,cond4,seg_m_a,seg_m_b],axis=0)

    return seg_m_b, seg_m_a, cond3, cond4, suma


def condiciones_cadencial(bajos, N4sb, N6sb, V4a, V6a):
    
    """
    Esta función permite calcular las condiciones para verificar si el acorde
    6/4 es cadencial.


    """

    inter_cuarta = []
    inter_sexta = []
    

    for i in range(len(bajos)):

        #Cuartas
        n4sb = N4sb[i]   # Nota de la voz de la cuarta del acorde 6/4 

        #n4bb = V4b[i][-1]  # Nota de la cuarta antes del acorde 6/4
    
        n4ba = V4a[i][-1]  # Nota de la cuarta después del acorde 6/4


        #Sextas
        n6sb = N6sb[i]   # Nota de la voz de la sexta del acorde 6/4
        n6ba = V6a[i][-1]  # Nota de la sexta después del acorde 6/4


        #Definir las notas con music21

        sb4 = note.Note(n4sb)  
        ba4 = note.Note(n4ba)
        sb6 = note.Note(n6sb)
        ba6 = note.Note(n6ba)

        #Definir los intervalos con music21

        int_b = interval.notesToInterval(sb4,ba4)
        int_a = interval.notesToInterval(sb6,ba6)

        #Agregar los intervalos a las listas 
        inter_cuarta.append(int_a.semiSimpleName)
        inter_sexta.append(int_b.semiSimpleName)

    terceras = [i == 'M3' for i in inter_cuarta]  #Verificar si son segunda menor (primera condición)
    sextas = [i == 'P5' for i in inter_sexta]  #Verificar si son segunda menor (segunda condición)

    #Convertir a numpy array
    terceras, sextas = np.array(terceras), np.array(sextas) 
    

    #Sumar todas las condiciones

    suma = np.sum([terceras,sextas],axis=0)

    return terceras ,  sextas , suma , inter_cuarta , inter_sexta


def acorde6_4_paso(dataframe):

    """
    Función que ecuentra todas las varibles necesarias para verificar si se cumple la condición de paso
    en los acordes 6/4 de un dataframe de pandas y retorna 

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe de los acordes de la partitura

    Returns
    -------


    """
    
    #Encontrar los acordes 6/4
    indices, df_filtrado = encontrar_64(dataframe)

    #Extraer las notas del bajo de los acordes 6/4
    bajos = extraer_bajo(df_filtrado)

    #Encontrar las voces que contienen el intervalo 6/4
    ind4, ind6 = voces_64(df_filtrado)

    #Extraer las notas del bajo antes y después de los acordes 6/4
    BB_n, BA_n = notas_bajos(dataframe,indices)

    #Extraer las notas de las voces antes y después de los acordes 6/4
    voces4b, voces4a, voces6b, voces6a = notas_voces(dataframe,ind4,ind6,BB_n,BA_n,indices)

    #Extraer las notas de la cuarta y sexta de los acordes 6/4
    N4sb, N6sb = extraer_n4_n6(df_filtrado,ind4,ind6)

    #Verificar las condiciones de paso
    seg_m_b, seg_m_a, cond3, cond4, suma = condiciones_paso(bajos, BB_n, BA_n, N4sb, N6sb, voces4b, voces6b, voces4a, voces6a)


    #Crear un dataframe con la información de los acordes 6/4
    df_condiciones = pd.DataFrame({'Acordes': df_filtrado['Notas'], 'Condición1': seg_m_b, 'Condición2': seg_m_a, 'Condición3': cond3, 'Condición4': cond4, 'Suma': suma})
    return df_condiciones


def acorde6_4_cadencial(dataframe):


    #Encontrar los acordes 6/4
    indices, df_filtrado = encontrar_64(dataframe)

    #Extraer las notas del bajo de los acordes 6/4
    bajos = extraer_bajo(df_filtrado)

    #Encontrar las voces que contienen el intervalo 6/4
    ind4, ind6 = voces_64(df_filtrado)

    #Extraer las notas de la cuarta y sexta de los acordes 6/4
    N4sb, N6sb = extraer_n4_n6(df_filtrado,ind4,ind6)

    #Extraer las notas del bajo antes y después de los acordes 6/4
    BB_n, BA_n = notas_bajos(dataframe,indices)

    #Extraer las notas de las voces antes y después de los acordes 6/4
    voces4b, voces4a, voces6b, voces6a = notas_voces(dataframe,ind4,ind6,BB_n,BA_n,indices)

    #Verificar condiciones para el 6/4 de cadencial
    terceras ,  sextas , suma , inter_cuarta , inter_sexta = condiciones_cadencial(bajos,N4sb,N6sb,voces4a,voces6a)

    #Crear un dataframe con la información de los acordes 6/4

    df_condiciones = pd.DataFrame({'Acordes': df_filtrado['Notas'], 'Terceras': terceras, 'Sextas': sextas, 'inter_3': inter_cuarta, 'inter_5': inter_sexta, 'Suma': suma})
    return df_condiciones