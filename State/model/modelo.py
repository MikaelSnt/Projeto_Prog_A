from tkinter import *
from dataclasses import dataclass
from dataclasses import asdict
from tkinter import filedialog
import json

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
                pass

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
                
                True
            except Exception as erro:
                return False
        return False 