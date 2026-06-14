from Funciones import linea2
from os import path
import tkinter as tk
from Clases import Punto
from tkinter import ttk
import Funciones
import matplotlib.pyplot as plt

puntos_guardados = {}

def crear_interfaz(grafica):
    

    ventana = tk.Tk()
    ventana.tk.call("source", "Forest-ttk-theme/forest-light.tcl")
    estilo = ttk.Style(ventana)
    estilo.theme_use("forest-light")
    frame_izquierdo = ttk.Frame(ventana)
    frame_derecho = ttk.Frame(ventana)

    #Titulo

    etiqueta_titulo = ttk.Label(ventana, text="Software de Procesos Psicrometricos", font=("Arial", 20, "bold"), foreground="black")
   

    #DEfinicion de caso

    etiqueta_def_caso = ttk.Label(ventana, text="Definición de Caso", font=("Arial", 16, "bold"), foreground="black")
    

    #etiquetas y cajas de texto
    var_proceso = tk.StringVar()
    etiqueta_proceso = ttk.Label(ventana, text = "Selección de proceso:")
    procesos = ["Mostrar Punto", "Calentamiento", "Enfriamiento", "Deshumidificacion", " (EE) Enfriamiento Evaporativo", "Humidificacion", "Mezcla de aire" ]
    lista_procesos = ttk.Combobox(ventana, values=procesos, textvariable = var_proceso, state="readonly")
    lista_procesos.current(0)
    

    #PROPIEDADES

    var_propiedades_1 = tk.StringVar()
    etiqueta_prop_iniciales = ttk.Label(frame_izquierdo, text = "Propiedades Iniciales")
    lista_propiedades = ["Temperatura de bulbo seco", "Temperatura de bulbo humedo", "Humedad relativa", "Entalpia", "Volumen especifico", "Humedad absoluta"]
    etiqueta_prop_1 = ttk.Label(frame_izquierdo, text="Propiedad 1:")
    Prop_1 = ttk.Combobox(frame_izquierdo, values=lista_propiedades, state="r", textvariable = var_propiedades_1)
    Prop_1.current(0)
    Prop_1_text = ttk.Entry(frame_izquierdo) 
   
    var_propiedades_2 = tk.StringVar()
    etiqueta_prop_2 = ttk.Label(frame_izquierdo, text = "Propiedad 2:")
    Prop_2 = ttk.Combobox(frame_izquierdo, values=lista_propiedades, state="r", textvariable = var_propiedades_2)
    Prop_2.current(0)
    Prop_2_text = ttk.Entry(frame_izquierdo)
  

    #CONDICIONES
    
    etiqueta_Cond_defectos = ttk.Label(frame_izquierdo, text = "Condiciones por Defecto:")
    altitud_bool = tk.BooleanVar()
    flujo_air_bool = tk.BooleanVar()
    presion_bool = tk.BooleanVar()
    altitud_var = tk.StringVar()
    flujo_var = tk.StringVar()
    presion_var = tk.StringVar()
    altitud_check = ttk.Checkbutton(frame_izquierdo, text="Altitud", variable=altitud_bool)
    altitud_text = ttk.Entry(frame_izquierdo, textvariable = altitud_var)
    flujo_check = ttk.Checkbutton(frame_izquierdo, text="Flujo de Aire", variable=flujo_air_bool)
    flujo_text = ttk.Entry(frame_izquierdo, textvariable = flujo_var)
    presion_check = ttk.Checkbutton(frame_izquierdo, text="Presion del Sistema", variable=presion_bool)
    presion_text = ttk.Entry(frame_izquierdo, textvariable = presion_var)
    traza_text = ttk.Label(frame_izquierdo, text="Armar trazo")
    
    def traza_2_puntos(punto1, punto2):
        
        
            linea2(punto1,punto2)
            print("Traza de 2 puntos")
    
    def traza_3_puntos(punto1, punto2, punto3):
        Funciones.linea3(punto1, punto2, punto3)
        print("Traza de 3 puntos")
        
    def accion_añadir():

        proceso_elegido = var_proceso.get()
        nombre_P = Nm_punto.get()
        if nombre_P == "":
            print("punto sin nombre")

        if altitud_bool.get() == True or presion_bool.get() == True:
            datos_punto = {

                "prop_ini_1" : Prop_1_text.get(),
                "prop_ini_2" : Prop_2_text.get(),
                "Altitud" : altitud_text.get(),
                "Flujo" : flujo_text.get(),
                "Presion" : presion_text.get(),
                "Und_1" : Prop_1.get(),
                "Und_2" : Prop_2.get()
        
            }
            punto_graf = Punto(nombre_P, datos_punto["prop_ini_1"], datos_punto["prop_ini_2"], datos_punto["Altitud"], datos_punto["Flujo"], datos_punto["Presion"], 0, 0, datos_punto["Und_1"], datos_punto["Und_2"])
            
        elif flujo_air_bool.get() == True and altitud_bool.get() == False and presion_bool.get() == False:
            datos_punto = {

                "prop_ini_1" : Prop_1_text.get(),
                "prop_ini_2" : Prop_2_text.get(),
                "Altitud" : altitud_text.get(),
                "Flujo" : flujo_text.get(),
                "Presion" : presion_text.get(),
                "Und_1" : Prop_1.get(),
                "Und_2" : Prop_2.get()
            } 
            punto_graf = Punto(nombre_P, datos_punto["prop_ini_1"], datos_punto["prop_ini_2"], datos_punto["Altitud"], datos_punto["Flujo"], datos_punto["Presion"], 0, 0, datos_punto["Und_1"], datos_punto["Und_2"]   )
        else:

            datos_punto = {

                "prop_ini_1" : Prop_1_text.get(),
                "prop_ini_2" : Prop_2_text.get(),
                "Altitud" : 0,
                "Flujo" : 1000,
                "Presion" : 101325,
                "Und_1" : Prop_1.get(),
                "Und_2" : Prop_2.get()

            }
            punto_graf = Punto(nombre_P, float(datos_punto["prop_ini_1"]), float(datos_punto["prop_ini_2"]), float(datos_punto["Altitud"]), float(datos_punto["Flujo"]), float(datos_punto["Presion"]), 0, 0, datos_punto["Und_1"], datos_punto["Und_2"])
            
        
        puntos_guardados[nombre_P] = punto_graf    
        punto_graf.dibujo(grafica)
        print(f"Punto añadido: {nombre_P} {datos_punto}")
        
        
        
    
    def accion_editar():

        proceso_elegido = var_proceso.get()
        print(f"Editando: {proceso_elegido} ")
    
    def accion_limpiar():

        lista_procesos.current(0)
        altitud_var.set("") 
        flujo_var.set("")
        presion_var.set("") 
        Prop_1.current(0)
        Prop_2.current(0)
        print(f"limpiado ")   
    
    def enlistar_puntos():
                
        lista_puntos = list(puntos_guardados.values())
        if len(lista_puntos) == 2:
            traza_2_puntos(lista_puntos[0], lista_puntos[1])
        elif len(lista_puntos) == 3:
            traza_3_puntos(lista_puntos[0], lista_puntos[1], lista_puntos[2])   
        elif len(lista_puntos) == 1:
            print("No hay suficientes puntos para trazar")
        

    def accion_simular():

        proceso_elegido = var_proceso.get()
        print(f"Simulando: {proceso_elegido} ")   
        
        manager = plt.get_current_fig_manager()

        for nombre, punto in puntos_guardados.items():
            punto.dibujo(grafica)
    
        ventana.destroy()
        plt.tight_layout()
        
        plt.show()
    
  
        
        

    #BOTONES

    boton_añadir = ttk.Button(frame_izquierdo, text="Añadir Punto", command = accion_añadir)
   
    boton_Editar = ttk.Button(frame_izquierdo, text="Editar Punto", command = accion_editar)

    boton_resetear = ttk.Button(frame_izquierdo, text="Limpiar Campos", command= accion_limpiar)

    boton_simular = ttk.Button(frame_izquierdo, text="Simular", command = accion_simular)
    
    boton_trazo = ttk.Button(frame_izquierdo, text = "Trazo", command= enlistar_puntos)
    
    

    #Direcciones

    #DIreccion ETIQUETAS
    
    etiqueta_proceso.grid(row = 3, column = 0, pady = 0, padx = 10, sticky="e")
    etiqueta_prop_iniciales.grid(row = 1, column = 2, columnspan = 2, pady=10)
    etiqueta_prop_2.grid(row = 4, column = 2, pady = 2)
    etiqueta_prop_1.grid(row = 2, column = 2, pady=2)
    etiqueta_def_caso.grid(row = 1, column = 0, columnspan = 2, pady=2)
    etiqueta_titulo.grid(row=0, column=0, columnspan=10, pady=2)
    etiqueta_Cond_defectos.grid(row=5, column= 0, columnspan = 2,  pady=2)
    
    
    #Direccion cajas y listas

    lista_procesos.grid(row=3, column=1,  pady = 5, padx = 10, sticky="w")
    Prop_1.grid(row=2, column=3, pady=5, padx = 10)
    Prop_1_text.grid(row=3, column=3,  pady=5, padx = 10)
    altitud_text.grid(row=6, column=1,  pady=10, padx = 10, sticky="w")
    flujo_text.grid(row=7, column=1,  pady=10, padx = 10, sticky="w")
    presion_text.grid(row=8, column=1, pady=10, padx = 10, sticky="w")
    Prop_2.grid(row = 4, column= 3, pady = 10, padx = 10)
    Prop_2_text.grid(row = 5, column = 3,  pady = 10, padx = 10)
   

    #DIRECCION CHESCKS


    altitud_check.grid(column=0, row = 6, pady=5, padx = 2, sticky="e")
    flujo_check.grid(column=0, row = 7, pady=10, padx = 2, sticky="e")
    presion_check.grid(column=0, row = 8, pady=10, padx = 2, sticky="e")
    

    #DIRECCION BOTONES
    
    boton_trazo.grid(column=3, row = 7, pady=10, padx = 2)
    boton_añadir.grid(column=0, row = 10, pady=10, padx = 10)
    boton_resetear.grid(column=1, row = 10, pady=10, padx = 10)
    boton_Editar.grid(column=2, row = 10, pady=10, padx = 10)
    boton_simular.grid(column=3, row = 10, pady=10, padx = 10)
    
    #ENTRY PARA GUARDAR EL NUMERO DEL PUNTO

    etiqueta_punto = ttk.Label(frame_izquierdo, text="Nombre del Punto:")
    etiqueta_punto.grid(column=0, row = 4, pady=2, sticky="e")
    Nm_punto = ttk.Entry(frame_izquierdo)
    Nm_punto.grid(column=1, row = 4, pady=5, padx=5, sticky="w")


    #FRAMES

    frame_izquierdo.grid(row=0,column=1,padx=10,pady=10,sticky="n")
    frame_derecho.grid(row = 0, column=1, padx = 10, pady = 10, sticky="n")

    #Ventana
    ventana.title("Simulador Psicometrico")
    ventana.state("zoomed")
    
    ventana.mainloop()
    
    
    
    return

