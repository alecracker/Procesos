# pyrefly: ignore [missing-import]
import psychrolib as pb

pb.SetUnitSystem(pb.SI)

class Punto: #CLase = MOLDE
    
    def __init__(self, nombre,proceso, prop1, prop2, altitud, flujo, tipo_flujo, presion,und1, und2, Tdb, W, RH, Twb, TDp, H, v, den): #INIT es el constructor que nos da las caracteristicas del punto
        
        self.nombre = nombre
        self.proceso = proceso
        self.prop1 = prop1
        self.prop2 = prop2
        self.altitud = altitud
        self.flujo = flujo
        self.tipo_flujo = tipo_flujo
        self.p = presion 
        self.und1 = und1
        self.und2 = und2
        self.Tdb = Tdb #Eje X
        self.W = W #Eje Y
        self.RH = RH
        self.Twb = Twb
        self.TDp = TDp
        self.H = H
        self.v = v
        self.d = den

        
    def dibujo(self, grafica):
        
        marcador = grafica.scatter(self.Tdb, self.W*1000, color = 'black', s = 80, zorder = 100, label = self.nombre)
        return marcador

    def calculo(self,prop1, prop2 , und1, und2):
        if self.proceso == "Mostrar Punto":
            if und1 == "Temperatura de bulbo seco" and und2 == "Humedad relativa" or und1 == "Humedad relativa" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.RH = prop2

                elif und1 == "Humedad relativa":
                    self.RH = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.RH = prop1
                elif und2 == "Humedad relativa":
                    self.RH = prop2
                    self.Tdb = prop1
                self.RH = float(self.RH)
                self.RH = self.RH/100
                self.Tdb = float(self.Tdb)
                #HUmedad absoluta
                self.W = pb.GetHumRatioFromRelHum(self.Tdb, self.RH, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen especifico
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromRelHum(self.Tdb,self.RH)
                #Temperatura de bulbo humedo
                self.Twb = pb.GetTWetBulbFromTDewPoint(self.Tdb,self.TDp, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb,self.W,self.p)
            if und1 == "Temperatura de bulbo seco" and und2 == "Temperatura de bulbo humedo" or und1 == "Temperatura de bulbo humedo" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.Twb = prop2
                elif und1 == "Temperatura de bulbo humedo":
                    self.Twb = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.Twb = prop1
                elif und2 == "Temperatura de bulbo humedo":
                    self.Twb = prop2
                    self.Tdb = prop1
                self.Tdb = float(self.Tdb)
                self.Twb = float(self.Twb)
                #Enfriamiento evaporativo adiatbatico
                #Humedad Relativa
                self.RH = pb.GetRelHumFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Humedad absoluta
                self.W = pb.GetHumRatioFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb, self.W, self.p)
            if und1 == "Temperatura de bulbo seco" and und2 == "Humedad absoluta" or und1 == "Humedad absoluta" and und2 == "Temperatura de bulbo seco":
                
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.W = prop2
                elif und1 == "Humedad absoluta":
                    self.W = prop1
                    self.Tdb = prop2
                elif und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.W = prop1
                elif und2 == "Humedad absoluta":
                    self.W = prop2
                    self.Tdb = prop1
                
                # Convertimos los datos a números decimales
                self.Tdb = float(self.Tdb) 
                # la librería necesita el dato en [kg/kg], por lo que hay que dividirlo entre 1000
                self.W = float(self.W) / 1000.0
                self.RH = pb.GetRelHumFromHumRatio(self.Tdb, self.W, self.p)
                self.TDp = pb.GetTDewPointFromHumRatio(self.Tdb, self.W, self.p)
                self.Twb = pb.GetTWetBulbFromHumRatio(self.Tdb, self.W, self.p)
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                self.d = pb.GetMoistAirDensity(self.Tdb, self.W, self.p)
        #CASO 1: 
        if self.proceso == 'Enfriamiento' or self.proceso == 'Calentamiento':
            if und1 == "Temperatura de bulbo seco" and und2 == "Humedad relativa" or und1 == "Humedad relativa" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.RH = prop2

                elif und1 == "Humedad relativa":
                    self.RH = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.RH = prop1
                elif und2 == "Humedad relativa":
                    self.RH = prop2
                    self.Tdb = prop1
                self.RH = float(self.RH)
                self.RH = self.RH/100
                self.Tdb = float(self.Tdb)
                #HUmedad absoluta
                self.W = pb.GetHumRatioFromRelHum(self.Tdb, self.RH, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen especifico
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromRelHum(self.Tdb,self.RH)
                #Temperatura de bulbo humedo
                self.Twb = pb.GetTWetBulbFromTDewPoint(self.Tdb,self.TDp, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb,self.W,self.p)
            if und1 == "Temperatura de bulbo seco" and und2 == "Temperatura de bulbo humedo" or und1 == "Temperatura de bulbo humedo" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.Twb = prop2
                elif und1 == "Temperatura de bulbo humedo":
                    self.Twb = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.Twb = prop1
                elif und2 == "Temperatura de bulbo humedo":
                    self.Twb = prop2
                    self.Tdb = prop1
                self.Tdb = float(self.Tdb)
                self.Twb = float(self.Twb)
                #Humedad Relativa
                self.RH = pb.GetRelHumFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Humedad absoluta
                self.W = pb.GetHumRatioFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb, self.W, self.p)
            

        #Caso 2
        if self.proceso == 'Mezcla de aire':
            if und1 == "Temperatura de bulbo seco" and und2 == "Humedad relativa" or und1 == "Humedad relativa" and und2 == "Temperatura de bulbo seco":
                
                    if und1 == "Temperatura de bulbo seco":
                        self.Tdb = prop1
                        self.RH = prop2

                    elif und1 == "Humedad relativa":
                        self.RH = prop1
                        self.Tdb = prop2
                    if und2 == "Temperatura de bulbo seco":
                        self.Tdb = prop2
                        self.RH = prop1
                    elif und2 == "Humedad relativa":
                        self.RH = prop2
                        self.Tdb = prop1
                    self.RH = float(self.RH)
                    self.RH = self.RH/100
                    self.Tdb = float(self.Tdb)
                    #HUmedad absoluta
                    self.W = pb.GetHumRatioFromRelHum(self.Tdb, self.RH, self.p)
                    #Entalpia
                    self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)

                    #Volumen especifico
                    self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                    #Punto de rocio
                    self.TDp = pb.GetTDewPointFromRelHum(self.Tdb,self.RH)
                    #Temperatura de bulbo humedo
                    self.Twb = pb.GetTWetBulbFromTDewPoint(self.Tdb,self.TDp, self.p)
                    #Densidad
                    self.d = pb.GetMoistAirDensity(self.Tdb,self.W,self.p)
                    self.H /= 1000 
            if und1 == "Temperatura de bulbo seco" and und2 == "Temperatura de bulbo humedo" or und1 == "Temperatura de bulbo humedo" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.Twb = prop2
                elif und1 == "Temperatura de bulbo humedo":
                    self.Twb = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.Twb = prop1
                elif und2 == "Temperatura de bulbo humedo":
                    self.Twb = prop2
                    self.Tdb = prop1
                self.Tdb = float(self.Tdb)
                self.Twb = float(self.Twb)
                #Humedad Relativa
                self.RH = pb.GetRelHumFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Humedad absoluta
                self.W = pb.GetHumRatioFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb, self.W, self.p)
                self.H /= 1000 
        #CASO 3
        if self.proceso == 'Humidificacion':
            if und1 == "Temperatura de bulbo seco" and und2 == "Humedad relativa" or und1 == "Humedad relativa" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.RH = prop2
                elif und1 == "Humedad relativa":
                    self.RH = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.RH = prop1
                elif und2 == "Humedad relativa":
                    self.RH = prop2
                    self.Tdb = prop1
                self.RH = float(self.RH)
                self.RH = self.RH/100
                self.Tdb = float(self.Tdb)
                #HUmedad absoluta
                self.W = pb.GetHumRatioFromRelHum(self.Tdb, self.RH, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen especifico
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromRelHum(self.Tdb,self.RH)
                #Temperatura de bulbo humedo
                self.Twb = pb.GetTWetBulbFromTDewPoint(self.Tdb,self.TDp, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb,self.W,self.p)
        #CASO 4
        if self.proceso == "Deshumidificacion":
             if und1 == "Temperatura de bulbo seco" and und2 == "Humedad relativa" or und1 == "Humedad relativa" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.RH = prop2
                elif und1 == "Humedad relativa":
                    self.RH = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.RH = prop1
                elif und2 == "Humedad relativa":
                    self.RH = prop2
                    self.Tdb = prop1
                self.RH = float(self.RH)
                self.RH = self.RH/100
                self.Tdb = float(self.Tdb)
                #HUmedad absoluta
                self.W = pb.GetHumRatioFromRelHum(self.Tdb, self.RH, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen especifico
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromRelHum(self.Tdb,self.RH)
                #Temperatura de bulbo humedo
                self.Twb = pb.GetTWetBulbFromTDewPoint(self.Tdb,self.TDp, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb,self.W,self.p)
        #CASO 5
        if self.proceso == " (EE) Enfriamiento Evaporativo":
              if und1 == "Temperatura de bulbo seco" and und2 == "Temperatura de bulbo humedo" or und1 == "Temperatura de bulbo humedo" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.Twb = prop2
                elif und1 == "Temperatura de bulbo humedo":
                    self.Twb = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.Twb = prop1
                elif und2 == "Temperatura de bulbo humedo":
                    self.Twb = prop2
                    self.Tdb = prop1
                self.Tdb = float(self.Tdb)
                self.Twb = float(self.Twb)
                #Enfriamiento evaporativo adiatbatico
                #Humedad Relativa
                self.RH = pb.GetRelHumFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Humedad absoluta
                self.W = pb.GetHumRatioFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromTWetBulb(self.Tdb, self.Twb, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb, self.W, self.p)

              if und1 == "Temperatura de bulbo seco" and und2 == "Humedad relativa" or und1 == "Humedad relativa" and und2 == "Temperatura de bulbo seco":
                if und1 == "Temperatura de bulbo seco":
                    self.Tdb = prop1
                    self.RH = prop2
                elif und1 == "Humedad relativa":
                    self.RH = prop1
                    self.Tdb = prop2
                if und2 == "Temperatura de bulbo seco":
                    self.Tdb = prop2
                    self.RH = prop1
                elif und2 == "Humedad relativa":
                    self.RH = prop2
                    self.Tdb = prop1
                self.RH = float(self.RH)
                self.RH = self.RH/100
                self.Tdb = float(self.Tdb)
                #HUmedad absoluta
                self.W = pb.GetHumRatioFromRelHum(self.Tdb, self.RH, self.p)
                #Entalpia
                self.H = pb.GetMoistAirEnthalpy(self.Tdb, self.W)
                #Volumen especifico
                self.v = pb.GetMoistAirVolume(self.Tdb, self.W, self.p)
                #Punto de rocio
                self.TDp = pb.GetTDewPointFromRelHum(self.Tdb,self.RH)
                #Temperatura de bulbo humedo
                self.Twb = pb.GetTWetBulbFromTDewPoint(self.Tdb,self.TDp, self.p)
                #Densidad
                self.d = pb.GetMoistAirDensity(self.Tdb,self.W,self.p)
        print(self.prop1,self.prop2, self.p, self.W, self.H, self.v, self.TDp, self.Twb, self.d)

            
            
            

        
            
        