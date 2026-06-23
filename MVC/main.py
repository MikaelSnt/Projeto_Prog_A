from tkinter import Tk

from model.modelo import Modelo
from view.visao import Visao
from controller.controlador import Controlador

janela = Tk()

modelo = Modelo()
visao = Visao(janela)
controlador = Controlador(modelo, visao)

janela.mainloop()