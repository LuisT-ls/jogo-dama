import pygame
import sys
from jogo import Jogo

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, cor_hover, acao):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_hover = cor_hover
        self.acao = acao
        self.fonte = pygame.font.Font(None, 36)

    def desenhar(self, tela):
        cor_atual = self.cor_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.cor
        pygame.draw.rect(tela, cor_atual, self.rect)
        texto_surface = self.fonte.render(self.texto, True, (255, 255, 255))
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)

    def checar_clique(self, pos):
        return self.rect.collidepoint(pos)

class InterfaceGrafica:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 800
        self.tamanho_quadrado = self.largura // 8
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Jogo de Damas")
        self.jogo = None
        self.fonte = pygame.font.Font(None, 36)
        self.menu_ativo = True
        self.selecao_modo = False
        self.selecao_dificuldade = False
        self.posicao_selecionada = None
        self.movimentos_validos = []
        self.botoes_menu = [
            Botao(300, 300, 200, 50, "Jogar", (0, 128, 0), (0, 200, 0), self.mostrar_selecao_modo),
            Botao(300, 375, 200, 50, "Opções", (0, 0, 128), (0, 0, 200), self.mostrar_opcoes),
            Botao(300, 450, 200, 50, "Sair", (128, 0, 0), (200, 0, 0), sys.exit)
        ]
        self.botoes_modo = [
            Botao(250, 300, 300, 50, "Jogador vs Jogador", (0, 128, 0), (0, 200, 0), lambda: self.iniciar_jogo("pvp")),
            Botao(250, 375, 300, 50, "Jogador vs IA", (0, 0, 128), (0, 0, 200), self.mostrar_selecao_dificuldade),
            Botao(250, 450, 300, 50, "Voltar", (128, 0, 0), (200, 0, 0), self.voltar_ao_menu)
        ]
        self.botoes_dificuldade = [
            Botao(250, 200, 300, 50, "Muito Fácil", (0, 255, 0), (0, 200, 0), lambda: self.iniciar_jogo("pvia", "muito fácil")),
            Botao(250, 275, 300, 50, "Fácil", (0, 200, 0), (0, 150, 0), lambda: self.iniciar_jogo("pvia", "fácil")),
            Botao(250, 350, 300, 50, "Médio", (0, 150, 0), (0, 100, 0), lambda: self.iniciar_jogo("pvia", "médio")),
            Botao(250, 425, 300, 50, "Difícil", (0, 100, 0), (0, 50, 0), lambda: self.iniciar_jogo("pvia", "difícil")),
            Botao(250, 500, 300, 50, "Muito Difícil", (0, 50, 0), (0, 25, 0), lambda: self.iniciar_jogo("pvia", "muito difícil")),
            Botao(250, 575, 300, 50, "Especialista", (0, 0, 0), (50, 50, 50), lambda: self.iniciar_jogo("pvia", "especialista")),
            Botao(250, 650, 300, 50, "Voltar", (128, 0, 0), (200, 0, 0), self.voltar_selecao_modo)
        ]
        self.animacao_ativa = False
        self.peca_animada = None
        self.pos_inicial = None
        self.pos_final = None
        self.modo_jogo = None
        self.progresso_animacao = 0
        self.velocidade_animacao = 0.05

    def mostrar_selecao_modo(self):
        self.menu_ativo = False
        self.selecao_modo = True
        self.selecao_dificuldade = False

    def mostrar_selecao_dificuldade(self):
        self.menu_ativo = False
        self.selecao_modo = False
        self.selecao_dificuldade = True

    def voltar_ao_menu(self):
        self.menu_ativo = True
        self.selecao_modo = False
        self.selecao_dificuldade = False

    def voltar_selecao_modo(self):
        self.menu_ativo = False
        self.selecao_modo = True
        self.selecao_dificuldade = False

    def iniciar_jogo(self, modo, dificuldade="médio"):
        self.jogo = Jogo(modo, dificuldade)
        self.modo_jogo = modo
        self.menu_ativo = False
        self.selecao_modo = False
        self.selecao_dificuldade = False
        print(f"Iniciando jogo no modo: {modo}, dificuldade: {dificuldade}")

    def executar_jogada_ia(self):
        print("IA está fazendo uma jogada...")
        jogada = self.jogo.jogada_ia()
        if jogada:
            de_x, de_y, para_x, para_y = jogada
            print(f"IA moveu de ({de_x}, {de_y}) para ({para_x}, {para_y})")
            self.iniciar_animacao(de_x, de_y, para_x, para_y)
        else:
            print("A IA não conseguiu fazer uma jogada válida.")

    def mostrar_opcoes(self):
        print("Opções (a ser implementado)")

    def desenhar_menu(self):
        self.tela.fill((255, 255, 255))
        titulo = self.fonte.render("Jogo de Damas", True, (0, 0, 0))
        self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 100))
        for botao in self.botoes_menu:
            botao.desenhar(self.tela)

    def desenhar_selecao_modo(self):
        self.tela.fill((255, 255, 255))
        titulo = self.fonte.render("Selecione o Modo de Jogo", True, (0, 0, 0))
        self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 100))
        for botao in self.botoes_modo:
            botao.desenhar(self.tela)

    def desenhar_tabuleiro(self):
        for i in range(8):
            for j in range(8):
                cor = (255, 206, 158) if (i + j) % 2 == 0 else (209, 139, 71)
                pygame.draw.rect(self.tela, cor, (j * self.tamanho_quadrado, i * self.tamanho_quadrado, self.tamanho_quadrado, self.tamanho_quadrado))
                
                # Desenha os indicadores de movimento válido
                if (i, j) in self.movimentos_validos:
                    pygame.draw.circle(self.tela, (0, 255, 0), 
                                       (j * self.tamanho_quadrado + self.tamanho_quadrado // 2, 
                                        i * self.tamanho_quadrado + self.tamanho_quadrado // 2), 
                                       10)

    def desenhar_pecas(self):
        for i in range(8):
            for j in range(8):
                peca = self.jogo.tabuleiro.obter_peca(i, j)
                if peca:
                    cor = (255, 255, 255) if peca.cor == "branca" else (0, 0, 0)
                    pygame.draw.circle(self.tela, cor, 
                                       (j * self.tamanho_quadrado + self.tamanho_quadrado // 2, 
                                        i * self.tamanho_quadrado + self.tamanho_quadrado // 2), 
                                       self.tamanho_quadrado // 2 - 10)
                    if peca.dama:
                        pygame.draw.circle(self.tela, (255, 0, 0) if peca.cor == "branca" else (255, 255, 0), 
                                           (j * self.tamanho_quadrado + self.tamanho_quadrado // 2, 
                                            i * self.tamanho_quadrado + self.tamanho_quadrado // 2), 
                                           10)

    def desenhar_peca(self, peca, x, y):
        cor = (255, 255, 255) if peca.cor == "branca" else (0, 0, 0)
        pygame.draw.circle(self.tela, cor, (x, y), self.tamanho_quadrado // 2 - 10)
        if peca.dama:
            texto = self.fonte.render("D", True, (255, 0, 0) if peca.cor == "branca" else (255, 255, 0))
            self.tela.blit(texto, (x - 10, y - 10))

    def exibir_jogador_atual(self):
        texto = self.fonte.render(f"Jogador atual: {self.jogo.jogador_atual}", True, (0, 0, 0))
        self.tela.blit(texto, (10, self.altura - 40))

    def obter_posicao_clique(self, pos):
        x, y = pos
        return y // self.tamanho_quadrado, x // self.tamanho_quadrado

    def iniciar_animacao(self, de_x, de_y, para_x, para_y):
        peca = self.jogo.tabuleiro.obter_peca(de_x, de_y)
        if peca is None:
            print(f"Erro: Não há peça na posição ({de_x}, {de_y})")
            return
        self.animacao_ativa = True
        self.peca_animada = peca
        self.pos_inicial = (de_y * self.tamanho_quadrado + self.tamanho_quadrado // 2, de_x * self.tamanho_quadrado + self.tamanho_quadrado // 2)
        self.pos_final = (para_y * self.tamanho_quadrado + self.tamanho_quadrado // 2, para_x * self.tamanho_quadrado + self.tamanho_quadrado // 2)
        self.progresso_animacao = 0

    def atualizar_animacao(self):
        if self.animacao_ativa and self.peca_animada:
            self.progresso_animacao += self.velocidade_animacao
            if self.progresso_animacao >= 1:
                self.animacao_ativa = False
                de_x, de_y = self.pos_inicial[1] // self.tamanho_quadrado, self.pos_inicial[0] // self.tamanho_quadrado
                para_x, para_y = self.pos_final[1] // self.tamanho_quadrado, self.pos_final[0] // self.tamanho_quadrado
                self.jogo.fazer_jogada(de_x, de_y, para_x, para_y)
                self.peca_animada = None
            else:
                x = self.pos_inicial[0] + (self.pos_final[0] - self.pos_inicial[0]) * self.progresso_animacao
                y = self.pos_inicial[1] + (self.pos_final[1] - self.pos_inicial[1]) * self.progresso_animacao
                self.desenhar_peca(self.peca_animada, x, y)


    def executar_jogada_ia(self):
        print("IA está fazendo uma jogada...")
        jogada = self.jogo.jogada_ia()
        if jogada:
            de_x, de_y, para_x, para_y = jogada
            print(f"IA moveu de ({de_x}, {de_y}) para ({para_x}, {para_y})")
            self.iniciar_animacao(de_x, de_y, para_x, para_y)
        else:
            print("A IA não conseguiu fazer uma jogada válida.")

    def desenhar_selecao_dificuldade(self):
        self.tela.fill((255, 255, 255))
        titulo = self.fonte.render("Selecione a Dificuldade", True, (0, 0, 0))
        self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 100))
        for botao in self.botoes_dificuldade:
            botao.desenhar(self.tela)


    def executar(self):
        rodando = True
        clock = pygame.time.Clock()

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and not self.animacao_ativa:
                    pos = pygame.mouse.get_pos()
                    if self.menu_ativo:
                        for botao in self.botoes_menu:
                            if botao.checar_clique(pos):
                                botao.acao()
                    elif self.selecao_modo:
                        for botao in self.botoes_modo:
                            if botao.checar_clique(pos):
                                botao.acao()
                    elif self.selecao_dificuldade:
                        for botao in self.botoes_dificuldade:
                            if botao.checar_clique(pos):
                                botao.acao()
                    elif self.jogo:
                        if self.modo_jogo == "pvia" and self.jogo.jogador_atual == "preta":
                            continue
                        linha, coluna = self.obter_posicao_clique(pos)
                        if self.posicao_selecionada is None:
                            peca = self.jogo.tabuleiro.obter_peca(linha, coluna)
                            if peca and peca.cor == self.jogo.jogador_atual:
                                self.posicao_selecionada = (linha, coluna)
                                self.movimentos_validos = self.jogo.obter_movimentos_validos(linha, coluna)
                        else:
                            de_x, de_y = self.posicao_selecionada
                            para_x, para_y = linha, coluna
                            if (de_x, de_y, para_x, para_y) in self.movimentos_validos:
                                self.iniciar_animacao(de_x, de_y, para_x, para_y)
                            self.posicao_selecionada = None
                            self.movimentos_validos = []

            self.tela.fill((255, 255, 255))

            if self.menu_ativo:
                self.desenhar_menu()
            elif self.selecao_modo:
                self.desenhar_selecao_modo()
            elif self.selecao_dificuldade:
                self.desenhar_selecao_dificuldade()
            elif self.jogo:
                self.desenhar_tabuleiro()
                self.desenhar_pecas()
                self.exibir_jogador_atual()
                self.atualizar_animacao()

                if not self.animacao_ativa:
                    vencedor = self.jogo.verificar_vitoria()
                    if vencedor:
                        self.exibir_vencedor(vencedor)
                    elif self.modo_jogo == "pvia" and self.jogo.jogador_atual == "preta":
                        self.executar_jogada_ia()

            pygame.display.flip()
            clock.tick(60) # Limita a 60 quadros por segundo

        pygame.quit()
        sys.exit()