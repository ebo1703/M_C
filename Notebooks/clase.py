#Music21 y su configuración para musescore

from music21 import *  #Importar todas las funciones de music21
us = environment.UserSettings()
us['musescoreDirectPNGPath'] = '/usr/bin/mscore'  #Ruta de musescore
us['directoryScratch'] = '/tmp'


import pandas as pd


class cuartas:

    """
    Clase para trabajar con partituras  y obtener información de las mismas

    """

    

    def __init__(self, archivo):
        
        """
        Constructor de la clase
        :param archivo: archivo xml de la partitura
        
        Se debe tener importado 'Pandas' y 'music21'

        """

        self.archivo = archivo  #Path de la partitura
        self.s = converter.parse(archivo) #Lectura del archivo

        #Listas para guardar la info de la partitura
        self.acordes = []
        self.beats = []
        self.notas = []
        self.intervalos = []
        self.num_semitonos_intervalo = []
        self.nombre_intervalos_sim = []
        self.nombre_intervalos_com = []
        self.compas = []
        self.division = []
        self.tipo_div = []

    def mostrar_partitura(self):
        
        """
        Método para mostrar la partitura
        """
        self.s.show()


    def chordify(self):
        """
        Método para realizar chordify a toda la partitura,
        juntar todas las notas que suenan simultáneamente
        """

        try:
            self.s = self.s.chordify()
            return self.s
        except Exception as e:
            print(f"Error al realizar chordify: {e}")
            return None
    
    def asignar_intervalos(self):
        
        """

        Método para asignar los intervalos dentro de la partitura

        """

        try:
            for c in self.s.recurse().getElementsByClass('Chord'):
                #Esta opción es para que quedén en la misma octava 
                # c.closedPosition(forceOctave=4, inPlace=True) 
                c.annotateIntervals(inPlace=True)
        
        except Exception as e:
            print(f"Error al asignar intervalos: {e}")
            return None

    def mostrar_intervalos(self):

        """ 
        Método para mostar en pantalla los acordes y sus intervalos

        """

        try:
            for c in self.s.recurse().getElementsByClass('Chord'):
                print(c, end=" ")
                for l in c.lyrics:
                    print(l.text, end=" ")
                print()
        except Exception as e:
            print(f"Error al mostrar los intervalos: {e}")
            return None

    def extraer_acordes(self):

        """
        Método que guarda todos los acordes de la partitura en el 
        atributo 'acordes'.
        """
        try:
            for c in self.s.recurse().getElementsByClass('Chord'):
                self.acordes.append(c)
            return self.acordes
        except Exception as e:
            print(f"Error al extraer acordes: {e}")
            return None
    

    #Método que no sirvió xd
    # def extraer_intervalos(self):
    #     self.intervalos = []
    #     for c in self.extraer_acordes():
    
    #         for l in c.lyrics:
    #             self.intervalos.append(int(l.text))

    #     return self.intervalos   

    def extraer_df(self):

        """

        Método para extraer un dataframe con la información de la partitura
        :return: dataframe con la información de la partitura

        ¡¡IMPORTANTE!!:

        El método de 'extraer_df' dentro llama a los métodos 'chordify', 
        'asignar_intervalos' y 'extraer_acordes' para obtener la información de la partitura.
        No es necesario llamar a estos métodos de forma individual, ya que el método 'extraer_df'
        los llama internamente.
        
        """
        try:
            # Métodos que dan la info que necesita de la partitura
            self.chordify()
            self.asignar_intervalos()
            self.extraer_acordes()

            acordes = self.acordes

            for i in acordes:
                self.notas.append([j.name + str(j.octave) for j in i.notes])
                self.beats.append(i.beat)
                self.intervalos.append([int(l.text) for l in i.lyrics])
                self.compas.append(i.measureNumber)
                self.division.append(i.duration.quarterLength)
                self.tipo_div.append(i.duration.type)

                # Nombres intervalos
                notas_inter_com = []
                notas_inter_sim = []
                semitonos = []
                for j in range(len(i) - 1):  # Número de intervalos = notas -1 
                    n1 = i[0]
                    n2 = i[j + 1]
                    intervalo = interval.notesToInterval(n1, n2)
                    notas_inter_com.append(intervalo.semiSimpleNiceName)
                    notas_inter_sim.append(intervalo.semiSimpleName)
                    semitonos.append(intervalo.semitones)
                self.nombre_intervalos_com.append(notas_inter_com)
                self.nombre_intervalos_sim.append(notas_inter_sim)
                self.num_semitonos_intervalo.append(semitonos)

            self.df = pd.DataFrame({
                'Notas': self.notas,
                'Intervalos': self.intervalos,
                'Nombre intervalo simplificado': self.nombre_intervalos_sim,
                'Num_semitonos': self.num_semitonos_intervalo,
                'Nombre intervalo completo': self.nombre_intervalos_com,
                'Beat': self.beats,
                'Compás': self.compas,
                'Duración': self.division,
                'Tipo': self.tipo_div
            })

            return self.df

        except Exception as e:
            print(f"Error general en extraer_df: {e}")
            return None
    
    

