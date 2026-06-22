from tkinter import *
from Menu import *
from Mouse import *
from Desenhos import *


class Aplicativo:
    def __init__(self):
        self.figuras = []
        self.rabisco_atual = None
        self.pontos_poligono = []

        self.janela = Tk()
        self.janela.title("Aplicativo_Prog_A")

        self.inicio_x = 0
        self.inicio_y = 0
        self.fim_x = 0
        self.fim_y = 0

        self.Menu()

    Menu = Menu
    Mudar = Mudar
    Aparecer_menu_poligonos = Aparecer_menu_poligonos

    iniciar_desenho = iniciar_desenho
    atualizar_desenho = atualizar_desenho
    finalizar_desenho = finalizar_desenho
    atualizar_previa_poligono = atualizar_previa_poligono
    desenhar_poligono = desenhar_poligono
    redesenhar = redesenhar
    limpar = limpar

    def Executar_app(self):
        self.janela.mainloop()

App = Aplicativo()
App.Executar_app()