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
                        "Polígono": FerramentaPoligono(self, classe_figura=Poligono),
                        "Polígono regular":FerramentaPoligonoRegular(self, classe_figura= Poligono)}
        
        self.ferramenta = self.ferramentas["Rabisco"]
        self.rabisco_atual = None
        self.figuras_copiadas = []
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
        
        self.visao.canvas.bind(
            "<ButtonPress-3>",
            self.aumentar_lado
        )
        self.visao.canvas.bind(
            "<Control-Button-1>",
            self.mouse_ctrl)
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
        self.visao.bt_agrupar.config(
            command=self.Agrupar
        )
    def mouse_pressionado(self, event):
        self.ferramenta.mouse_pressionado(event)

    def mouse_arrastado(self, event):
        self.ferramenta.mouse_arrastado(event)

    def mouse_solto(self, event):
        self.ferramenta.mouse_solto(event)

    def mouse_duplo(self, event):
        self.ferramenta.mouse_duplo(event)
    def mouse_ctrl(self,event):
        self.ferramenta.mouse_ctrl(event)
    def aumentar_lado(self,event):
        self.ferramenta.aumentar_lado()
    
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
    def Agrupar(self):
        self.modelo.agrupar_figuras()
        self.redesenhar()
    def copiar(self, *args):

        if not self.modelo.figuras_selecionadas:
            return
        self.figuras_copiadas = copy.deepcopy(
            self.modelo.figuras_selecionadas
    )
    def colar(self, *args):
        if not self.figuras_copiadas:
            return
        
        novas = copy.deepcopy(self.figuras_copiadas)
        
        for figura in novas:
            figura.mover(20,20)
            self.modelo.adicionar_figura(figura)
            self.historico.append(("desenho", figura))
        
        self.lista_refazer.clear()
        self.redesenhar()
    def cima(self,*args):
        self.figura_selecionadas = self.modelo.figuras_selecionadas
        for figura in self.figura_selecionadas:
            indice = self.modelo.figuras.index(figura)
            self.modelo.figuras.pop(indice)
            self.modelo.figuras.insert(indice+1,figura)
        self.redesenhar()

    def cima_total(self,*args):
        self.figuras_selecionadas = self.modelo.figuras_selecionadas
        self.ordem = []
        for figura in self.figuras_selecionadas:
            i = self.modelo.figuras.index(figura)
            self.modelo.figuras.remove(figura)
            self.ordem.append((i,figura))
        self.ordem.sort(key=lambda a: a[0])
        for figura in self.ordem:
            self.modelo.figuras.append(figura[1])
        self.redesenhar()

    def Baixo(self,*args):
        self.figura_selecionadas = self.modelo.figuras_selecionadas
        for figura in self.figura_selecionadas:
            indice = self.modelo.figuras.index(figura)
            self.modelo.figuras.pop(indice)
            self.modelo.figuras.insert(indice-1,figura)
        self.redesenhar()

    def Baixo_total(self,*args):
        self.figuras_selecionadas = self.modelo.figuras_selecionadas
        self.ordem = []
        for figura in self.figuras_selecionadas:
            i = self.modelo.figuras.index(figura)
            self.modelo.figuras.remove(figura)
            self.ordem.append((i,figura))
        self.ordem.sort(key=lambda a: a[0])
        for figura in reversed(self.ordem):
            self.modelo.figuras.insert(0, figura[1])
        self.redesenhar()

    def apagar(self,*args):
        apagados = []
        for figura in self.modelo.figuras_selecionadas:
            self.modelo.figuras.remove(figura)
            apagados.append(figura)
        self.lista_refazer.clear()
        self.historico.append(("apagado",apagados))

        self.redesenhar()
        
    def desfazer(self,*args):
        if not self.historico:
            return

        historico = self.historico.pop()
        ultima_acao = historico[0]
        if ultima_acao == "moveu":
            figuras = historico[1]
            dx = historico[2]
            dy = historico[3]
           
            for figura in figuras:
                figura.mover(-dx, -dy)
         
        elif ultima_acao == "apagado":
            figura = historico[1]
            self.modelo.figuras.extend(figura)
            

        elif ultima_acao == "desenho":
            figura  = historico[1]
            if figura in self.modelo.obter_figuras():
                self.modelo.figuras.remove(figura)
        self.lista_refazer.append(historico)    
        self.redesenhar()

    def refazer(self, *args):
        if not self.lista_refazer:
            return

        historico = self.lista_refazer.pop()
        ultima_acao = historico[0]

        if ultima_acao == "desenho":
            figura = historico[1]
            self.modelo.figuras.append(figura)

        elif ultima_acao == "apagado":
            figuras = historico[1]
            for figura in figuras:
                if figura in self.modelo.obter_figuras():
                    self.modelo.figuras.remove(figura)

        elif ultima_acao == "moveu":
            figuras = historico[1]
            dx = historico[2]
            dy = historico[3]

            for figura in figuras:
                figura.mover(dx, dy)

        self.historico.append(historico)
        self.redesenhar()
       

