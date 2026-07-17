from tkinter import *
from dataclasses import dataclass
from dataclasses import asdict
from tkinter import filedialog
from abc import ABC, abstractmethod
import json
import math

@dataclass
class Figuras(ABC):
    cor_borda : str
    espessura : float
    cor_preenchimento : str 
    @abstractmethod
    def identificar(self,x,y):
        pass
    
    def mover(self, dx,dy):
        self.x1 += dx
        self.y1 += dy
        self.y2 += dy
        self.x2 += dx

@dataclass
class Rabisco(Figuras):
    pontos : list
    def desenhar(self, canvas):
        if len(self.pontos) >= 4:
            canvas.create_line(self.pontos, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self,x,y):
        for i in range(0, len(self.pontos) - 2, 2):

            x1 = self.pontos[i]
            y1 = self.pontos[i + 1]

            x2 = self.pontos[i + 2]
            y2 = self.pontos[i + 3]

            if self.calcular_distancia(x, y, x1, y1, x2, y2):
                return True

    def calcular_distancia(self, x, y, x1, y1, x2, y2):         
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return ((x - x1) ** 2 + (y- y1) ** 2) ** 0.5
        
        t = ((x - x1) * dx + (y - y1) * dy) / (dx ** 2 + dy ** 2)
        t = max(0, min(1, t))

        proj_x = x1 + t * dx
        proj_y = y1 + t * dy

        distancia = (((x - proj_x) ** 2 + (y - proj_y) ** 2)) ** 0.5
        return distancia <= 15
    def mover(self, dx,dy):
        for i in range(0, len(self.pontos), 2):
            self.pontos[i] += dx
            self.pontos[i + 1] += dy
@dataclass
class Linha(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    def desenhar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self,x,y):
        ponto_x, ponto_y = x , y

        vetor_x = self.x2 - self.x1
        vetor_y = self.y2 - self.y1
        
        vetor_px = ponto_x - self.x1 
        vetor_py = ponto_y - self.y1  
        
        comprimento = vetor_x ** 2 + vetor_y ** 2
        if comprimento == 0: 
            return False
        t = (vetor_px * vetor_x + vetor_py * vetor_y) / comprimento
        t = max(0, min(1, t))

        fx = self.x1 + t * vetor_x
        fy = self.y1 + t * vetor_y

        distancia = (((ponto_x - fx) ** 2 + (ponto_y - fy) ** 2)) ** 0.5
        return distancia <= 15

