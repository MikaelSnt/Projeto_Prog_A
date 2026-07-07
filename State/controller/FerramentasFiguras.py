from dataclasses import dataclass


@dataclass
class Ferramenta():
    controlador : object
    inicio_X: int = 0
    inicio_Y: int = 0
    figura: object = None
    figura_selecionada = None
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
            self.controlador.modelo.adicionar_figura(self.figura)
            self.figura = None
        
        self.controlador.redesenhar()
    
    def criar_figura(self, x1, y1, x2 , y2):
        pass
    def mouse_duplo(self, event):
        pass
    def selecionar(self, *args):
        pass
@dataclass
class FerramentaCriar(Ferramenta):
    classe_figura: type = None

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
            self.controlador.modelo.adicionar_figura(self.figura)
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
            self.controlador.modelo.adicionar_figura(self.figura)
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
class FerramentaSelecao(Ferramenta):
    classe_figura: type = None
    figura_selecionada = None
    def selecionar(self, event): 
        for figura in reversed( self.controlador.modelo.figuras ): 
            if figura.identificar(event): 
                self.figura_selecionada = figura
                break
    def mouse_arrastado(self, event):
        if self.figura_selecionada is None:
            return

        dx = event.x - self.inicio_X
        dy = event.y - self.inicio_Y

        self.figura_selecionada.mover(dx, dy)

        self.inicio_X = event.x
        self.inicio_Y = event.y

        self.controlador.redesenhar()