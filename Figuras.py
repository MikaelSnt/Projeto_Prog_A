from dataclasses import dataclass


@dataclass
class Figuras:
    cor_borda : str
    espessura : float
    cor_preenchimento : str 
    def desenhar(self, canvas):
        raise NotImplementedError(
            "Precisa usar o desenhar()"
        )

@dataclass
class Rabisco(Figuras):
    pontos : list
    
    def desenhar(self, canvas):
        canvas.create_line(self.pontos, fill=self.cor_preenchimento, width=self.espessura)

@dataclass
class Linha(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int

    def desenhar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_preenchimento, width=self.espessura )
    
@dataclass
class Retangulo(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int

    def desenhar(self, canvas):
         canvas.create_rectangle( self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura )

@dataclass
class Oval(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    
    def desenhar(self, canvas):
        canvas.create_oval( self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura )

@dataclass
class Circulo(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int

    def desenhar(self, canvas):
        raio = ((self.x1-self.x2)**2 + (self.y1-self.y2)**2)**0.5
        canvas.create_oval( self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, outline=self.cor_borda,  fill=self.cor_preenchimento,  width=self.espessura)

@dataclass
class Poligono(Figuras):
    pontos: list

    def desenhar(self, canvas):
        canvas.create_polygon(self.pontos, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)

