from tkinter import *
from dataclasses import dataclass

@dataclass
class Figuras:
        cor_borda : str
        espessura : float
        cor_preenchimento : str 


@dataclass
class Rabisco(Figuras):
        pontos : list
        def desenhar(self, canvas):
            if len(self.pontos) >= 4:
                canvas.create_line(self.pontos, fill=self.cor_preenchimento, width=self.espessura)

@dataclass
class Linha(Figuras):
        x1 : int
        y1 : int
        x2 : int
        y2 : int
        def desenhar(self, canvas):
            canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_preenchimento, width=self.espessura)
    
@dataclass
class Retangulo(Figuras):
        x1 : int
        y1 : int
        x2 : int
        y2 : int
        def desenhar(self, canvas):
            canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)

@dataclass
class Oval(Figuras):
        x1 : int
        y1 : int
        x2 : int
        y2 : int
        def desenhar(self, canvas):
            canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)

@dataclass
class Circulo(Figuras):
        x1 : int
        y1 : int
        x2 : int
        y2 : int
        def desenhar(self, canvas):
            raio = ((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2 ) ** 0.5
            canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)

@dataclass
class Poligono(Figuras):
        pontos: list
        def desenhar(self, canvas):
            canvas.create_polygon(self.pontos,outline=self.cor_borda,fill=self.cor_preenchimento,width=self.espessura)
class Modelo:
    def __init__(self):    
        self.figuras = []
        self.pontos_poligonos = []

    def criar_figuras(self, tipo, cor_borda, espessura, cor_preenchimento, x1, y1, x2, y2, rabisco = None):
        figura = None

        if tipo == "Rabisco":
            if rabisco and len(rabisco) >= 4:
                figura = Rabisco(cor_borda, espessura, cor_preenchimento, rabisco )

        elif tipo == "Linha":
            figura = Linha(cor_borda, espessura, cor_preenchimento, x1 , y1, x2, y2)

        elif tipo == "Retângulo":
            figura = Retangulo( cor_borda, espessura, cor_preenchimento,x1 , y1, x2, y2)

        elif tipo == "Oval":
            figura = Oval(cor_borda, espessura, cor_preenchimento, x1 , y1, x2, y2)
            
        elif tipo == "Círculo":
            figura = Circulo(cor_borda, espessura, cor_preenchimento,x1 , y1, x2, y2)
        
        if figura:
            self.figuras.append(figura)

        return figura 
    
    def adicionar_figura(self, figura):
        self.figuras.append(figura)        

    def obter_figuras(self):
        return self.figuras

    def limpar(self):
        self.figuras.clear()
        self.pontos_poligonos.clear()
    def criar_grade(self, largura, altura, tamanho):
        linhas = []

        for x in range(0, largura, tamanho):
            linhas.append((x, 0, x, altura))

        for y in range(0, altura, tamanho):
            linhas.append((0, y, largura, y))

        return linhas