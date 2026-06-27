import Interfaz
import Funciones
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt 
# pyrefly: ignore [missing-import]
import psychrochart as pc #IMPORTANTES CREAR IMAGEN VECTORIAL DE LA CARTA PSICROMETRICA
# pyrefly: ignore [missing-import]
import psychrolib as pb #IMPORTANTES CONTIENE LAS ECUACIONES QUE NECESITAMOS PAR`A CALCULAR LAS PROPIEDADES DEL AIRE
import Funciones
from Clases import Punto
import Interfaz
# pyrefly: ignore [missing-import]
import mplcursors as mpl

#crear carta


ps_card = Funciones.carta_create()

#CREAR INTERFAZ

grafica = Funciones.plano(ps_card) 
simulador = Interfaz.VentanaPrincipal(grafica)




