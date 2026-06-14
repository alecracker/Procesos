import psychrochart as pc
import matplotlib.pyplot as plt


def carta_create():

    #Creacion de carta
    carta = pc.PsychroChart.create()

    #Parametros de la carta
    carta.config.limits.range_temp_c = (-10.0,55.0)
    carta.config.limits.range_humidity_g_kg = (0,33.0)
    carta.config.saturation.linewidth = 1
    carta.config.constant_wet_temp.color = "darkblue"
    carta.config.chart_params.constant_humid_label_step = 1
    carta.config.chart_params.with_constant_h = True
    carta.config.chart_params.constant_h_step = 5
    carta.config.chart_params.constant_h_labels = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55,  60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115 ]
    carta.config.constant_h.color = "red"
    carta.config.chart_params.constant_h_labels_loc = -0.068

    return carta



def habilitar_zoom_scroll(ax, factor_zoom=1.2):

    margen_x_min, margen_x_max = ax.get_xlim()
    margen_y_min, margen_y_max = ax.get_ylim()
     
    #Evento captura el evento del mouse
    def zoom(evento):
        print("¡La computadora sintió el ratón! Giraste hacia:", evento.button)
        if evento.xdata is None or evento.ydata is None: return #Ver si el cursor esta dentro de la grafica
        
        #Ver hacia donde gira el scroll y opera segun a donde vaya
        if evento.button == 'up': escala = 1 / factor_zoom
        elif evento.button == 'down': escala = factor_zoom
        else: return

        #Obtenemos los limites actuales de la grafica(ax)
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        #Establecemos los nuevos limites
        nuevo_x_min = evento.xdata - (evento.xdata - x_min) * escala
        nuevo_x_max = evento.xdata + (x_max - evento.xdata) * escala
        nuevo_y_min = evento.ydata - (evento.ydata - y_min) * escala
        nuevo_y_max = evento.ydata + (y_max - evento.ydata) * escala

        #Actualizamos/Seteamos los limites de la grafica
        
        if margen_x_max - margen_x_min < nuevo_x_max - nuevo_x_min:
            print("Limite de zoom alcanzado")
        elif margen_y_max - margen_y_min < nuevo_y_max - nuevo_y_min:
            print("Limite de zoom alcanzado")
        else:
            eje_x = nuevo_x_max - nuevo_x_min
            eje_y = nuevo_y_max - nuevo_y_min
        #Evitar salidas del plano (Eje X)
            if nuevo_x_min < margen_x_min:
                nuevo_x_min = margen_x_min
                nuevo_x_max = margen_x_min + eje_x
            elif nuevo_x_max > margen_x_max:
                nuevo_x_max = margen_x_max
                nuevo_x_min = margen_x_max - eje_x
            #Evitar slidas del plano (EJe Y)
            if nuevo_y_min < margen_y_min:
                nuevo_y_min = margen_y_min
                nuevo_y_max = margen_y_min + eje_y
            elif nuevo_y_max > margen_y_max:
                nuevo_y_max = margen_y_max
                nuevo_y_min = margen_y_max - eje_y

            ax.set_xlim([nuevo_x_min, nuevo_x_max])
            ax.set_ylim([nuevo_y_min, nuevo_y_max])
        
        #Redibuja la grafica
        ax.figure.canvas.draw()
        plt.pause(0.01)
        


    ax.figure.canvas.mpl_connect('scroll_event', zoom)

    memoria = {"x_anterior": None, "y_anterior": None}

    def move(evento):
        
       if evento.xdata == None or evento.ydata == None:
            #print("Cursor fuera de la grafica")
            return
       #captura del click
       elif evento.button == 1:
            #Probando
            #print(evento.xdata, evento.ydata)
            #Guardando datos en memoria
            if memoria["x_anterior"] is None:
                memoria["x_anterior"] = evento.xdata
                memoria["y_anterior"] = evento.ydata


            distancia_x = evento.xdata - memoria["x_anterior"]
            distancia_y = evento.ydata - memoria["y_anterior"]

            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()

            eje_x = x_max - x_min
            eje_y = y_max - y_min
            
            nuevo_x_min = x_min - distancia_x
            nuevo_x_max = x_max - distancia_x

            nuevo_y_min = y_min - distancia_y
            nuevo_y_max = y_max - distancia_y
            #Evitar salidas del plano (Eje X)
            if nuevo_x_min < margen_x_min:
                nuevo_x_min = margen_x_min
                nuevo_x_max = margen_x_min + eje_x
            elif nuevo_x_max > margen_x_max:
                nuevo_x_max = margen_x_max
                nuevo_x_min = margen_x_max - eje_x
            #Evitar slidas del plano (EJe Y)
            if nuevo_y_min < margen_y_min:
                nuevo_y_min = margen_y_min
                nuevo_y_max = margen_y_min + eje_y
            elif nuevo_y_max > margen_y_max:
                nuevo_y_max = margen_y_max
                nuevo_y_min = margen_y_max - eje_y
            
            
            ax.set_xlim([nuevo_x_min, nuevo_x_max])
            ax.set_ylim([nuevo_y_min, nuevo_y_max])

            ax.figure.canvas.draw_idle()
            plt.pause(0.01)
       else:
            memoria["x_anterior"] = None
            memoria["y_anterior"] = None

    ax.figure.canvas.mpl_connect('motion_notify_event', move)

def linea2(punto1,punto2):
    lineX2 = [punto1.Tdb, punto2.Tdb]
    lineY2 = [punto1.W, punto2.W]

    plt.plot(lineX2,lineY2)
    return

def linea3(punto1, punto2, punto3):
    

     lineVX = [punto1.Tdb, punto2.Tdb, punto3.Tdb]
     lineVY = [punto1.W, punto2.W, punto3.W]

     plt.plot(lineVX,lineVY)

     return 
    
def plano(card):

    #Creacion de plano
    fig, ax = plt.subplots()
    card.plot(ax=ax)
     # Punto
    
    habilitar_zoom_scroll(ax)
    
   
    #MOdificacion de parametros del plano
    for texto in ax.texts:
    
        if "kJ/kg" in texto.get_text():
            texto.set_rotation(-19)
    
        # Aumentamos los márgenes a 15% (0.15) abajo y a la derecha
    
    fig.savefig("Carta.svg")

    return ax



