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
            figura = self.figura

            self.controlador.modelo.adicionar_figura(self.figura)
            self.figura = None

            self.controlador.redesenhar()
            self.controlador.lista_refazer.clear()
            self.controlador.historico.append(("desenho", figura))
    
    def criar_figura(self, x1, y1, x2 , y2):
        pass
    def mouse_duplo(self, event):
        pass
    def selecionar(self, *args):
        pass
    def desselecionar(self):
        pass
    def atualizar_cor(self):
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
class FerramentaSelecao(Ferramenta):
    classe_figura: type = None
    figura_selecionada = None
    cor_original = None
    def mouse_pressionado(self, event):
        super().mouse_pressionado(event)
        self.desselecionar()
        for figura in reversed( self.controlador.modelo.figuras): 
            if figura.identificar(event): 
                self.figura_selecionada = figura
                self.dx_total = 0
                self.dy_total = 0
                if type(self.figura_selecionada).__name__ in ("Linha", "Rabisco") :
                    self.cor_original = figura.cor_preenchimento
                    figura.cor_preenchimento = "#80ff00"
                else:
                    self.cor_original = figura.cor_borda
                    figura.cor_borda = "#80ff00"
                self.controlador.redesenhar()
                break

    def mouse_arrastado(self, event):
        if self.figura_selecionada is None:
            return

        dx = event.x - self.inicio_X
        dy = event.y - self.inicio_Y

        self.dx_total += dx
        self.dy_total += dy
        
        self.figura_selecionada.mover(dx, dy)

        self.inicio_X = event.x
        self.inicio_Y = event.y
        self.controlador.redesenhar()
    
    def mouse_solto(self, event):
        if self.figura_selecionada:
            if self.dx_total != 0 or self.dy_total != 0:
                self.controlador.lista_refazer.clear()
                self.controlador.historico.append(("moveu",self.figura_selecionada,self.dx_total,self.dy_total))
        self.dx_total = 0
        self.dy_total = 0
    def desselecionar(self):
        if self.figura_selecionada:
            if type(self.figura_selecionada).__name__ in ("Linha", "Rabisco") :
                self.figura_selecionada.cor_preenchimento = self.cor_original
            else:
                self.figura_selecionada.cor_borda = self.cor_original
        self.figura_selecionada = None
        self.cor_original = None
        self.nova_cor = None
        self.controlador.redesenhar()
    def atualizar_cor(self):
        if self.figura_selecionada:
            self.figura_selecionada.cor_preenchimento = self.controlador.visao.cor_preenchimento.get()
            self.cor_original = self.controlador.visao.cor_borda.get()
 