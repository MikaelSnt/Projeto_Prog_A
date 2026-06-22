from Figuras import *

def desenhar_previa(self, tipo, cor_borda, espessura, cor_preenchimento):

    if tipo == "Linha":
        previa = Linha(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)
        previa.desenhar(self.canvas)

    elif tipo == "Retângulo":
        previa = Retangulo(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)
        previa.desenhar(self.canvas)

    elif tipo == "Oval":
        previa = Oval(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)
        previa.desenhar(self.canvas)

    elif tipo == "Círculo":
        previa = Circulo(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)
        previa.desenhar(self.canvas)