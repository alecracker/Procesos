
from tkinter.messagebox import showerror
from tkinter import messagebox
import Funciones
from Funciones import linea2
from os import path
import tkinter as tk
from Clases import Punto
from tkinter import ttk
import Funciones
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
# pyrefly: ignore [missing-import]
import psychrolib as pb
# pyrefly: ignore [missing-import]
import mplcursors as mpl 
from tkinter import messagebox as msg

puntos_guardados = {}


class VentanaPrincipal:


    def __init__(self,ps_card):
        self.ps_card = ps_card 
        self.ventana = tk.Tk()
        self.ventana.tk.call("source", "Forest-ttk-theme/forest-light.tcl")
        estilo = ttk.Style(self.ventana)
        estilo.theme_use("forest-light")
        self.frame_izquierdo = ttk.Frame(self.ventana)
        self.frame_derecho = ttk.Frame(self.ventana)
        self.puntos_guardados = {}


        
        # Titulo
        self.etiqueta_titulo = ttk.Label(self.frame_izquierdo, text="Software de Procesos Psicrométricos", font=("Arial", 20, "bold"), foreground="black")

        # Definicion de caso
        self.etiqueta_def_caso = ttk.Label(self.frame_izquierdo, text="Definición de Caso", font=("Arial", 16, "bold"), foreground="black")

        # etiquetas y cajas de texto
        self.var_proceso = tk.StringVar()
        self.etiqueta_proceso = ttk.Label(self.frame_izquierdo, text="Selección de proceso:")
        procesos = ["Mostrar Punto", "Calentamiento", "Enfriamiento", "Deshumidificacion", " (EE) Enfriamiento Evaporativo", "Humidificacion", "Mezcla de aire" ]
        self.lista_procesos = ttk.Combobox(self.frame_izquierdo, values=procesos, textvariable=self.var_proceso, state="readonly")
        self.proc_seleccionado = self.lista_procesos.bind("<<ComboboxSelected>>", lambda event: self.lista_procesos.get())
        self.unidad_prop1 = ttk.Label(self.frame_izquierdo, text="", width=5, foreground="black", font=("Segoe UI", 9, "bold"))
        self.unidad_prop2 = ttk.Label(self.frame_izquierdo, text="", width=5, foreground="black", font=("Segoe UI", 9, "bold"))

        # PROPIEDADES
        self.var_propiedades_1 = tk.StringVar()
        self.etiqueta_prop_iniciales = ttk.Label(self.frame_izquierdo, text="Propiedades Iniciales")
        lista_propiedades = ["Temperatura de bulbo seco", "Temperatura de bulbo humedo", "Humedad relativa", "Humedad absoluta"]
        self.etiqueta_prop_1 = ttk.Label(self.frame_izquierdo, text="Propiedad 1:")
        self.unidad_flujo = ttk.Label(
                                    self.frame_izquierdo, 
                                    text="[m³/h]", 
                                    width=6, 
                                    foreground="black", 
                                    font=("Segoe UI", 9, "bold")
                                )
        self.unidad_flujo.grid(row=7, column=3, sticky="w")


        self.Prop_1 = ttk.Combobox(self.frame_izquierdo, values=lista_propiedades, state="r", textvariable=self.var_propiedades_1)
        self.Prop_1.current(0)
        self.Prop_1_text = ttk.Entry(self.frame_izquierdo) 

        self.var_propiedades_2 = tk.StringVar()
        self.etiqueta_prop_2 = ttk.Label(self.frame_izquierdo, text="Propiedad 2:")
        self.Prop_2 = ttk.Combobox(self.frame_izquierdo, values=lista_propiedades, state="r", textvariable=self.var_propiedades_2)
        self.Prop_2.current(0)
        self.Prop_2_text = ttk.Entry(self.frame_izquierdo)
        self.Prop_1.bind("<<ComboboxSelected>>", self.actualizar_unidades)
        self.Prop_2.bind("<<ComboboxSelected>>", self.actualizar_unidades)
        self.unidad_altitud = ttk.Label(
            self.frame_izquierdo, 
            text="[m]", 
            width=5, 
            foreground="black", 
            font=("Segoe UI", 9, "bold")
        )
        self.unidad_presion = ttk.Label(
        self.frame_izquierdo, 
        text="[Pa]", 
        width=5, 
        foreground="Black", 
        font=("Segoe UI", 9, "bold")
        )
        self.Prop_1.bind("<<ComboboxSelected>>", self.actualizar_unidades)
        self.Prop_2.bind("<<ComboboxSelected>>", self.actualizar_unidades)
        

        # CONDICIONES
        self.etiqueta_Cond_defectos = ttk.Label(self.frame_izquierdo, text="Condiciones por Defecto:")
        self.altitud_bool = tk.BooleanVar(self.ventana)
        self.flujo_bool = tk.BooleanVar(self.ventana)
        self.presion_bool = tk.BooleanVar(self.ventana)
        self.altitud_var = tk.StringVar(self.ventana)
        self.tipo_flujo_var = tk.StringVar(self.ventana)
        self.flujo_var = tk.StringVar(self.ventana)
        self.presion_var = tk.StringVar(self.ventana)
        self.altitud_var.set(0)
        self.tipo_flujo_var.set("Flujo volumetrico")
        self.flujo_var.set(1000)
        self.presion_var.set(101325)
        
        self.altitud_check = ttk.Checkbutton(self.frame_izquierdo, text="Altitud", variable=self.altitud_bool)
        self.altitud_text = ttk.Entry(self.frame_izquierdo, textvariable=self.altitud_var)
        self.flujo_check = ttk.Checkbutton(self.frame_izquierdo, text="Flujo:", variable=self.flujo_bool)
        self.tipo_flujo_combo = ttk.Combobox(self.frame_izquierdo, values=["Flujo volumetrico", "Flujo masico"], textvariable=self.tipo_flujo_var, state="readonly", width=16)
        self.flujo_text = ttk.Entry(self.frame_izquierdo, textvariable=self.flujo_var, width=10)
        self.presion_check = ttk.Checkbutton(self.frame_izquierdo, text="Presión del Sistema", variable=self.presion_bool)
        self.presion_text = ttk.Entry(self.frame_izquierdo, textvariable=self.presion_var)
        self.traza_text = ttk.Label(self.frame_izquierdo, text="Armar trazo")
        self.tipo_flujo_combo.bind("<<ComboboxSelected>>", self.actualizar_unidad_flujo)
        # ENTRY PARA GUARDAR EL NUMERO DEL PUNTO
        self.etiqueta_punto = ttk.Label(self.frame_izquierdo, text="Nombre del Punto:")
        self.etiqueta_punto.grid(column=0, row=4, pady=2, sticky="e")
        self.Nm_punto = ttk.Entry(self.frame_izquierdo)
        self.Nm_punto.grid(column=1, row=4, pady=5, padx=5, sticky="w")

        # BOTONES
        self.boton_añadir = ttk.Button(self.frame_izquierdo, text="Añadir Punto", command=self.accion_añadir)
        self.boton_Editar = ttk.Button(self.frame_izquierdo, text="Editar Punto", command=self.accion_editar)
        self.boton_resetear = ttk.Button(self.frame_izquierdo, text="Limpiar Campos", command=self.accion_limpiar)
        self.boton_simular = ttk.Button(self.frame_izquierdo, text="Simular", command=self.accion_simular)
        self.boton_trazo = ttk.Button(self.frame_izquierdo, text="Trazo", command=self.accion_trazo)


        # Direcciones ETIQUETAS
        self.etiqueta_proceso.grid(row=3, column=0, pady=0, padx=10, sticky="e")
        self.etiqueta_prop_iniciales.grid(row=1, column=2, columnspan=2, pady=10)
        self.etiqueta_prop_2.grid(row=4, column=2, pady=2)
        self.etiqueta_prop_1.grid(row=2, column=2, pady=2)
        self.etiqueta_def_caso.grid(row=1, column=0, columnspan=2, pady=2)
        self.etiqueta_titulo.grid(row=0, column=0, columnspan=10, pady=2)
        self.etiqueta_Cond_defectos.grid(row=5, column=0, columnspan=2, pady=2)
        self.unidad_altitud.grid(row=6, column=2, sticky="w")
        self.unidad_presion.grid(row=8, column=2, sticky="w")
        self.unidad_prop1.grid(row=3, column=4, sticky="w")
        self.unidad_prop2.grid(row=5, column=4, sticky="w")


        # Direccion cajas y listas
        self.lista_procesos.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        self.Prop_1.grid(row=2, column=3, pady=5, padx=10)
        self.Prop_1_text.grid(row=3, column=3, pady=5, padx=10)
        self.altitud_text.grid(row=6, column=1, pady=10, padx=10, sticky="w")
        self.tipo_flujo_combo.grid(row=7, column=1, pady=10, padx=10, sticky="w")
        self.flujo_text.grid(row=7, column=2, pady=10, padx=10, sticky="w")
        self.presion_text.grid(row=8, column=1, pady=10, padx=10, sticky="w")
        self.Prop_2.grid(row=4, column=3, pady=10, padx=10)
        self.Prop_2_text.grid(row=5, column=3, pady=10, padx=10)

        # DIRECCION CHESCKS
        self.altitud_check.grid(column=0, row=6, pady=5, padx=2, sticky="w")
        self.flujo_check.grid(column=0, row=7, pady=10, padx=2, sticky="w")
        self.presion_check.grid(column=0, row=8, pady=10, padx=2, sticky="w")

        # DIRECCION BOTONES
        self.boton_trazo.grid(column=3, row=8, pady=10, padx=2)
        self.boton_añadir.grid(column=0, row=10, pady=10, padx=10)
        self.boton_resetear.grid(column=1, row=10, pady=10, padx=10)
        self.boton_Editar.grid(column=2, row=10, pady=10, padx=10)
        self.boton_simular.grid(column=3, row=10, pady=10, padx=10)

        # FRAMES
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # FRAME DERECHO (Caja de información)
        self.caja_info = tk.Text(
            self.frame_derecho, 
            font=("Consolas", 11),  
            bg="#f8f9fa",           
            fg="#2c3e50",           
            padx=20, pady=20,       
            relief="flat"           
        )
        
        # Hacemos que la caja cubra TODO el frame derecho (nsew)
        self.caja_info.grid(row=0, column=0, sticky="nsew")
        
        # --- EL TRUCO DE LA EXPANSIÓN ---
        # 1. Le decimos al frame derecho que expanda la caja por dentro
        self.frame_derecho.grid_rowconfigure(0, weight=1)
        self.frame_derecho.grid_columnconfigure(0, weight=1)
        
        # 2. Le decimos a la ventana principal que todo el espacio sobrante se lo regale al lado derecho (columna 1)
        self.ventana.grid_rowconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=1)



        # Ventana
        self.ventana.title("Simulador Psicometrico")
        self.ventana.state("zoomed")
        self.actualizar_unidades(None)
        self.actualizar_unidad_flujo(None)
        self.ventana.mainloop()


    def traza_2_puntos(self,punto1, punto2):
            
            
        linea2(punto1,punto2)
        print("Traza de 2 puntos")
        
    def traza_3_puntos(self,punto1, punto2, punto3):
            Funciones.linea3(punto1, punto2, punto3)
            print("Traza de 3 puntos")
            
    def accion_añadir(self):

        proceso_elegido = self.var_proceso.get()
        nombre_P = self.Nm_punto.get()
        if nombre_P == "":
            msg.showwarning("Cuidado", "El punto guardado no tiene nombre")
        
                
        if len(self.puntos_guardados) >= 1:
            
            primer_punto = list(self.puntos_guardados.values())[0]
            
            # Comparacion de procesos
            if primer_punto.proceso != self.lista_procesos.get():
                msg.showerror("Error", f"No puedes cambiar el proceso a mitad de camino. Empezaste simulando un '{primer_punto.proceso}'.")
                return

        altitud = 0
        flujo = 1000
        presion = 101325

        if self.flujo_bool.get() == True and self.flujo_text.get() != "":

            flujo = self.flujo_text.get()
           
                
        
        if self.altitud_bool.get() == True and self.altitud_text.get() != "":

            altitud = self.altitud_text.get()
            
                
        if self.presion_bool.get() == True and self.presion_text.get() != "":
            
            presion = self.presion_text.get()
        
               # 1. Validar que no estén vacíos
        if self.Prop_1_text.get() == "" or self.Prop_2_text.get() == "":
            msg.showwarning("Cuidado", "El punto guardado no tiene propiedades")
            return
        
        # 2. Try/Except para validar que sí sean números y no letras
        try:
            float(self.Prop_1_text.get())
            float(self.Prop_2_text.get())
        except ValueError:
            msg.showerror("Error", "¡Debes ingresar solo números en las propiedades!")
            return
        
        # 3. Validar que sí hayan seleccionado Bulbo Seco en alguna de las dos listas
        if self.Prop_1.get() != "Temperatura de bulbo seco" and self.Prop_2.get() != "Temperatura de bulbo seco":
            msg.showerror("Error", "Las propiedades no son correctas (Se necesita la Temperatura de bulbo seco)")
            return
        
        elif self.Prop_1.get() == "Temperatura de bulbo seco" and self.Prop_2.get() == "Temperatura de bulbo seco":
            msg.showerror("Error", "No puedes seleccionar 'Temperatura de bulbo seco' en ambas casillas.")
            return
        # 4. Validar que seleccionaron un proceso
        if self.lista_procesos.get() == "":
            msg.showwarning("Cuidado", "El punto guardado no tiene proceso")
            return

        datos_punto = {
                "proceso" : self.lista_procesos.get(),

                "prop_ini_1" : self.Prop_1_text.get(), 
                
                "prop_ini_2" : self.Prop_2_text.get(), 
                
                "Altitud" : altitud,
                
                "Flujo" : flujo,
                "Tipo_flujo" : self.tipo_flujo_var.get(),
                
                "Presion" : presion,
                
                "Und_1" : self.Prop_1.get(), 
                
                "Und_2" : self.Prop_2.get()
        }
        
        self.punto_acal = Punto(nombre_P,datos_punto['proceso'], float(datos_punto["prop_ini_1"]), float(datos_punto["prop_ini_2"]), float(datos_punto["Altitud"]), float(datos_punto["Flujo"]), datos_punto["Tipo_flujo"], float(datos_punto["Presion"]), datos_punto["Und_1"], datos_punto["Und_2"], 0 , 0, 0, 0, 0, 0,0,0)
        # 2. Hace el cálculo internamente
                
        try:
            self.punto_acal.calculo(datos_punto["prop_ini_1"],datos_punto["prop_ini_2"], datos_punto["Und_1"], datos_punto["Und_2"] )
            
            # Validación manual: Que no se salga de los límites visuales de tu carta gráfica
            if self.punto_acal.Tdb < -10 or self.punto_acal.Tdb > 55 or self.punto_acal.W < 0 or self.punto_acal.W > 0.033:
                msg.showerror("Fuera de rango", "El punto se sale de los límites de la carta psicrométrica (-10 a 55 °C, o Humedad mayor a 33 g/kg).")
                return
                
        except Exception:
            # Si psychrolib colapsa porque la matemática no cuadra (Ej. Bulbo Húmedo > Seco)
            msg.showerror("Error Termodinámico", "Los valores ingresados son físicamente imposibles de calcular.")
            return
             
        # 3. Guardamos el objeto REAL en el diccionario 
        self.puntos_guardados[nombre_P] = self.punto_acal  

               
        

        print(f"Punto añadido: {nombre_P} {datos_punto}")
                # Formato de tarjeta limpia y profesional para la bitácora
        mensaje_bonito = (
            f"✅ PUNTO AÑADIDO: [ {nombre_P} ]\n"
            f"{'-'*55}\n"
            f"🌡️ Propiedades:\n"
            f"   • {datos_punto['Und_1']}: {datos_punto['prop_ini_1']}\n"
            f"   • {datos_punto['Und_2']}: {datos_punto['prop_ini_2']}\n\n"
            f"⚙️ Condiciones del Sistema:\n"
            f"   • Flujo: {datos_punto['Flujo']} ({datos_punto['Tipo_flujo']})\n"
            f"   • Presión: {datos_punto['Presion']} Pa\n"
            f"{'='*55}\n\n"
        )
        self.caja_info.insert(tk.END, mensaje_bonito)

        
                
        if self.lista_procesos.get() == "Enfriamiento" or self.lista_procesos.get() == "Calentamiento":
            
            
            if len(self.puntos_guardados) == 1:
                msg.showinfo("Aviso de Termodinámica", "En los procesos de enfriamiento y calentamiento sensible, el contenido de humedad absoluta (W) no varía. Por lo tanto, se tomará como constante, de manera que para añadir el segundo punto solo se considera la temperatura de bulbo seco y se va directamente a la opción de simular.")

       
        
        
    def accion_editar(self):
        nombre_P = self.Nm_punto.get()
        
        
        if nombre_P == "":
            msg.showwarning("Cuidado", "Ingresa el nombre del punto que quieres editar.")
            return
            
        if nombre_P not in self.puntos_guardados:
            msg.showerror("Error", f"El punto '{nombre_P}' no existe. Usa 'Añadir Punto' para crearlo primero.")
            return
            
        # Validar que las propiedades no estén vacías
        if self.Prop_1_text.get() == "" or self.Prop_2_text.get() == "":
            msg.showwarning("Cuidado", "Faltan propiedades para editar el punto.")
            return
            
        # Validar que sí sean números
        try:
            float(self.Prop_1_text.get())
            float(self.Prop_2_text.get())
        except ValueError:
            msg.showerror("Error", "¡Debes ingresar solo números en las propiedades!")
            return
            
        # Validar que tengan Bulbo Seco seleccionado
        if self.Prop_1.get() != "Temperatura de bulbo seco" and self.Prop_2.get() != "Temperatura de bulbo seco":
            msg.showerror("Error", "Las propiedades no son correctas (Se necesita la Temperatura de bulbo seco)")
            return

        # Recoger datos de condiciones (Altitud, Flujo, Presión)
        altitud = self.altitud_text.get() if (self.altitud_bool.get() and self.altitud_text.get() != "") else 0
        flujo = self.flujo_text.get() if (self.flujo_bool.get() and self.flujo_text.get() != "") else 1000
        presion = self.presion_text.get() if (self.presion_bool.get() and self.presion_text.get() != "") else 101325
            
        # Para evitar que el usuario cambie de proceso al editar, mantenemos el proceso original
        proceso_original = self.puntos_guardados[nombre_P].proceso
        
        # Creamos el punto editado
        punto_editado = Punto(
            nombre_P, proceso_original, 
            float(self.Prop_1_text.get()), float(self.Prop_2_text.get()), 
            float(altitud), float(flujo), self.tipo_flujo_var.get(), float(presion), 
            self.Prop_1.get(), self.Prop_2.get(), 
            0, 0, 0, 0, 0, 0, 0, 0
        )
        
        
        punto_editado.calculo(self.Prop_1_text.get(), self.Prop_2_text.get(), self.Prop_1.get(), self.Prop_2.get())
        
        
        self.puntos_guardados[nombre_P] = punto_editado
        
        
        msg.showinfo("Éxito", f"El punto '{nombre_P}' se ha actualizado correctamente.")
        self.caja_info.insert(tk.END, f"Punto EDITADO: {nombre_P} | Prop_1: {self.Prop_1_text.get()} {self.Prop_1.get()} | Prop_2: {self.Prop_2_text.get()} {self.Prop_2.get()}\n")

        
    def accion_limpiar(self):

        
        self.Nm_punto.delete(0, tk.END)
        self.Prop_1_text.delete(0, tk.END)
        self.Prop_2_text.delete(0, tk.END)
        self.caja_info.delete('1.0', tk.END)
        self.puntos_guardados.clear()
        self.lista_procesos.current(0)
        self.altitud_var.set("") 
        self.tipo_flujo_var.set("Flujo volumetrico")
        self.flujo_var.set("")
        self.presion_var.set("") 
        self.Prop_1.current(0)
        self.Prop_2.current(0)
        msg.showinfo("Limpiado", "Se ha limpiado los campos")  
   

    def enlistar_puntos(self):
                    
        lista_puntos = list(self.puntos_guardados.values())
            
            
        return lista_puntos
    def accion_trazo(self):
        # 1. Traer los puntos guardados
        self.lista_puntos = self.enlistar_puntos()
        
        # 2. Validar que haya suficientes puntos
        if len(self.lista_puntos) < 2:
            msg.showwarning("Atención", "¡Necesitas al menos 2 puntos guardados para armar un trazo!")
            return

        # 3. Limpiar y crear lienzo nuevo (igual que en la simulación)
        plt.close('all')
        self.grafica = Funciones.plano(self.ps_card)
        dibujos_puntos = []

        # 4. Dibujar las bolitas (puntos)
        for nombre, punto in self.puntos_guardados.items():
            marcador = punto.dibujo(self.grafica)
            marcador.datos_psicrometricos = punto
            dibujos_puntos.append(marcador)
            
        # 5. Conectar los puntos con líneas
        if len(self.lista_puntos) == 2:
            self.traza_2_puntos(self.lista_puntos[0], self.lista_puntos[1])
        elif len(self.lista_puntos) >= 3:
            self.traza_3_puntos(self.lista_puntos[0], self.lista_puntos[1], self.lista_puntos[2])

        # 6. Activar interacciones y mostrar
        Funciones.activar_hover(dibujos_puntos)
        plt.tight_layout()
        plt.show()

    
    def actualizar_unidades(self, event=None):
        # Nuestro diccionario "traductor" de unidades
        diccionario_unidades = {
            "Temperatura de bulbo seco": "[°C]",
            "Humedad relativa": "[%]",
            "Temperatura de bulbo humedo": "[°C]",
            "Humedad absoluta": "[g/kg]"
        }
        
        
        seleccion_1 = self.Prop_1.get()
        seleccion_2 = self.Prop_2.get()
        
   
        self.unidad_prop1.config(text=diccionario_unidades.get(seleccion_1, ""))
        self.unidad_prop2.config(text=diccionario_unidades.get(seleccion_2, ""))

    def actualizar_unidad_flujo(self, event=None):
        seleccion = self.tipo_flujo_combo.get()
        
        if seleccion == "Flujo volumetrico":
            self.unidad_flujo.config(text="[m³/h]") # (O usa m³/s si en tus fórmulas calculas por segundo)
        elif seleccion == "Flujo masico":
            self.unidad_flujo.config(text="[kg/min]") # (O kg/s)

    def accion_simular(self):

        dibujos_puntos = [] #Guarda ubicaciones
        proceso_elegido = self.lista_procesos.get()
        print(f"Simulando: {proceso_elegido} ") 
        self.lista_puntos = self.enlistar_puntos()
        if proceso_elegido == "Enfriamiento" or proceso_elegido == "Calentamiento":

           
            if len(self.lista_puntos) != 2:
                msg.showwerror("Los enfriamientos y calentamientos utilizan 2 puntos")
                return  
            elif len(self.lista_puntos) == 2:
              
                self.lista_puntos[1].W = self.lista_puntos[0].W
                self.lista_puntos[1].RH = pb.GetRelHumFromHumRatio(self.lista_puntos[1].Tdb, self.lista_puntos[1].W, self.lista_puntos[1].p)
                    
                #Entalpia
                self.lista_puntos[1].H = pb.GetMoistAirEnthalpy(self.lista_puntos[1].Tdb, self.lista_puntos[1].W)
                #Volumen especifico
                self.lista_puntos[1].v = pb.GetMoistAirVolume(self.lista_puntos[1].Tdb, self.lista_puntos[1].W, self.lista_puntos[1].p)
                #Punto de rocio
                self.lista_puntos[1].TDp = pb.GetTDewPointFromRelHum(self.lista_puntos[1].Tdb,self.lista_puntos[1].RH)
                #Temperatura de bulbo humedo
                self.lista_puntos[1].Twb = pb.GetTWetBulbFromTDewPoint(self.lista_puntos[1].Tdb,self.lista_puntos[1].TDp, self.lista_puntos[1].p)
                #Densidad
                self.lista_puntos[1].d = pb.GetMoistAirDensity(self.lista_puntos[1].Tdb,self.lista_puntos[1].W,self.lista_puntos[1].p)
                self.lista_puntos[1].H = self.lista_puntos[1].H / 1000
                    
                
                print(self.lista_puntos[0].Tdb,self.lista_puntos[0].W,self.lista_puntos[0].RH,self.lista_puntos[0].Twb,self.lista_puntos[0].TDp,self.lista_puntos[0].H/1000,self.lista_puntos[0].v,self.lista_puntos[0].d)
                print(self.lista_puntos[1].Tdb,self.lista_puntos[1].W,self.lista_puntos[1].RH,self.lista_puntos[1].Twb,self.lista_puntos[1].TDp,self.lista_puntos[1].H,self.lista_puntos[1].v,self.lista_puntos[1].d)
        if proceso_elegido == "Humidificacion":
                  
            if len(self.lista_puntos) != 2:
                msg.showerror("Error", "Las humidificaciones utilizan 2 puntos")
                return 
                    
           
            print(self.lista_puntos[0].Tdb,self.lista_puntos[0].W,self.lista_puntos[0].RH,self.lista_puntos[0].Twb,self.lista_puntos[0].TDp,self.lista_puntos[0].H/1000,self.lista_puntos[0].v,self.lista_puntos[0].d)
            print(self.lista_puntos[1].Tdb,self.lista_puntos[1].W,self.lista_puntos[1].RH,self.lista_puntos[1].Twb,self.lista_puntos[1].TDp,self.lista_puntos[1].H/1000,self.lista_puntos[1].v,self.lista_puntos[1].d)

        if proceso_elegido == "Deshumidificacion":

            if len(self.lista_puntos) != 2:
                messagebox.showerror("Error" , "Las deshumidificaciones utilizan 2 puntos")
                return 
            
            
            print(self.lista_puntos[0].Tdb,self.lista_puntos[0].W,self.lista_puntos[0].RH,self.lista_puntos[0].Twb,self.lista_puntos[0].TDp,self.lista_puntos[0].H/1000,self.lista_puntos[0].v,self.lista_puntos[0].d)
            print(self.lista_puntos[1].Tdb,self.lista_puntos[1].W,self.lista_puntos[1].RH,self.lista_puntos[1].Twb,self.lista_puntos[1].TDp,self.lista_puntos[1].H/1000,self.lista_puntos[1].v,self.lista_puntos[1].d)

        if proceso_elegido == " (EE) Enfriamiento Evaporativo":

            if len(self.lista_puntos) != 2:
                msg.showerror("Error","Las enfriamientos evaporativos utilizan 2 puntos")
                return 

            self.lista_puntos[1].H = self.lista_puntos[0].H
            
            self.lista_puntos[1].W = pb.GetHumRatioFromTWetBulb(self.lista_puntos[1].Tdb, self.lista_puntos[1].Twb, self.lista_puntos[1].p)
            #Punto de rocio
            self.lista_puntos[1].TDp = pb.GetTDewPointFromTWetBulb(self.lista_puntos[1].Tdb, self.lista_puntos[1].Twb, self.lista_puntos[1].p)
            #Entalpia
            self.lista_puntos[1].H = pb.GetMoistAirEnthalpy(self.lista_puntos[1].Tdb, self.lista_puntos[1].W)
            #Volumen
            self.lista_puntos[1].v = pb.GetMoistAirVolume(self.lista_puntos[1].Tdb, self.lista_puntos[1].W, self.lista_puntos[1].p)
            #Densidad
            self.lista_puntos[1].d = pb.GetMoistAirDensity(self.lista_puntos[1].Tdb, self.lista_puntos[1].W, self.lista_puntos[1].p)
            
           
            print(self.lista_puntos[0].Tdb ,self.lista_puntos[0].W,self.lista_puntos[0].RH,self.lista_puntos[0].Twb,self.lista_puntos[0].TDp,self.lista_puntos[0].H/1000,self.lista_puntos[0].v,self.lista_puntos[0].d)
            print(self.lista_puntos[1].Tdb,self.lista_puntos[1].W,self.lista_puntos[1].RH,self.lista_puntos[1].Twb,self.lista_puntos[1].TDp,self.lista_puntos[1].H/1000,self.lista_puntos[1].v,self.lista_puntos[1].d)

        if proceso_elegido == "Mezcla de aire":

            if len(self.lista_puntos) != 2:
                msg.showerror("Error","Las mezclas utilizan 2 puntos")
                return 
            p1 = self.lista_puntos[0]
            p2 = self.lista_puntos[1]

            if p1.tipo_flujo == "Flujo masico" and p2.tipo_flujo == "Flujo masico":
                flujo_masico_p1 = p1.flujo 
                flujo_masico_p2 = p2.flujo 

                flujo_masico_total = flujo_masico_p1 + flujo_masico_p2
                
                H3 = (p1.H * flujo_masico_p1 + p2.H * flujo_masico_p2) / flujo_masico_total
                W3 = (p1.W * flujo_masico_p1 + p2.W * flujo_masico_p2) / flujo_masico_total

                T3 = pb.GetTDryBulbFromEnthalpyAndHumRatio(H3 * 1000 , W3)
                RH3 = pb.GetRelHumFromHumRatio(T3, W3, p1.p)
                TDp3 = pb.GetTDewPointFromRelHum(T3, RH3)
                Twb3 = pb.GetTWetBulbFromTDewPoint(T3, TDp3, p1.p)
                v3 = pb.GetMoistAirVolume(T3, W3, p1.p)
                d3 = pb.GetMoistAirDensity(T3, W3, p1.p)

            
                nuevo_punto = Punto(
                    "Punto Mezcla",     # nombre
                    "Mezcla de aire",   # proceso
                    0,                  # prop1
                    0,                  # prop2
                    0,                  # altitud
                    p1.flujo + p2.flujo,# flujo (opcional, la suma de los volúmenes)
                    "Flujo masico",     # tipo_flujo
                    p1.p,               # presion
                    "",                 # und1
                    "",                 # und2
                    T3,                 # Tdb
                    W3,                 # W
                    RH3,                # RH
                    Twb3,               # Twb
                    TDp3,               # TDp
                    H3,                 # H
                    v3,                 # v
                    d3                  # den (d3)
                )

                self.lista_puntos.append(nuevo_punto)

                self.puntos_guardados["Punto Mezcla"] = self.lista_puntos[2]
               
                
                # Ventana emergente de resultados
            
                humedad_total = flujo_masico_total * W3 * 3600 # kg/h
                msg.showinfo("Resultados de Mezcla", f"Flujo Másico Total: {flujo_masico_total:.2f} kg/min")
                
            elif p1.tipo_flujo == "Flujo volumetrico" and p2.tipo_flujo == "Flujo volumetrico":
                # Convertir flujo volumétrico a flujo másico dividiendo entre volumen específico
                flujo_masico_p1 = p1.flujo / p1.v
                flujo_masico_p2 = p2.flujo / p2.v

                flujo_masico_total = flujo_masico_p1 + flujo_masico_p2
                
                H3 = (p1.H * flujo_masico_p1 + p2.H * flujo_masico_p2) / flujo_masico_total
                W3 = (p1.W * flujo_masico_p1 + p2.W * flujo_masico_p2) / flujo_masico_total

                T3 = pb.GetTDryBulbFromEnthalpyAndHumRatio(H3 * 1000 , W3)
                RH3 = pb.GetRelHumFromHumRatio(T3, W3, p1.p)
                TDp3 = pb.GetTDewPointFromRelHum(T3, RH3)
                Twb3 = pb.GetTWetBulbFromTDewPoint(T3, TDp3, p1.p)
                v3 = pb.GetMoistAirVolume(T3, W3, p1.p)
                d3 = pb.GetMoistAirDensity(T3, W3, p1.p)
                
                flujo_vol_total = flujo_masico_total * v3
            
                nuevo_punto = Punto(
                    "Punto Mezcla",     
                    "Mezcla de aire",   
                    0,                  
                    0,                  
                    0,                  
                    flujo_vol_total,
                    "Flujo volumetrico",
                    p1.p,               
                    "",                 
                    "",                 
                    T3,                 
                    W3,                 
                    RH3,                
                    Twb3,               
                    TDp3,               
                    H3,                 
                    v3,                 
                    d3                  
                )

                self.lista_puntos.append(nuevo_punto)

                self.puntos_guardados["Punto Mezcla"] = self.lista_puntos[2]
                
                
                # Ventana emergente con resultados
            
                humedad_total = flujo_masico_total * W3 * 3600
                msg.showinfo("Resultados de Mezcla", f"Flujo Volumétrico Total: {flujo_vol_total:.2f} m³/s\nHumedad Total: {humedad_total:.2f} kg/h")
            
        plt.close('all') # Cierra ventanas viejas de matplotlib
        self.grafica = Funciones.plano(self.ps_card) # Dibuja una carta nuevecita

        
        
        for nombre, punto in self.puntos_guardados.items():
            marcador = punto.dibujo(self.grafica)
            
            marcador.datos_psicrometricos = punto
            dibujos_puntos.append(marcador)
        

        Funciones.activar_hover(dibujos_puntos)
        #self.ventana.destroy()
        plt.tight_layout()
            
        plt.show()
