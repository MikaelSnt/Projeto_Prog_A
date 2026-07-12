from model.modelo import *
from controller.FerramentasFiguras import * 
from dataclasses import dataclass
import copy as copy

@dataclass
class Controlador:
    modelo: object 
    visao : object 
    def __post_init__(self):         
        self.ferramentas = {"Seleção" : FerramentaSelecao(self),
                        "Linha" : FerramentaSimples(self,classe_figura= Linha), 
                       "Retângulo" : FerramentaSimples(self, classe_figura = Retangulo),
                        "Oval" : FerramentaSimples(self,classe_figura= Oval),
                        "Círculo": FerramentaSimples(self,classe_figura= Circulo),
                        "Rabisco": FerramentaRabisco(self, classe_figura=Rabisco),
                        "Polígono": FerramentaPoligono(self, classe_figura=Poligono)}
        
        self.ferramenta = self.ferramentas["Rabisco"]
        self.rabisco_atual = None
        self.lista_refazer = []
        self.lista_apagados = []
        self.historico = []
        self.configurar_eventos()
        self.redesenhar()
        self.visao.canvas.bind(
            "<Double-Button-1>",
            self.mouse_duplo
        )
        self.visao.canvas.bind(
            "<ButtonPress-1>",
            self.mouse_pressionado
        )

        self.visao.canvas.bind(
            "<B1-Motion>",
            self.mouse_arrastado
        )

        self.visao.canvas.bind(
            "<ButtonRelease-1>",
            self.mouse_solto
        )
                
        self.visao.canvas.bind_all(
            "<Control-z>",
            self.desfazer)
        
        self.visao.canvas.bind_all(
            "<Control-y>",
            self.refazer)
        self.visao.canvas.bind_all(
            "<Control-c>", self.copiar
        )
        self.visao.canvas.bind_all(
            "<Control-v>", self.colar
        )
        self.visao.canvas.bind_all(
            "<Delete>", self.apagar
        )
        self.visao.canvas.bind_all(
            "<Right>", self.cima
        )
        self.visao.canvas.bind_all(
            "<Left>", self.Baixo
        )
        self.visao.canvas.bind_all(
            "<Up>", self.cima_total
        )
        self.visao.canvas.bind_all(
            "<Down>", self.Baixo_total
        )
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
        self.visao.cor_preenchimento.trace_add(
            "write",
            self.atualizar_cor_selecao
        )
        self.visao.cor_borda.trace_add(
            "write",
            self.atualizar_cor_selecao
        )
        self.visao.bt_abrir.config(
            command=self.abrir
            )
        self.visao.bt_salvar.config(
            command=self.salvar
        )

        self.visao.btn_limpar.config(
            command=self.limpar
        )
    def mouse_pressionado(self, event):
        self.ferramenta.mouse_pressionado(event)

    def mouse_arrastado(self, event):
        self.ferramenta.mouse_arrastado(event)

    def mouse_solto(self, event):
        self.ferramenta.mouse_solto(event)

    def mouse_duplo(self, event):
        self.ferramenta.mouse_duplo(event)

    def mudar_ferramenta(self, *args):

        self.ferramenta = self.ferramentas.get(self.visao.tipo_figura.get())

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
            width=self.visao.espessura.get()
        )

    def limpar(self):
        self.modelo.limpar()
        self.visao.canvas.delete("all")
        if self.visao.grade.get() == "Com grade":
            self.exibir_grades()

    def atualizar_cor_selecao(self, *args):
        self.modelo.atualizar_cor(self.visao.cor_borda.get(), self.visao.cor_preenchimento.get())
        self.redesenhar()

    def salvar(self):
        self.modelo.salvar_projeto()
    
    def abrir(self):
        if self.modelo.abrir_projeto():
            self.redesenhar()

    def copiar(self, *agrs):
        if self.modelo.figura_selecionada is None:
            return

        if self.modelo.figura_selecionada:
            self.figura_copiada = copy.deepcopy(self.modelo.figura_selecionada)
        if type(self.figura_copiada).__name__ in ("Linha", "Rabisco"):
            self.figura_copiada.cor_preenchimento = self.modelo.cor_original
        else:
            self.figura_copiada.cor_borda = self.modelo.cor_original
    def colar(self, *args):
        if self.figura_copiada:
            nova_fig = copy.deepcopy(self.figura_copiada)

            self.modelo.adicionar_figura(nova_fig)
            self.lista_refazer.clear()
            self.historico.append(("desenho", nova_fig))
            self.redesenhar()
    def cima(self,*args):
        self.figura_selecionada = self.modelo.figura_selecionada
        i = self.modelo.figuras.index(self.figura_selecionada)
        figura = self.modelo.figuras.pop(i)
        self.modelo.figuras.insert(i+1,figura)
        self.redesenhar()

    def cima_total(self,*args):
        self.figura_selecionada = self.modelo.figura_selecionada
        self.modelo.figuras.remove(self.figura_selecionada)
        self.modelo.figuras.append(self.figura_selecionada)
        self.redesenhar()

    def Baixo(self,*args):
        self.figura_selecionada = self.modelo.figura_selecionada
        i = self.modelo.figuras.index(self.figura_selecionada)
        figura = self.modelo.figuras.pop(i)
        self.modelo.figuras.insert(i-1,figura)
        self.redesenhar()

    def Baixo_total(self,*args):
        self.figura_selecionada = self.modelo.figura_selecionada
        self.modelo.figuras.remove(self.figura_selecionada)
        self.modelo.figuras.insert(0,self.figura_selecionada)
        self.redesenhar()

    def apagar(self,*args):
        figura = self.modelo.figura_selecionada

        if figura is None:
            return
        
        self.modelo.figuras.remove(figura)
        self.lista_refazer.clear()
        self.historico.append(("apagado", figura))

        self.redesenhar()
        
    def desfazer(self,*args):
        if not self.historico:
            return

        historico = self.historico.pop()
        ultima_acao = historico[0]
        
        if ultima_acao == "moveu":
            figura = historico[1]
            dx = historico[2]
            dy = historico[3]
            figura.mover(-dx,-dy)
         
        
        elif ultima_acao == "apagado":
            figura = historico[1]
            self.modelo.figuras.append(figura)
            

        elif ultima_acao == "desenho":
            figura  = historico[1]
            if figura in self.modelo.obter_figuras():
                self.modelo.figuras.remove(figura)
        self.lista_refazer.append(historico)    
        self.redesenhar()

    def refazer(self, *agrs):
        if not self.lista_refazer:
            return
        
        historico = self.lista_refazer.pop()
        ultima_acao = historico[0]
        
        if ultima_acao == "desenho":
            figura = historico[1]
            self.modelo.figuras.append(figura)
        
        elif ultima_acao == "apagado":
            figura = historico[1]
            if figura in self.modelo.obter_figuras():
                self.modelo.figuras.remove(figura)
        
        elif ultima_acao == "moveu":
            figura = historico[1]
            dx = historico[2]
            dy = historico[3]
            figura.mover(dx, dy)

        self.historico.append(historico)
        self.redesenhar()