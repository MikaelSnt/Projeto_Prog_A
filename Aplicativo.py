from tkinter import *
from Figuras import *
# Sempre Comentar as Atualizações para não se Perder.
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

        self.largura = 400
        self.altura = 100

        frame_Menu = Frame(self.janela)
        frame_Menu.pack()

        self.tipo_figura = StringVar(value="Rabisco")
        self.tipo_figura.trace_add("write", self.Aparecer_menu_poligonos)
        Menu_figura = OptionMenu(frame_Menu, self.tipo_figura, "Rabisco", "Linha", "Retângulo", "Oval", "Círculo", "Polígono")
        Menu_figura.grid(row=0, column=0)

        
        self.menu_tamanho = StringVar(value="Tamanho_do_Desenho")
        self.menu_tamanho.trace_add("write", self.Mudar)
        menu_tamanho = OptionMenu(frame_Menu, self.menu_tamanho, "800 x 600", "1280 x 600", "1920 x 1300")
        menu_tamanho.grid(row=0,column=12)


        self.cor_borda = StringVar(value="black")
        Menu_Borda = OptionMenu(frame_Menu, self.cor_borda, "black", "blue", "green", "yellow", "purple")
        Menu_Borda.grid(row=0, column=3)
        
        self.cor_preenchimento = StringVar(value="Black")
        Menu_preenchimento = OptionMenu(frame_Menu, self.cor_preenchimento, "black", "blue", "green", "yellow", "purple")
        Menu_preenchimento.grid(row=0, column=4)
        
        self.espessura = IntVar(value=5)
        Menu_espessura = OptionMenu(frame_Menu, self.espessura, 1, 5, 10, 20, 30, 50)
        Menu_espessura.grid(row=0, column=5)

        self.menu_poly = IntVar(value=3)
        self.Menu_poly = OptionMenu(frame_Menu, self.menu_poly, 3, 4, 5, 6)
        self.Menu_poly.grid_forget()

        Btn_limpar = Button(frame_Menu, text="Limpar",  command=self.limpar)
        Btn_limpar.grid(row=0, column=6)


        self.canvas = Canvas(self.janela, bg="white", width=self.largura, height=self.altura)
        self.canvas.pack()



        self.canvas.bind("<ButtonPress-1>",  self.iniciar_desenho )
        self.canvas.bind("<B1-Motion>", self.atualizar_desenho)
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_desenho)


    def Mudar(self, *args):
        tamanho = self.menu_tamanho.get().split()
        self.altura = int(tamanho[0])
        self.largura = int(tamanho[2])
        self.canvas.config( width=self.largura, height=self.altura)

    def Aparecer_menu_poligonos(self, *Nome):
        if self.tipo_figura.get() == "Polígono":
            self.Menu_poly.grid(row=0, column=1)
        else:
            self.Menu_poly.grid_forget()
    def iniciar_desenho(self, event):
        self.inicio_x = event.x
        self.inicio_y = event.y

        if self.tipo_figura.get() == "Rabisco" :
            self.rabisco_atual = [event.x, event.y]

        elif self.tipo_figura.get() == "Polígono":
            self.desenhar_poligono(event)

    def atualizar_desenho(self, event):
        self.fim_x = event.x
        self.fim_y = event.y
    
        if self.tipo_figura.get() == "Rabisco" and self.rabisco_atual != None:
            self.rabisco_atual.extend([event.x, event.y])
        
            self.redesenhar()
            if len(self.rabisco_atual) >= 4:
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
            if self.rabisco_atual and len(self.rabisco_atual) >= 4:
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
        self.pontos_poligono.append(event.x)
        self.pontos_poligono.append(event.y)
        
        coordenadas = int(self.menu_poly.get()) * 2
        
        if len(self.pontos_poligono) < coordenadas:
            return
        
        figura_atual = Poligono(self.cor_borda.get(), float(self.espessura.get()), self.cor_preenchimento.get(), self.pontos_poligono.copy())
        self.figuras.append(figura_atual)
        self.pontos_poligono.clear()
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