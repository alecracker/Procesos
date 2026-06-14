import psychrolib as pb

pb.SetUnitSystem(pb.SI)

class Punto:
    
    def __init__(self, nombre, Tdb, W, RH, Twb, TDp, H, v):
        
        self.nombre = nombre
        self.Tdb = Tdb #Eje X
        self.W = W #Eje Y
        self.RH = RH
        self.Twb = Twb
        self.TDp = TDp
        self.H = H
        self.v = v
        
    def dibujo(self, grafica):

        grafica.scatter(self.Tdb, self.W, color = 'black', s = 80, zorder = 100, label = self.nombre)

        