from Figuras import *
from Criar_figura import *
from Previa import *

def iniciar_desenho(self, event):

    self.inicio_x = event.x
    self.inicio_y = event.y

    if self.tipo_figura.get() == "Rabisco":
        self.rabisco_atual = [event.x, event.y]

    elif self.tipo_figura.get() == "Polígono":
        self.desenhar_poligono(event)

def atualizar_desenho(self, event):

    self.fim_x = event.x
    self.fim_y = event.y

    tipo = self.tipo_figura.get()

    cor_borda = self.cor_borda.get()
    cor_preenchimento = self.cor_preenchimento.get()
    espessura = float(self.espessura.get())

    if tipo == "Rabisco" and self.rabisco_atual != None:
        self.rabisco_atual.extend([event.x, event.y])

        self.redesenhar()

        if len(self.rabisco_atual) >= 4:
            self.canvas.create_line(self.rabisco_atual, fill=self.cor_preenchimento.get(), width=float(self.espessura.get()))

    elif tipo != "Polígono":
        self.redesenhar()
        desenhar_previa(self, tipo, cor_borda, espessura, cor_preenchimento)

def finalizar_desenho(self, event):

    self.fim_x = event.x
    self.fim_y = event.y

    tipo = self.tipo_figura.get()

    cor_borda = self.cor_borda.get()
    cor_preenchimento = self.cor_preenchimento.get()
    espessura = float(self.espessura.get())

    figura_atual = criar_figura(self, tipo, cor_borda, espessura, cor_preenchimento)

    if tipo == "Rabisco":
        self.rabisco_atual = None

    if figura_atual:
        self.figuras.append(figura_atual)

    self.redesenhar()

def atualizar_previa_poligono(self, event):

    if self.tipo_figura.get() == "Polígono" and len(self.pontos_poligono) >= 2:

        self.redesenhar()

        pontos = self.pontos_poligono.copy()

        pontos.append(event.x)
        pontos.append(event.y)

        self.canvas.create_line(
            pontos,
            fill=self.cor_borda.get(),
            width=float(self.espessura.get()),
            dash=(1,1)
        )