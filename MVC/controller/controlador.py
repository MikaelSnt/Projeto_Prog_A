from model.modelo import Poligono

class Controlador:
    def __init__(self, modelo, visao):
        self.modelo = modelo
        self.visao = visao

        self.inicio_x = 0
        self.inicio_y = 0
        self.fim_x = 0
        self.fim_y = 0

        self.rabisco_atual = None

        self.configurar_eventos()
        self.redesenhar()

    def configurar_eventos(self):
        self.visao.grade.trace_add("write", self.atualizar_grade)

        self.visao.menu_tamanho.trace_add("write", self.mudar_tamanho)

        self.visao.btn_limpar.config(command=self.limpar)

        self.visao.canvas.bind("<ButtonPress-1>", self.iniciar_desenho)

        self.visao.canvas.bind("<B1-Motion>", self.atualizar_desenho)

        self.visao.canvas.bind("<ButtonRelease-1>", self.finalizar_desenho)

       

    def mudar_tamanho(self, *args):
        tamanho = self.visao.menu_tamanho.get().split()

        self.visao.altura = int(tamanho[0])
        self.visao.largura = int(tamanho[2])

        self.visao.canvas.config(width=self.visao.largura, height=self.visao.altura)
        if self.visao.grade.get() == "Com grade":
            self.exibir_grades()

    def iniciar_desenho(self, event):
        self.inicio_x = event.x
        self.inicio_y = event.y
        
        if self.visao.tipo_figura.get() == "Rabisco":
            self.rabisco_atual = [event.x, event.y]
        elif self.visao.tipo_figura.get() == "Polígono":
            self.desenhar_poligono(event)

    def atualizar_desenho(self, event):
        self.fim_x = event.x
        self.fim_y = event.y
        self.redesenhar()
        tipo = self.visao.tipo_figura.get()
        cor_borda = self.visao.cor_borda.get()
        espessura = self.visao.espessura.get()
        cor_preenchimento = self.visao.cor_preenchimento.get()
        
        if self.visao.tipo_figura.get() == "Rabisco" and self.rabisco_atual:
            self.rabisco_atual.extend([event.x, event.y])

            if len(self.rabisco_atual) >= 4:
                self.visao.canvas.create_line(self.rabisco_atual, fill=self.visao.cor_preenchimento.get(), width=float(self.visao.espessura.get()))
                
        elif tipo == "Linha":
            self.visao.canvas.create_line(self.inicio_x, self.inicio_y, self.fim_x, self.fim_y, fill=cor_preenchimento, width=espessura)

        elif tipo == "Retângulo":
            self.visao.canvas.create_rectangle(self.inicio_x, self.inicio_y, self.fim_x, self.fim_y, outline=cor_borda, fill=cor_preenchimento ,width=espessura)


        elif tipo == "Oval":
            self.visao.canvas.create_oval(self.inicio_x, self.inicio_y, self.fim_x, self.fim_y, outline=cor_borda, fill=cor_preenchimento ,width=espessura)
            
        elif tipo == "Círculo":
            raio = ((self.inicio_x - self.fim_x) ** 2 + (self.inicio_y - self.fim_y) ** 2 ) ** 0.5
            self.visao.canvas.create_oval(self.inicio_x - raio, self.inicio_y - raio, self.inicio_x + raio, self.inicio_y + raio,outline=cor_borda, fill=cor_preenchimento ,width=espessura)
    
    def finalizar_desenho(self, event):
        tipo = self.visao.tipo_figura.get()
        if tipo == "Polígono":
            return
        self.fim_x = event.x
        self.fim_y = event.y
        
        cor_borda = self.visao.cor_borda.get()
        espessura = self.visao.espessura.get()
        cor_preenchimento = self.visao.cor_preenchimento.get()
        
        figura = self.modelo.criar_figuras(tipo, cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x,self.fim_y, self.rabisco_atual)
        if figura:
            self.modelo.adicionar_figura(figura)
        self.rabisco_atual = None
        self.redesenhar()
    
    def desenhar_poligono(self, event):
        self.modelo.pontos_poligonos.append(event.x)
        self.modelo.pontos_poligonos.append(event.y)
        self.visao.canvas.bind("<Double-Button-1>", self.finalizar_poligono)
        self.redesenhar() 
        
    def finalizar_poligono(self, event):
        if self.visao.tipo_figura.get() != "Polígono":
            return
        if len(self.modelo.pontos_poligonos) < 6:
            return
        figura = Poligono(self.visao.cor_borda.get(),float(self.visao.espessura.get()),self.visao.cor_preenchimento.get(),self.modelo.pontos_poligonos.copy())
        if figura:
            self.modelo.adicionar_figura(figura)
        self.modelo.pontos_poligonos.clear()
        self.redesenhar() 
    
    
    def exibir_grades(self):
            linhas = self.modelo.criar_grade(self.visao.largura,self.visao.altura,10)
            for x1, y1, x2, y2 in linhas:
                self.visao.canvas.create_line(x1, y1, x2, y2, fill="lightgray")


         
    def atualizar_grade(self, *args):
        self.redesenhar()

    def redesenhar(self):
        self.visao.canvas.delete("all")

        if self.visao.grade.get() == "Com grade":
            self.exibir_grades()

        for figura in self.modelo.obter_figuras():
            figura.desenhar(self.visao.canvas)

        if len(self.modelo.pontos_poligonos) >= 4:
            self.visao.canvas.create_line(
            self.modelo.pontos_poligonos,
            fill=self.visao.cor_borda.get(),
            width=2
        )

    def limpar(self):
        self.modelo.limpar()
        self.visao.canvas.delete("all")
        if self.visao.grade.get() == "Com grade":
            self.exibir_grades()