from model.modelo import *
from controller.FerramentasFiguras import * 
from dataclasses import dataclass

@dataclass
class Controlador:
    modelo: object 
    visao : object 
    def __comecar__(self):         
        self.ferramentas = {"Linha" : FerramentaCriar(self, Linha), 
                       "Retângulo" : FerramentaCriar(self, Retangulo),
                        "Oval" : FerramentaCriar(self, Retangulo),
                        "Círculo": FerramentaCriar(self, Circulo) }
        
        self.ferramentas = self.ferramentas["Linha"]
        self.rabisco_atual = None
        self.configurar_eventos()
        self.redesenhar()

    def configurar_eventos(self):

        self.visao.tipo_figura.trace_add(
            "write",
            self.mudar_ferramenta
        )

        self.visao.grade.trace_add(
            "write",
            self.atualizar_grade
        )

        self.visao.menu_tamanho.trace_add(
            "write",
            self.mudar_tamanho
        )

        self.visao.btn_limpar.config(
            command=self.limpar
        )

        self.atualizar_eventos()

    def atualizar_eventos(self):

        self.visao.canvas.bind(
            "<ButtonPress-1>",
            self.ferramenta.mouse_pressionado
        )

        self.visao.canvas.bind(
            "<B1-Motion>",
            self.ferramenta.mouse_arrastado
        )

        self.visao.canvas.bind(
            "<ButtonRelease-1>",
            self.ferramenta.mouse_solto
        )
    def mudar_ferramenta(self, *args):

        self.ferramenta = self.ferramentas.get(
            self.visao.tipo_figura.get(),
            self.ferramenta
        )

        self.atualizar_eventos()
    def mudar_tamanho(self, *args):
        tamanho = self.visao.menu_tamanho.get().split()

        self.visao.altura = int(tamanho[0])
        self.visao.largura = int(tamanho[2])

        self.visao.canvas.config(width=self.visao.largura, height=self.visao.altura)
        if self.visao.grade.get() == "Com grade":
            self.exibir_grades()

    def exibir_grades(self):
            linhas = self.modelo.criar_grade(self.visao.largura,self.visao.altura,10)
            for x1, y1, x2, y2 in linhas:
                self.visao.canvas.create_line(x1, y1, x2, y2, fill="lightgray")


         
    def atualizar_grade(self, *args):
        self.redesenhar()

    def redesenhar(self):
        self.visao.canvas.delete("all")

        if self.visao.grade.get() == "Com grade":
            self.exibir_grades()

        for figura in self.modelo.obter_figuras():
            figura.desenhar(self.visao.canvas)

        if len(self.modelo.pontos_poligonos) >= 4:
            self.visao.canvas.create_line(
            self.modelo.pontos_poligonos,
            fill=self.visao.cor_borda.get(),
            width=2
        )

    def limpar(self):
        self.modelo.limpar()
        self.visao.canvas.delete("all")
        if self.visao.grade.get() == "Com grade":
            self.exibir_grades()