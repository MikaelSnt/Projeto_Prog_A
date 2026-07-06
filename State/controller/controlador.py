from model.modelo import *
from controller.FerramentasFiguras import * 
from dataclasses import dataclass


@dataclass
class Controlador:
    modelo: object 
    visao : object 
    def __post_init__(self):         
        self.ferramentas = {"Linha" : FerramentaCriar(self,classe_figura= Linha), 
                       "Retângulo" : FerramentaCriar(self, classe_figura = Retangulo),
                        "Oval" : FerramentaCriar(self,classe_figura= Oval),
                        "Círculo": FerramentaCriar(self,classe_figura= Circulo),
                        "Rabisco": FerramentaRabisco(self, classe_figura=Rabisco),
                        "Polígono": FerramentaPoligono(self, classe_figura=Poligono)}
        
        self.ferramenta = self.ferramentas["Rabisco"]
        self.rabisco_atual = None
        self.lista_ults = []
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
        self.visao.bt_abrir.config(command=self.abrir)
        self.visao.bt_salvar.config(command=self.salvar)

        self.visao.btn_limpar.config(
            command=self.limpar
        )
        self.atualizar_eventos()

    def atualizar_eventos(self):
        self.visao.canvas.bind(
            "<Double-Button-1>",
            self.ferramenta.mouse_duplo
            )

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
        self.visao.canvas.bind_all(
            "<Control-z>",
            self.desfazer)
        self.visao.canvas.bind_all(
            "<Control-y>",
            self.refazer)
    def mudar_ferramenta(self, *args):

        self.ferramenta = self.ferramentas.get(self.visao.tipo_figura.get())
        self.atualizar_eventos()

    def mudar_tamanho(self, *args):
        tamanho = self.visao.menu_tamanho.get().split()

        self.visao.altura = int(tamanho[0])
        self.visao.largura = int(tamanho[2])

        self.visao.canvas.config(width=self.visao.largura, height=self.visao.altura)
        if self.visao.grade.get() == "Com grade":
            self.redesenhar()

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
    
    def salvar(self):
        self.modelo.salvar_projeto()
    
    def abrir(self):
        self.modelo.abrir_projeto()
        self.redesenhar()
        
    def desfazer(self,event):
        lista_fig = self.modelo.figuras
        self.ultimo = lista_fig.pop()
        self.lista_ults.append(self.ultimo)
        print(self.lista_ults)
        self.redesenhar()
        
    def refazer(self,event):
        control_y = self.lista_ults.pop()
        print(self.lista_ults)
        self.modelo.figuras.append(control_y)
        self.redesenhar()