@dataclass
class Retangulo(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    def desenhar(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self,x,y):
        maior_x, menor_x = max(self.x1, self.x2), min(self.x1, self.x2)
        maior_y, menor_y = max(self.y1, self.y2), min(self.y1, self.y2)
        return menor_x <= x <= maior_x and menor_y <= y <= maior_y

@dataclass
class Oval(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    def desenhar(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self,x,y):
        Centro_X = (self.x1 + self.x2)/2
        Centro_Y = (self.y1 + self.y2)/2
        a = (self.x2 - self.x1)/2
        b = (self.y2 - self.y1)/2
        ponto = ((x - Centro_X)**2 / (a ** 2)) + ((y - Centro_Y)**2 / (b ** 2))
        return ponto  <= 1

@dataclass
class Circulo(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    def desenhar(self, canvas):
        self.raio = ((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2 ) ** 0.5
        canvas.create_oval(self.x1 - self.raio, self.y1 - self.raio, self.x1 + self.raio, self.y1 + self.raio, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self,x,y):
        centro_geral = ((x - self.x1)**2 + (y - self.y1)**2)
        return centro_geral <= self.raio**2

@dataclass
class Poligono(Figuras):
    pontos: list
    def desenhar(self, canvas):
        canvas.create_polygon(self.pontos,outline=self.cor_borda,fill=self.cor_preenchimento,width=self.espessura)
    def identificar(self,x,y):
        vertices = [] 
        dentro = False
        
        for i in range(0, len(self.pontos), 2): #Transforma em vertices, porque no nosso caso, são pontos organizados em [x1,y1,x2,y2,x3,y3]
            vertices.append((self.pontos[i], self.pontos[i+1]))

        n = len(vertices)
        if n < 3:
            return False    
        p1x, p1y = vertices[0]
        for i in range(n + 1):
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_interceptado = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro
            p1x, p1y = p2x, p2y
        return dentro
    def mover(self, dx , dy):
        for i in range(0, len(self.pontos), 2):
            self.pontos[i] += dx
            self.pontos[i + 1] += dy
class Modelo:
    def __init__(self):    
        self.figuras = []
        self.pontos_poligonos = []
        
        self.figuras_selecionadas = []
        self.cor_original = None
        self.dx_total = 0
        self.dy_total = 0
        self.inicio_x = 0
        self.inicio_y = 0
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
    
    def salvar_projeto(self):
        if not self.figuras:
                return

        caminho = filedialog.asksaveasfilename(
                defaultextension=".json",
             filetypes=(("Arquivos de Desenho (*.json)", "*.json"), ("Todos os Arquivos", "*.*")),
                title="Escolha onde salvar seu desenho"
            )

        if caminho:
            try:
                lista_convertida = []
                for fig in self.obter_figuras():
                    atributos = asdict(fig) 
                    nome_classe = fig.__class__.__name__
            
                    lista_convertida.append({
                        "tipo_classe": nome_classe,
                        "atributos": atributos
                    })

                with open(caminho, "w", encoding="utf-8") as arquivo:
                    json.dump(lista_convertida, arquivo, indent=4)
                    
            except Exception as erro:
                print("Erro quando ta Salvando o projeto:", erro)

    def abrir_projeto(self):
        caminho = filedialog.askopenfilename(
            filetypes=(("Arquivos de Desenho (*.json)", "*.json"), ("Todos os Arquivos", "*.*")),
            title="Selecione o arquivo do seu desenho"
        )
        
        if caminho:
            try:
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    dados_carregados = json.load(arquivo)
                novas_figuras = []
                classes_permitidas = {
                    "Linha": Linha,
                    "Retangulo": Retangulo,
                    "Oval": Oval,
                    "Circulo": Circulo,
                    "Rabisco": Rabisco,
                    "Poligono": Poligono
                }
        
                for item in dados_carregados:
                    nome_classe = item["tipo_classe"]
                    atributos = item["atributos"]
                    
                    classe_figura = classes_permitidas.get(nome_classe)
                    
                    if classe_figura:
                       
                        objeto_recriado = classe_figura(**atributos)
                        novas_figuras.append(objeto_recriado)
                
                self.figuras = novas_figuras
            except Exception as erro:
                print("Erro quando ta abrindo o projeto:", erro)

    def identificar_figura(self, x, y):
        for figura in reversed(self.figuras):
            if figura.identificar(x, y):
                if figura in self.figuras_selecionadas:
                    self.inicio_x = x
                    self.inicio_y = y
                    self.dx_total = 0
                    self.dy_total = 0
                    return figura
                self.desselecionar()
                self.figuras_selecionadas.append(figura)
                if type(figura).__name__ in ("Linha", "Rabisco"):
                    figura.cor_original = figura.cor_preenchimento
                    figura.cor_preenchimento = "#80ff00"
                else:
                    figura.cor_original = figura.cor_borda
                    figura.cor_borda = "#80ff00"
                self.inicio_x = x
                self.inicio_y = y
                self.dx_total = 0
                self.dy_total = 0
                return figura
        self.desselecionar()
        return None
    
    def mover_figura(self, x,y):
        if not self.figuras_selecionadas:
            return
        else:
            dx = x - self.inicio_x
            dy = y - self.inicio_y
            self.dx_total += dx
            self.dy_total += dy

            for figura in self.figuras_selecionadas:
                figura.mover(dx, dy)
            self.inicio_x = x
            self.inicio_y = y
    def finalizar_movimento(self):
        if not self.figuras_selecionadas:
            return None

        if self.dx_total == 0 and self.dy_total == 0:
            return None

        return (
            "moveu",
            list(self.figuras_selecionadas),
            self.dx_total,
            self.dy_total
        )

    def desselecionar(self):
        for figura in self.figuras_selecionadas:
            if type(figura).__name__ in ("Linha", "Rabisco"):
                figura.cor_preenchimento = figura.cor_original
            else:
                figura.cor_borda = figura.cor_original
            figura.cor_original = None
        self.figuras_selecionadas.clear()
    def atualizar_cor(self, cor_borda, cor_preenchimento):
        if not self.figuras_selecionadas:
            return
        for figura in self.figuras_selecionadas:
            if type(figura).__name__ in ("Linha", "Rabisco"):
                figura.cor_preenchimento = cor_preenchimento
                figura.cor_original = cor_preenchimento
            else:
                figura.cor_borda = cor_borda
                figura.cor_preenchimento = cor_preenchimento
                figura.cor_original = cor_borda

    def identificar_varias(self,x,y):

        for figura in reversed( self.figuras): 
            if figura.identificar(x,y): 
                if figura in self.figuras_selecionadas:
                    self.figuras_selecionadas.remove(figura)
                    if type(figura).__name__ in ("Linha", "Rabisco"):
                        figura.cor_preenchimento = figura.cor_original
                    else:
                        figura.cor_borda = figura.cor_original
                    figura.cor_original = None
                else:
                    self.figuras_selecionadas.append(figura)
                    if type(figura).__name__ in ("Linha", "Rabisco"):
                            figura.cor_original = figura.cor_preenchimento
                            figura.cor_preenchimento = "#80ff00"
                    else:
                            figura.cor_original = figura.cor_borda
                            figura.cor_borda = "#80ff00"
                self.dx_total = 0
                self.dy_total = 0
                self.inicio_x = x 
                self.inicio_y = y
                return figura
        return None 

    def calcular_pontos_poligono(self, cx, cy, mx, my, lados):

        raio = math.hypot(mx - cx, my - cy)
        if raio < 2:
            return []
        angulo_inicial = math.atan2(my - cy, mx - cx)

        pontos = []

        for i in range(lados):
            angulo = angulo_inicial + (2 * math.pi * i) / lados

            x = cx + raio * math.cos(angulo)
            y = cy + raio * math.sin(angulo)

            pontos.append(x)
            pontos.append(y)
        return pontos
