# tabuleiro.py
from peca import Peca

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.inicializar_pecas()

    def inicializar_pecas(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    if i < 3:
                        self.tabuleiro[i][j] = Peca("branca")
                    elif i > 4:
                        self.tabuleiro[i][j] = Peca("preta")

    def obter_peca(self, x, y):
        return self.tabuleiro[x][y]

    def mover_peca(self, de_x, de_y, para_x, para_y):
        peca = self.tabuleiro[de_x][de_y]
        self.tabuleiro[de_x][de_y] = None
        self.tabuleiro[para_x][para_y] = peca

        # Verificar se a peça deve ser promovida a dama
        if (peca.cor == "branca" and para_x == 7) or (peca.cor == "preta" and para_x == 0):
            peca.promover_dama()

    def posicao_valida(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8