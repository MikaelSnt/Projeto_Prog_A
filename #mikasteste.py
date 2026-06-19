#mikasteste

from tkinter import *
def desenhar_figuras(event):
    global inicio_x, inicio_y
    inicio_x = event.x
    inicio_y = event.y
def atualizar_desenho(event):
    global fim_x, fim_y
    fim_x = event.x
    fim_y = event.y

    canvas.delete("all")
    for desenho in figuras:
        desenhar_um(desenho)
    desenhar_previa()    
    

def finalizar_desenho(event):
    global fim_x, fim_y
    fim_x = event.x
    fim_y = event.y

    tipo = tipo_figura_var.get()
    cor_borda = borda.get()
    cor_preenchimento = preenchimento.get()

    desenho = ( tipo, inicio_x, inicio_y, fim_x, fim_y, cor_borda, cor_preenchimento)
    
    figuras.append(desenho)
    
    desenhar_tudo()


def desenhar_tudo():
    canvas.delete("all")
    for desenho in figuras:
        desenhar_um(desenho)

def desenhar_previa():
    tipo = tipo_figura_var.get()
    cor_borda = borda.get()
    cor_preenchimento = preenchimento.get()
    
   

    if tipo == "Retângulos":
        canvas.create_rectangle( inicio_x, inicio_y,fim_x, fim_y, outline=cor_borda, fill=cor_preenchimento)

    elif tipo == "Ovais":
        canvas.create_oval( inicio_x, inicio_y,fim_x, fim_y,  outline=cor_borda, fill=cor_preenchimento)
    
    elif tipo == "Círculos":
        raio =  ((fim_x - inicio_x) ** 2 + (fim_y - inicio_y) ** 2) ** 0.5
        novo_x2 = 0
        novo_y2 = 0
        if fim_x >= inicio_x:
            novo_x2 = inicio_x + raio  
        else: 
            novo_x2 = inicio_x- raio
        if fim_y >= inicio_y:
            novo_y2 = fim_y + raio
        else:
            novo_y2 = fim_y - raio
        canvas.create_oval(inicio_x, fim_y, novo_x2, novo_y2, outline=cor_borda, fill=cor_preenchimento)

def desenhar_um(desenho):
    tipo, x1, y1, x2, y2, cor_borda, cor_preenchimento = desenho

    if tipo == "Retângulos":
        canvas.create_rectangle( x1, y1, x2, y2, outline=cor_borda, fill=cor_preenchimento)

    elif tipo == "Ovais":
        canvas.create_oval( x1, y1, x2, y2, outline=cor_borda, fill=cor_preenchimento)
    
    elif tipo == "Círculos":
        raio =  ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        novo_x2 = 0
        novo_y2 = 0
        if x2 >= x1:
            novo_x2 = x1 + raio  
        else: 
            novo_x2 = x1 - raio
        if y2 >= y1:
            novo_y2 = y1 + raio
        else:
            novo_y2 = y1 - raio
        canvas.create_oval(x1, y1, novo_x2, novo_y2, outline=cor_borda, fill=cor_preenchimento)

def limpar_tela():
    figuras.clear()
    canvas.delete("all")


figuras = []

janela = Tk()
janela.geometry('800x600')
janela.title("Atividade_1")
frame = Frame(janela)
paddings = {'padx': 5, 'pady': 5}


borda = StringVar(master=janela)
borda.set("Black")
preenchimento = StringVar(master=janela)
preenchimento.set("Black")

tipo_figura_var = StringVar(value="Retângulos")
option_menu = OptionMenu(frame, tipo_figura_var, 'Retângulos', 'Ovais', 'Círculos')

canvas = Canvas(janela, width=600, height=600, bg="white")
canvas.bind('<ButtonPress-1>',desenhar_figuras )
canvas.bind('<B1-Motion>', atualizar_desenho)
canvas.bind('<ButtonRelease-1>', finalizar_desenho)

btn = Button(janela, relief=RAISED, text="Limpar", command=limpar_tela)

btn.pack( anchor="center")
frame.pack(fill="x", anchor="w")
option_menu.pack(side=LEFT, padx=5, pady=5)
canvas.pack(fill="both", expand=True)
janela.mainloop()