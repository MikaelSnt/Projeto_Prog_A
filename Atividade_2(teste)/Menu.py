from tkinter import *

def Menu(self):

    self.largura = 600
    self.altura = 800

    frame_Menu = Frame(self.janela)
    frame_Menu.pack()

    self.tipo_figura = StringVar(value="Rabisco")
    self.tipo_figura.trace_add("write", self.Aparecer_menu_poligonos)

    Menu_figura = OptionMenu(frame_Menu, self.tipo_figura, "Rabisco", "Linha", "Retângulo", "Oval", "Círculo", "Polígono")
    Menu_figura.grid(row=0, column=1)

    Figura_lbl = Label(frame_Menu,text= "Figuras: ")
    Figura_lbl.grid(row =0,column = 0)

    self.menu_tamanho = StringVar(value="800 x 600")
    self.menu_tamanho.trace_add("write", self.Mudar)

    menu_tamanho = OptionMenu(frame_Menu, self.menu_tamanho, "800 x 600", "1920 x 1300")
    menu_tamanho.grid(row=0,column=7)

    Tamanho_lbl = Label(frame_Menu,text= "Tamanho da tela: ")
    Tamanho_lbl.grid(row =0,column = 6)

    self.cor_borda = StringVar(value="black")
    Menu_Borda = OptionMenu(frame_Menu, self.cor_borda, "black", "blue", "green", "yellow", "purple")
    Menu_Borda.grid(row=1, column=4)

    lbl_corborda = Label(frame_Menu,text= "Cor da borda: ")
    lbl_corborda.grid(row = 1,column= 3)

    self.cor_preenchimento = StringVar(value="")
    Menu_preenchimento = OptionMenu(frame_Menu, self.cor_preenchimento, "black", "blue", "green", "yellow", "purple")
    Menu_preenchimento.grid(row=1, column=2)

    lbl_preenchimento = Label(frame_Menu,text= "Cor do preenchimento")
    lbl_preenchimento.grid(row = 1 , column = 1)

    self.espessura = IntVar(value=1)
    Menu_espessura = OptionMenu(frame_Menu, self.espessura, 1, 5, 10, 20, 30, 50)
    Menu_espessura.grid(row=0, column=5)

    lbl_espessura = Label(frame_Menu,text = "Espessura da borda: ")
    lbl_espessura.grid(row = 0 , column = 4)

    self.menu_poly = IntVar(value=3)
    self.Menu_poly = OptionMenu(frame_Menu, self.menu_poly, 3, 4, 5, 6)
    self.Menu_poly.grid_forget()

    self.poly_pontos = Label(frame_Menu,text= "Pontos do Polígono:")
    self.poly_pontos.grid_forget()

    Btn_limpar = Button(frame_Menu, text="Limpar", command=self.limpar)
    Btn_limpar.grid(row=1, column=6)

    self.canvas = Canvas(self.janela, bg="white", width=self.largura, height=self.altura)
    self.canvas.pack()

    self.canvas.bind("<ButtonPress-1>", self.iniciar_desenho)
    self.canvas.bind("<B1-Motion>", self.atualizar_desenho)
    self.canvas.bind("<Motion>", self.atualizar_previa_poligono)
    self.canvas.bind("<ButtonRelease-1>", self.finalizar_desenho)
def Mudar(self, *args):
    tamanho = self.menu_tamanho.get().split()
    self.altura = int(tamanho[0])
    self.largura = int(tamanho[2])
    self.canvas.config(width=self.largura, height=self.altura)

def Aparecer_menu_poligonos(self, *Nome):
    if self.tipo_figura.get() == "Polígono":
        self.Menu_poly.grid(row=0, column=3)
        self.poly_pontos.grid(row=0,column=2)
    else:
        self.Menu_poly.grid_forget()