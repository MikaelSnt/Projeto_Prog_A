from tkinter import *
from dataclasses import dataclass
from dataclasses import asdict
from tkinter import filedialog
from abc import ABC, abstractmethod
import json

@dataclass
class Figuras(ABC):
    cor_borda : str
    espessura : float
    cor_preenchimento : str 
    @abstractmethod
    def identificar(self,event):
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
    def identificar(self, event):
        pass
    def mover(self, event):
        pass
@dataclass
class Linha(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    def desenhar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self, event):
        ponto_x, ponto_y = event.x , event.y

        vetor_x = self.x2 - self.x1
        vetor_y = self.y2 - self.y1
        
        vetor_px = ponto_x - self.x1 
        vetor_py = ponto_y - self.y1  
        
        comprimento = vetor_x ** 2 + vetor_y ** 2
        if comprimento == 0: 
            return False
        t = (vetor_px * vetor_x + vetor_py * vetor_y) / comprimento
        t = max(0, min(1, t))

        x = self.x1 + t * vetor_x
        y = self.y1 + t * vetor_y

        distancia = (((ponto_x - x) ** 2 + (ponto_y - y) ** 2)) ** 0.5
        return distancia <= 15

@dataclass
class Retangulo(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    def desenhar(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self, event):
        maior_x, menor_x = max(self.x1, self.x2), min(self.x1, self.x2)
        maior_y, menor_y = max(self.y1, self.y2), min(self.y1, self.y2)
        return menor_x <= event.x <= maior_x and menor_y <= event.y <= maior_y

@dataclass
class Oval(Figuras):
    x1 : int
    y1 : int
    x2 : int
    y2 : int
    def desenhar(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)
    def identificar(self, event):
        Centro_X = (self.x1 + self.x2)/2
        Centro_Y = (self.y1 + self.y2)/2
        a = (self.x2 - self.x1)/2
        b = (self.y2 - self.y1)/2
        ponto = ((event.x - Centro_X)**2 / (a ** 2)) + ((event.y - Centro_Y)**2 / (b ** 2))
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
    def identificar(self, event):
        centro_geral = ((event.x - self.x1)**2 + (event.y - self.y1)**2)
        return centro_geral <= self.raio**2

@dataclass
class Poligono(Figuras):
    pontos: list
    def desenhar(self, canvas):
        canvas.create_polygon(self.pontos,outline=self.cor_borda,fill=self.cor_preenchimento,width=self.espessura)
    def identificar(self, event):
        x = event.x
        y = event.y
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
       