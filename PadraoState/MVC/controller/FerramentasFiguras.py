from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Ferramenta(ABC):
    controlador : object
    inicio_X: int = 0
    inicio_Y: int = 0
    figura: object = None

    def mouse_pressionado(self, event):
        self.inicio_X = event.x
        self.inicio_Y = event.y

    def mouse_arrastado(self, event):
        self.figura = self.criar_figura(self.inicio_X, self.inicio_Y, event.x, event.y)
        self.controlador.redesenhar()

    def mouse_solto(self, event):
        if self.figura:
            self.controlador.modelo.adicionar_figura(self.figura)
            self.figura = None
        
        self.controlador.redesenhar()

    @abstractmethod
    def criar_figura(self, x1, y1, x2 , y2):
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