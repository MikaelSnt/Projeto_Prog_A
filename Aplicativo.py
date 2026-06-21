from tkinter import *
from Figuras import *

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

    def Menu(self):
        frame_Menu = Frame(self.janela)
        frame_Menu.pack()

        self.tipo_figura = StringVar(value="Rabisco")
        Menu_figura = OptionMenu(frame_Menu, self.tipo_figura, "Linha", "Retângulo", "Oval", "Círculo", "Rabisco", "Polígono")
        Menu_figura.grid(row=0, column=0)

        self.cor_borda = StringVar(value="black")
        Menu_Borda = OptionMenu(frame_Menu, self.cor_borda, "black", "blue", "green", "yellow", "purple")
        Menu_Borda.grid(row=0, column=1)
        
        self.cor_preenchimento = StringVar(value="Black")
        Menu_preenchimento = OptionMenu(frame_Menu, self.cor_preenchimento, "black", "blue", "green", "yellow", "purple")
        Menu_preenchimento.grid(row=0, column=2)
        
        self.espessura = StringVar(value="5")
        Menu_espessura = OptionMenu(frame_Menu, self.espessura, "1", "2", "3", "5", "10")
        Menu_espessura.grid(row=0, column=3)

        self.menu_poly = StringVar(value=3)
        Menu_poly = OptionMenu(frame_Menu, self.menu_poly, 3, 4, 5)
        Menu_poly.grid_forget()

        Btn_limpar = Button(frame_Menu, text="Limpar",  command=self.limpar)
        Btn_limpar.grid(row=0, column=4)

        self.canvas = Canvas(self.janela, bg="white",  width=800,  height=600 )
        self.canvas.pack()



        self.canvas.bind("<ButtonPress-1>",  self.iniciar_desenho )
        self.canvas.bind("<B1-Motion>", self.atualizar_desenho)
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_desenho)
        
    def iniciar_desenho(self, event):
        self.inicio_x = event.x
        self.inicio_y = event.y
 
        if self.tipo_figura.get() == "Rabisco":
            self.rabisco_atual = [(event.x, event.y)]
    def atualizar_desenho(self, event):
        self.fim_x = event.x
        self.fim_y = event.y
    
        if self.tipo_figura.get() == "Rabisco":
            self.rabisco_atual.append( (event.x, event.y) )
        
            self.redesenhar()

            self.canvas.create_line(self.rabisco_atual, fill=self.cor_preenchimento.get(), width=float(self.espessura.get()))
    
    def finalizar_desenho(self, event):

        self.fim_x = event.x
        self.fim_y = event.y

        tipo = self.tipo_figura.get()

        cor_borda = self.cor_borda.get()
        cor_preenchimento = self.cor_preenchimento.get()
        espessura = float(self.espessura.get())

        figura_atual = None


        if tipo == "Rabisco":
            figura_atual = Rabisco(cor_borda, espessura, cor_preenchimento, self.rabisco_atual)
            self.rabisco_atual = None

        elif tipo == "Linha":
            figura_atual = Linha(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x,  self.fim_y )

        elif tipo == "Retângulo":
            figura_atual = Retangulo(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)

        elif tipo == "Oval":
            figura_atual = Oval(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y )

        elif tipo == "Círculo":
            figura_atual = Circulo(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y )
        if figura_atual:
            self.figuras.append(figura_atual)
        
        self.redesenhar()
    
    def desenhar_poligono(self, event):
        if len(self.pontos_poligono) < 6:
            return 
        self.pontos_poligono.append(event.x)
        self.pontos_poligono.append(event.y)

        figura_atual = Poligono(self.cor_borda.get(), float(self.espessura.get()), self.cor_preenchimento.get(), self.pontos_poligono)
        self.figuras.append(figura_atual)


        self.redesenhar()

    def redesenhar(self):
        self.canvas.delete("all")
        for figura_atual in self.figuras:
            figura_atual.desenhar(self.canvas)
        
    def limpar(self):
        self.figuras.clear()
        self.pontos_poligono.clear()
        self.canvas.delete("all")
    def Executar_app(self):
        self.janela.mainloop()

App = Aplicativo()
App.Executar_app()