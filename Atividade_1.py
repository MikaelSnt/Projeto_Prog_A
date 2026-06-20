from tkinter import *
def desenhar_figuras(event):
    global inicio_x, inicio_y, rabisco_atual
    inicio_x = event.x
    inicio_y = event.y
    if tipo_figura_var.get() == "Rabisco":
        rabisco_atual = [(event.x, event.y)]
def atualizar_desenho(event):
    global fim_x, fim_y, inicio_x, inicio_y, rabisco_atual

    fim_x = event.x
    fim_y = event.y

    if tipo_figura_var.get() == "Rabisco":
        rabisco_atual.append((event.x, event.y))
        canvas.delete("all")
        for desenho in figuras:
            desenhar_um(desenho)
        if len(rabisco_atual) > 1:
            canvas.create_line(rabisco_atual, fill=preenchimento.get(), width=float(Valor_da_borda.get()),)
    else:
        canvas.delete("all")
        for desenho in figuras:
            desenhar_um(desenho)
        desenhar_previa()
def finalizar_desenho(event):
    global rabisco_atual
    global fim_x, fim_y

    fim_x = event.x
    fim_y = event.y

    tipo = tipo_figura_var.get()
    cor_borda = borda.get()
    cor_preenchimento = preenchimento.get()
    tamanho_da_borda = float(Valor_da_borda.get())
    desenho = ( tipo, inicio_x, inicio_y, fim_x, fim_y, cor_borda, tamanho_da_borda, cor_preenchimento)

    if tipo_figura_var.get() == "Rabisco":
        if rabisco_atual and len(rabisco_atual) > 1:
            figuras.append(("Rabisco", rabisco_atual, float(Valor_da_borda.get()), preenchimento.get()))
        rabisco_atual = None
        return

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
    tamanho_da_borda = float(Valor_da_borda.get())
    if tipo == "linha":
        canvas.create_line(inicio_x,inicio_y, fim_x, fim_y, fill=cor_preenchimento, width=tamanho_da_borda )
    elif tipo == "Retângulos":
        canvas.create_rectangle( inicio_x, inicio_y,fim_x, fim_y, outline=cor_borda, fill=cor_preenchimento, width=tamanho_da_borda)
    elif tipo == "Ovais":
        canvas.create_oval( inicio_x, inicio_y,fim_x, fim_y,  outline=cor_borda, fill=cor_preenchimento, width=tamanho_da_borda)
    elif tipo == "Círculos":
        raio = ( (inicio_x - fim_x)**2 + (inicio_y - fim_y)**2 ) ** 0.5
        canvas.create_oval(inicio_x - raio, inicio_y - raio, inicio_x + raio,inicio_y + raio , outline=cor_borda, fill=cor_preenchimento,width=tamanho_da_borda)
def desenhar_um(desenho):
    if desenho[0] == "Rabisco":
        _, pontos, espessura, cor = desenho
        canvas.create_line( pontos, fill=cor, width=espessura,)
        return
    tipo, x1, y1, x2, y2, cor_borda, tamanho_da_borda, cor_preenchimento = desenho
    if tipo == "linha":
        canvas.create_line(x1, y1, x2, y2, fill=cor_preenchimento, width=tamanho_da_borda )
    elif tipo == "Retângulos":
        canvas.create_rectangle( x1, y1, x2, y2, outline=cor_borda, fill=cor_preenchimento, width=tamanho_da_borda )
    elif tipo == "Ovais":
        canvas.create_oval( x1, y1, x2, y2, outline=cor_borda,fill=cor_preenchimento, width=tamanho_da_borda )
    elif tipo == "Círculos":
        raio = ((x1-x2)**2 + (y1-y2)**2)**0.5
        canvas.create_oval( x1-raio, y1-raio, x1+raio, y1+raio, outline=cor_borda, fill=cor_preenchimento, width=tamanho_da_borda)
def limpar_tela():
    figuras.clear()
    canvas.delete("all")

rabisco_atual = None
figuras = []

janela = Tk()
janela.rowconfigure(0, minsize=800, weight=1)
janela.columnconfigure(0, minsize=800, weight=1)
janela.title("Projeto_Prog_A")
frame = Frame(janela)
frame_opcoes  = Frame(janela)
frame_bnt = Frame(janela)
paddings = {'padx': 20, 'pady': 2}

Valor_da_borda = StringVar()
menu_controlar_borda = OptionMenu(frame_opcoes,Valor_da_borda,  "10","20","30","40","50","60" )
Valor_da_borda.set("10")


borda = StringVar()
menu_da_borda = OptionMenu(frame_opcoes, borda, "Black", "white", "blue", "yellow", "purple", "green"  )
borda.set("Black")

preenchimento = StringVar()
menu_do_preenchimento = OptionMenu(frame_opcoes, preenchimento, "Black", "white", "blue", "yellow", "purple", "green" )
preenchimento.set("Black")

tipo_figura_var = StringVar(value="linha")
option_menu = OptionMenu(frame_opcoes, tipo_figura_var, 'linha', 'Retângulos', 'Ovais','Círculos', 'Rabisco')

canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.bind('<ButtonPress-1>',desenhar_figuras )
canvas.bind('<B1-Motion>', atualizar_desenho)
canvas.bind('<ButtonRelease-1>', finalizar_desenho)


frame_opcoes.pack(**paddings)
option_menu.grid(row=0, column=0)
lbl_texto_borda = Label(master=frame_opcoes, text="Borda:").grid(row=0, column=1)
menu_da_borda.grid(row=0,column=2)
lbl_texto_Preenchimento = Label(master=frame_opcoes, text="Preenchimento:").grid(row=0, column=3)
menu_do_preenchimento.grid(row=0,column=4)
lbl_texto_Espessura = Label(master=frame_opcoes, text="Espessura:").grid(row=0, column=5)
menu_controlar_borda.grid(row=0, column=6)

frame.pack()
canvas.grid(column=0, row=1, **paddings)

btn = Button(frame_bnt, relief=RAISED, text="Limpar", command=limpar_tela).grid(row=1, column=0)
frame_bnt.pack()

janela.mainloop()