import random

class Peca:
    def __init__(self, cor):
        self.cor = cor
        self.dama = False

    def promover_dama(self):
        self.dama = True

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

        # Remover peça capturada, se houver
        if abs(de_x - para_x) == 2:
            meio_x = (de_x + para_x) // 2
            meio_y = (de_y + para_y) // 2
            self.tabuleiro[meio_x][meio_y] = None

        return peca.dama

    def posicao_valida(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

class IAAvancada:
    def __init__(self, jogo):
        self.jogo = jogo
        self.dificuldades = {
            "muito fácil": 1,
            "fácil": 2,
            "médio": 3,
            "difícil": 4,
            "muito difícil": 5,
            "especialista": 6
        }

    def avaliar_tabuleiro(self):
        pontuacao = 0
        for i in range(8):
            for j in range(8):
                peca = self.jogo.tabuleiro.obter_peca(i, j)
                if peca:
                    valor = 1 if not peca.dama else 2
                    if peca.cor == "preta":
                        pontuacao += valor
                    else:
                        pontuacao -= valor
        return pontuacao

    def obter_todos_movimentos(self, cor):
        movimentos = []
        for i in range(8):
            for j in range(8):
                peca = self.jogo.tabuleiro.obter_peca(i, j)
                if peca and peca.cor == cor:
                    movimentos.extend(self.jogo.obter_movimentos_validos(i, j))
        return movimentos

    def minimax(self, profundidade, alfa, beta, maximizando):
        if profundidade == 0 or self.jogo.verificar_vitoria():
            return self.avaliar_tabuleiro()

        movimentos = self.obter_todos_movimentos("preta" if maximizando else "branca")
        if not movimentos:
            return -1000 if maximizando else 1000

        if maximizando:
            melhor_valor = float('-inf')
            for movimento in movimentos:
                self.jogo.fazer_jogada(*movimento)
                valor = self.minimax(profundidade - 1, alfa, beta, False)
                self.jogo.desfazer_jogada()
                melhor_valor = max(melhor_valor, valor)
                alfa = max(alfa, melhor_valor)
                if beta <= alfa:
                    break
            return melhor_valor
        else:
            melhor_valor = float('inf')
            for movimento in movimentos:
                self.jogo.fazer_jogada(*movimento)
                valor = self.minimax(profundidade - 1, alfa, beta, True)
                self.jogo.desfazer_jogada()
                melhor_valor = min(melhor_valor, valor)
                beta = min(beta, melhor_valor)
                if beta <= alfa:
                    break
            return melhor_valor

    def obter_melhor_jogada(self, dificuldade):
        profundidade = self.dificuldades.get(dificuldade, 3)
        
        if dificuldade == "muito fácil":
            return self.jogada_aleatoria()
        
        melhor_jogada = None
        melhor_valor = float('-inf')
        alfa = float('-inf')
        beta = float('inf')

        movimentos = self.obter_todos_movimentos("preta")
        random.shuffle(movimentos)

        for movimento in movimentos:
            self.jogo.fazer_jogada(*movimento)
            valor = self.minimax(profundidade - 1, alfa, beta, False)
            self.jogo.desfazer_jogada()
            
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = movimento

            if dificuldade != "especialista" and random.random() < 0.1:
                break

        return melhor_jogada

    def jogada_aleatoria(self):
        movimentos = self.obter_todos_movimentos("preta")
        return random.choice(movimentos) if movimentos else None

class Jogo:
    def __init__(self, modo="pvp", dificuldade="médio"):
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = "branca"
        self.modo = modo
        self.dificuldade = dificuldade
        self.ia_avancada = IAAvancada(self)
        self.historico_jogadas = []

    def trocar_jogador(self):
        self.jogador_atual = "preta" if self.jogador_atual == "branca" else "branca"

    def movimento_valido(self, de_x, de_y, para_x, para_y):
        if not self.tabuleiro.posicao_valida(para_x, para_y):
            return False

        peca = self.tabuleiro.obter_peca(de_x, de_y)
        if peca is None or peca.cor != self.jogador_atual:
            return False

        destino = self.tabuleiro.obter_peca(para_x, para_y)
        if destino is not None:
            return False

        direcao = 1 if peca.cor == "branca" else -1
        if peca.dama:
            if abs(de_x - para_x) == abs(de_y - para_y):
                return True
        elif para_x - de_x == direcao and abs(de_y - para_y) == 1:
            return True
        elif para_x - de_x == 2 * direcao and abs(de_y - para_y) == 2:
            meio_x = (de_x + para_x) // 2
            meio_y = (de_y + para_y) // 2
            peca_meio = self.tabuleiro.obter_peca(meio_x, meio_y)
            if peca_meio and peca_meio.cor != peca.cor:
                return True

        return False

    def fazer_jogada(self, de_x, de_y, para_x, para_y):
        if self.movimento_valido(de_x, de_y, para_x, para_y):
            peca = self.tabuleiro.obter_peca(de_x, de_y)
            peca_capturada = self.tabuleiro.obter_peca((de_x + para_x) // 2, (de_y + para_y) // 2) if abs(de_x - para_x) == 2 else None
            foi_promovida = self.tabuleiro.mover_peca(de_x, de_y, para_x, para_y)
            self.historico_jogadas.append((de_x, de_y, para_x, para_y, peca_capturada, foi_promovida, peca.dama))
            self.trocar_jogador()
            return True
        return False

    def desfazer_jogada(self):
        if self.historico_jogadas:
            de_x, de_y, para_x, para_y, peca_capturada, foi_promovida, era_dama = self.historico_jogadas.pop()
            peca = self.tabuleiro.obter_peca(para_x, para_y)
            self.tabuleiro.mover_peca(para_x, para_y, de_x, de_y)
            peca.dama = era_dama
            if peca_capturada:
                self.tabuleiro.tabuleiro[(de_x + para_x) // 2][(de_y + para_y) // 2] = peca_capturada
            self.trocar_jogador()

    def jogada_ia(self):
        melhor_jogada = self.ia_avancada.obter_melhor_jogada(self.dificuldade)
        if melhor_jogada:
            de_x, de_y, para_x, para_y = melhor_jogada
            self.fazer_jogada(de_x, de_y, para_x, para_y)
            return melhor_jogada
        return None

    def verificar_vitoria(self):
        pecas_brancas = pecas_pretas = 0
        for linha in self.tabuleiro.tabuleiro:
            for peca in linha:
                if peca:
                    if peca.cor == "branca":
                        pecas_brancas += 1
                    else:
                        pecas_pretas += 1
        if pecas_brancas == 0:
            return "preta"
        elif pecas_pretas == 0:
            return "branca"
        return None

    def obter_movimentos_validos(self, x, y):
        movimentos_validos = []
        peca = self.tabuleiro.obter_peca(x, y)
        if peca:
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in direcoes:
                if self.movimento_valido(x, y, x + dx, y + dy):
                    movimentos_validos.append((x, y, x + dx, y + dy))
                if self.movimento_valido(x, y, x + 2*dx, y + 2*dy):
                    movimentos_validos.append((x, y, x + 2*dx, y + 2*dy))
        return movimentos_validos

    def fazer_jogada(self, de_x, de_y, para_x, para_y):
        if self.movimento_valido(de_x, de_y, para_x, para_y):
            peca_capturada = self.tabuleiro.obter_peca((de_x + para_x) // 2, (de_y + para_y) // 2) if abs(de_x - para_x) == 2 else None
            foi_promovida = self.tabuleiro.mover_peca(de_x, de_y, para_x, para_y)
            self.historico_jogadas.append((de_x, de_y, para_x, para_y, peca_capturada, foi_promovida))
            self.trocar_jogador()
            return True
        return False

    def desfazer_jogada(self):
        if self.historico_jogadas:
            de_x, de_y, para_x, para_y, peca_capturada, foi_promovida = self.historico_jogadas.pop()
            peca = self.tabuleiro.mover_peca(para_x, para_y, de_x, de_y)
            if foi_promovida:
                peca.dama = False
            if peca_capturada:
                self.tabuleiro.tabuleiro[(de_x + para_x) // 2][(de_y + para_y) // 2] = peca_capturada
            self.trocar_jogador()

    def jogada_ia(self):
        melhor_jogada = self.ia_avancada.obter_melhor_jogada(self.dificuldade)
        if melhor_jogada:
            de_x, de_y, para_x, para_y = melhor_jogada
            self.fazer_jogada(de_x, de_y, para_x, para_y)
            return melhor_jogada
        return None

    def verificar_vitoria(self):
        pecas_brancas = pecas_pretas = 0
        for linha in self.tabuleiro.tabuleiro:
            for peca in linha:
                if peca:
                    if peca.cor == "branca":
                        pecas_brancas += 1
                    else:
                        pecas_pretas += 1
        if pecas_brancas == 0:
            return "preta"
        elif pecas_pretas == 0:
            return "branca"
        return None

    def obter_movimentos_possiveis(self, cor):
        return self.ia_avancada.obter_todos_movimentos(cor)