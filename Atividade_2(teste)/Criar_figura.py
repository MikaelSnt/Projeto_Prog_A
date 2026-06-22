from Figuras import *

def criar_figura(self, tipo, cor_borda, espessura, cor_preenchimento):

    if tipo == "Rabisco":
        if self.rabisco_atual and len(self.rabisco_atual) >= 4:
            return Rabisco(cor_borda, espessura, cor_preenchimento, self.rabisco_atual)

    elif tipo == "Linha":
        return Linha(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)

    elif tipo == "Retângulo":
        return Retangulo(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)

    elif tipo == "Oval":
        return Oval(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)

    elif tipo == "Círculo":
        return Circulo(cor_borda, espessura, cor_preenchimento, self.inicio_x, self.inicio_y, self.fim_x, self.fim_y)

    return None