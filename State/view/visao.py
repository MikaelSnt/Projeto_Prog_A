from tkinter import *
from tkinter.colorchooser import askcolor
import tkinter as tk




class Visao:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Aplicativo_MMD")

        self.largura = 400
        self.altura = 400

        self.tipo_figura = StringVar(value= "Rabisco")
        self.menu_tamanho = StringVar(value="Tamanho_do_Desenho")
        self.cor_borda = StringVar(value="black")
        self.cor_preenchimento = StringVar(value="black")
        self.espessura = IntVar(value=5)
        self.menu_poly = IntVar(value=3)
        self.grade = StringVar(value = "Sem grade")
        self.criar_interface()

    def criar_interface(self):

        self.frame_menu = Frame(self.janela)
        self.frame_menu.pack()

        self.menu_figura = OptionMenu(
            self.frame_menu,
            self.tipo_figura,
           "Rabisco",
            "Linha",
            "Retângulo",
            "Oval",
            "Círculo",
            "Polígono"
        )
        self.menu_figura.grid(row=0, column=1)
        lbl_figura = Label(self.frame_menu,text = "Figura: ")
        lbl_figura.grid(row = 0 , column= 0)

        self.menu_tam = OptionMenu(
            self.frame_menu,
            self.menu_tamanho,
            "800 x 600",
            "1920 x 1300",
        )
    
        self.menu_tam.grid(row=0, column=7)
        lbl_tamanho = Label(self.frame_menu,text = "Tamanho da tela: ")
        lbl_tamanho.grid(row = 0 , column= 6)

        self.botao_cor_borda = Button(
                    self.frame_menu,
                    bg=self.cor_borda.get(),width=3,
                command=self.escolher_cor_borda,
                relief=tk.RAISED,borderwidth=3
                            )
        self.botao_cor_borda.grid(row=1, column=4)
        lbl_borda = Label(self.frame_menu,text = "Cor da Borda: ")
        lbl_borda.grid(row = 1 , column= 3)

        self.botao_preenchimento = Button(
                    self.frame_menu,
                    bg=self.cor_preenchimento.get(),width=3,
                command=self.escolher_cor_preenchimento,
                relief=tk.RAISED,borderwidth=3
                            )
        self.botao_preenchimento.grid(row=1, column=1)
        lbl_preenchimento = Label(self.frame_menu,text = "Cor do preenchimento: ")
        lbl_preenchimento.grid(row = 1 , column= 0)

        self.menu_espessura = OptionMenu(
            self.frame_menu,
            self.espessura,
            1, 5, 10, 20, 30, 50
        )
        self.menu_espessura.grid(row=0, column=4)
        lbl_espessura = Label(self.frame_menu,text = "Espessura: ")
        lbl_espessura.grid(row = 0 , column= 3)

        self.btn_limpar = Button(
            self.frame_menu,
            text="Limpar",
           activebackground="gray", activeforeground="white" 
        )
        self.btn_limpar.grid(row=1,column=7)
        self.menu_grade = OptionMenu(
            self.frame_menu,
            self.grade,
             "Sem grade","Com grade")
        self.menu_grade.grid(row=1,column=6)
               
        
        self.bt_abrir = tk.Button(self.frame_menu, text="Abrir Desenho")
        self.bt_abrir.grid(row = 2 , column= 5)
        self.bt_salvar =tk.Button(self.frame_menu, text="Salvar Desenho")
        self.bt_salvar.grid(row = 2,column= 3)

        self.canvas = Canvas(
            self.janela,
            bg="white",
            width=self.largura,
            height=self.altura
        
        )
        self.canvas.pack()
    def escolher_cor_borda(self):
        cor = askcolor()[1]

        if cor:
            self.cor_borda.set(cor)
            self.botao_cor_borda.config(bg=cor)
    def escolher_cor_preenchimento(self):
        cor = askcolor()[1]

        if cor:
            self.cor_preenchimento.set(cor)
            self.botao_preenchimento.config(bg=cor)