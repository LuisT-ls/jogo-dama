# peca.py

class Peca:
    def __init__(self, cor):
        self.cor = cor
        self.dama = False

    def promover_dama(self):
        self.dama = True

    def __str__(self):
        return self.cor[0].upper() + ('D' if self.dama else '')