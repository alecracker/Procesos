import Interfaz
import Funciones
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt 
# pyrefly: ignore [missing-import]
import psychrochart as pc
# pyrefly: ignore [missing-import]
import psychrolib as pb
import Funciones
from Clases import Punto
import Interfaz


#crear carta


ps_card = Funciones.carta_create()

#PLANO
grafica = Funciones.plano(ps_card)
Interfaz.crear_interfaz(grafica)




