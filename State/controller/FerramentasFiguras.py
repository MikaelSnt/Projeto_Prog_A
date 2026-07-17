from dataclasses import dataclass
import math
@dataclass
class Ferramenta():
    controlador : object
    inicio_X: int = 0
    inicio_Y: int = 0
    figura: object = None
    figura_selecionada = None
    def mouse_pressionado(self, event):
        pass
    def mouse_arrastado(self, event):
        pass
    def mouse_solto(self, event):
        pass
    def criar_figura(self, x1, y1, x2 , y2):
        pass
    def mouse_duplo(self, event):
        pass
    def aumentar_lado(self):
        pass
    def diminuir_lado(self):
        pass

@dataclass
class FerramentaSimples(Ferramenta):
    classe_figura : type = None 
    def mouse_pressionado(self, event):
        self.inicio_X = event.x
        self.inicio_Y = event.y

    def mouse_arrastado(self, event):
        self.figura = self.criar_figura(self.inicio_X, self.inicio_Y, event.x, event.y)
        self.controlador.redesenhar()
        if self.figura:
            self.figura.desenhar(self.controlador.visao.canvas)

    def mouse_solto(self, event):
        if self.figura:
            figura = self.figura
            self.controlador.modelo.adicionar_figura(figura)
            self.controlador.redesenhar()
            self.controlador.historico.append(("desenho", figura))
            self.figura = None
    def criar_figura(self, x1, y1, x2, y2):

            return self.classe_figura(
            self.controlador.visao.cor_borda.get(),
            self.controlador.visao.espessura.get(),
            self.controlador.visao.cor_preenchimento.get(),
            x1,
            y1,
            x2,
            y2
            )
@dataclass
class FerramentaRabisco(Ferramenta):
    classe_figura: type = None
    def mouse_pressionado(self, event):
        self.controlador.rabisco_atual = [event.x, event.y]   
    def mouse_arrastado(self, event):
            self.controlador.rabisco_atual.extend([event.x, event.y])
            self.figura = self.criar_figura_rabisco(self.controlador.rabisco_atual)
            self.controlador.redesenhar()
            if self.figura:
                self.figura.desenhar(self.controlador.visao.canvas)
    def mouse_solto(self, event):
        if self.figura:
            figura = self.figura

            self.controlador.modelo.adicionar_figura(self.figura)
            self.controlador.lista_refazer.clear()
            self.controlador.historico.append(("desenho", figura))
            self.figura = None

        self.controlador.rabisco_atual = None
        self.controlador.redesenhar()

    def criar_figura_rabisco(self, rabisco):
        return self.classe_figura(
            self.controlador.visao.cor_borda.get(),
            self.controlador.visao.espessura.get(),
            self.controlador.visao.cor_preenchimento.get(), rabisco)

@dataclass
class FerramentaPoligono(Ferramenta):
    classe_figura: type = None
    def mouse_duplo(self, *args):
        if len(self.controlador.modelo.pontos_poligonos) < 6:
             return
        self.figura =  self.classe_figura(self.controlador.visao.cor_borda.get(), 
                                          self.controlador.visao.espessura.get(), 
                                          self.controlador.visao.cor_preenchimento.get(), 
                                          self.controlador.modelo.pontos_poligonos.copy())
        
        if self.figura:
            figura = self.figura
            self.controlador.modelo.adicionar_figura(self.figura)
            self.controlador.lista_refazer.clear()
            self.controlador.historico.append(("desenho", figura))
            self.figura = None
        self.controlador.modelo.pontos_poligonos.clear()
        self.controlador.redesenhar()     

    def mouse_pressionado(self, event):
        self.controlador.modelo.pontos_poligonos.append(event.x)
        self.controlador.modelo.pontos_poligonos.append(event.y)
        self.controlador.redesenhar()
    
    def mouse_arrastado(self, event):
        pass

    def mouse_solto(self,event):
        pass 

@dataclass
class FerramentaPoligonoRegular(Ferramenta):
    classe_figura: type = None
    lados: int = 3
    fim_X: int = 0
    fim_Y: int = 0
    parou_mover: bool = False
    desenhando : bool = False

    def mouse_pressionado(self, event):
        if not self.parou_mover:
            self.inicio_X = event.x
            self.inicio_Y = event.y
            self.desenhando = True
        else:
            self.diminuir_lado()

    def mouse_arrastado(self, event):
        if self.desenhando:
            self.fim_X = event.x
            self.fim_Y = event.y
            self.atualizar_desenho()

    def mouse_solto(self, event):
        if self.fim_X != 0:
            self.desenhando = False
            self.parou_mover = True

    def mouse_duplo(self, event):
        if self.figura:
            self.controlador.modelo.adicionar_figura(self.figura)
            self.controlador.lista_refazer.clear()
            self.controlador.historico.append(("desenho", self.figura))

            self.figura = None
            self.fim_X = 0
            self.fim_Y = 0
            self.desenhando = True
            self.parou_mover = False
            self.lados = 3
            self.controlador.redesenhar()

    def aumentar_lado(self):
        if self.parou_mover:
            self.lados += 1
            self.atualizar_desenho()

    def diminuir_lado(self):
        if self.lados > 3:
            self.lados -= 1
            self.atualizar_desenho()

    def atualizar_desenho(self):
        cx = self.inicio_X
        cy = self.inicio_Y

        pontos = self.controlador.modelo.calcular_pontos_poligono(
            cx,
            cy,
            self.fim_X,
            self.fim_Y,
            self.lados
        )
        if not pontos:
            return
        self.controlador.redesenhar()
        self.figura = self.classe_figura(
            self.controlador.visao.cor_borda.get(),
            self.controlador.visao.espessura.get(),
            self.controlador.visao.cor_preenchimento.get(),
            pontos
        )
        self.figura.desenhar(self.controlador.visao.canvas)
    
@dataclass
class FerramentaSelecao(Ferramenta):
    classe_figura: type = None
    def mouse_pressionado(self, event):
        self.inicio_X = event.x
        self.inicio_Y = event.y
        self.controlador.modelo.identificar_figura(event.x, event.y)
        self.controlador.redesenhar()

    def mouse_ctrl(self,event):
        self.controlador.modelo.identificar_varias(event.x,event.y)
        self.controlador.redesenhar()

    def mouse_arrastado(self, event):
        if self.controlador.modelo.figuras_selecionadas:
            self.controlador.modelo.mover_figura(event.x,event.y)
        self.controlador.redesenhar()
        if not self.controlador.modelo.figuras_selecionadas:
            self.controlador.modelo.retangulo_de_selecao(self.inicio_X, self.inicio_Y, event.x, event.y, self.controlador.visao.canvas)
    def mouse_solto(self, event):
        ultima_acao = self.controlador.modelo.finalizar_movimento()
        if ultima_acao:
                self.controlador.lista_refazer.clear()
                self.controlador.historico.append(ultima_acao)
        self.controlador.modelo.dx_total = 0
        self.controlador.modelo.dy_total = 0
        self.controlador.modelo.selecionar_retangulo(self.inicio_X, self.inicio_Y, event.x, event.y)
        self.controlador.redesenhar()        
    def atualizar_cor(self):
        self.controlador.modelo.atualizar_cor(self.controlador.visao.cor_borda.get(), self.controlador.visao.cor_preenchimento.get())
 