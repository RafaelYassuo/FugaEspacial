"""
Jogo: Fuga Espacial
Descrição: Um grupo de diplomatas escapam de uma fortaleza estelar a bordo de uma nave danificada.
    A nave precisa se desviar das ameaças e sobreviver até atingir a zona de segurança diplomática.
"""
import sys

import pygame
import time
import random
import math
import os
import sys


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Background:
    """
    Esta classe define o plano de fundo do jogo
    """
    image = None         # Atributo
    margin_left = None   # Atributo
    margin_right = None  # Atributo
    x = None
    y = None

    def __init__(self):

        background_fig = pygame.image.load("Images/background.png")
        background_fig.convert()
        background_fig = pygame.transform.scale(background_fig, (800, 602))
        self.image = background_fig   # Atribui imagem para o background

        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60,602))
        self.margin_right = margin_right_fig

    # __init__()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))              # imagem do background para tela
        screen.blit(self.margin_left, (0, 0))       # 60 depois da primeira margem
        screen.blit(self.margin_right, (740, 0))    # 60 depois da segunda margem
    # draw()

    def draw_freedom(self, screen):
        screen.blit(self.image, (0, 0))

    # Define posições do Plano de Fundo para criar o movimento
    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):

        for i in range(0, 2):
            screen.blit(self.image, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_left, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_right, (movR_x, movR_y - i * scr_height))
    # move()
# Background

class Player:
    """
    Esta classe define o Jogador
    """
    image = None
    x = None
    y = None

    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y

    # __init__()

    # Desenhar Player
    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def move(self, mudar_x, mudar_y):
        # movimentação do player
        # altera a coordenada x e y da nave de acordo com as mudanças no handle events da classe game
        self.x += mudar_x
        self.y += mudar_y

class Hazard:

    image = None
    x = None
    y = None

    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y

    # __init__()

    # desenhar hazard
    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

# Hazard:

class Soundtrack:
    soundtrack = None
    sound = None

    def __init__(self, soundtrack):
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + "not found..ignored", file=sys.stderr)

    def play(self):
        pygame.mixer.music.load(self.soundtrack)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)

    def set(self, soundtrack):
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + "not found..ignored", file=sys.stderr)

    def play_sound(self, sound):
        # Som
        if os.path.isfile(sound):
            self.sound = sound
            pygame.mixer.music.load(sound)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        else:
            print(sound + "not found..ignored", file=sys.stderr)

class Bonus:

    image = None
    x = None
    y = None

    def __init__(self, x, y):
        bonus_fig = pygame.image.load("Images/bonusStar.png")
        bonus_fig.convert()
        bonus_fig = pygame.transform.scale(bonus_fig, (35, 35))
        self.image = bonus_fig
        self.x = x
        self.y = y

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

class Game:
    screen = None
    screen_size = None
    width = 800
    height = 600     # inicializar atributos
    run = True
    background = None
    player = None
    hazard = []
    bonus = None
    screen1 = pygame.display.set_mode((width, height))

    # movimento do player
    mudar_x = 0.0
    mudar_y = 0.0

    pygame.display.set_caption("Menu")

    start_img = pygame.image.load("Menu/start_btn.png").convert()
    exit_img = pygame.image.load("Menu/exit_btn.png").convert()

    start_button = Button(100, 200, start_img, 0.8)
    exit_button = Button(450, 200, exit_img, 0.8)

    run_menu = True
    while run_menu:


        if start_button.draw(screen1):
            run_menu = False
        if exit_button.draw(screen1):
            pygame.quit()

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    pygame.quit()

    def __init__(self, size, fullscreen):   # operações

        """
        Função que inicializa o pygame, define a resolução da tela,
        caption e desabilita o mouse.
        """
        pygame.init()   # inicializar o pygame

        self.screen = pygame.display.set_mode((self.width, self.height))   #tamanho da tela
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible(0)   #desabilitar o mouse
        pygame.display.set_caption('Fuga Espacial')


    # init()

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False            # tratar saída do jogo

            # se clicar em qualquer tecla, entra no if
            if event.type == pygame.KEYDOWN:

                # se clicar na seta da esquerda, anda 3 para esquerda no eixo x
                if event.key == pygame.K_LEFT:
                    self.mudar_x = -7

                # se clicar na seta direita, anda 3 para direita no eixo x
                elif event.key == pygame.K_RIGHT:
                    self.mudar_x = 7

                # se clicar na seta para cima, anda 3 para cima no eixo y
                elif event.key == pygame.K_UP:
                    self.mudar_y = -7

                # se clicar na seta para baixa, anda 3 para baixo no eixo y
                elif event.key == pygame.K_DOWN:
                    self.mudar_y = 10

                elif event.key == pygame.K_ESCAPE:
                    self.game_pause = True


            # se soltar qualquer tecla, não faz nada
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.mudar_x = 0

                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    self.mudar_y = 0

    #handle_events()

    def elements_draw(self):                # desenhar elementos
        self.background.draw(self.screen)
    # elements_draw()

    # Informa a quantidade de hazard que passaram e a pontuação
    def score_card(self, screen,passou, score):
        font = pygame.font.Font("Fonts/Fonte3.ttf", 25)
        #passou = font.render("Passou: " + str(passou), True, (255, 255, 128))
        score = font.render("Score: " + str(score), True, (253, 231, 32))
        #screen.blit(passou, (61, 50))
        screen.blit(score, (61, 20))

    def draw_explosion(self, screen, x, y):
        explosion_fig = pygame.image.load("Images/explosion.png")
        explosion_fig.convert()
        explosion_fig = pygame.transform.scale(explosion_fig, (150, 150))
        screen.blit(explosion_fig, (x, y))

    def write_message(self, message, R, G, B, x, y):
        my_font1 = pygame.font.Font("Fonts/Fonte4.ttf", 100)
        # Menagens para o jogador
        render_text = my_font1.render(message, False, (R, G, B))
        # desenha
        self.screen.blit(render_text, (x, y))

    def loop(self):
        """
        Laço principal
        """

        score = 0
        h_passou = 0

        #  variáveis para movimento de Plano de Fundo/Background
        velocidade_background = 7
        velocidade_hazard = 7

        # movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = 740
        movR_y = 0

        # Criar o plano de fundo
        self.background = Background()          # Criar objeto Background

        # Incluir trilha sonora
        #self.play_soundtrack()

        # Posicao do Player
        x = (self.width - 56) / 2
        y = self.height - 125

        # Posicao do bonus
        x1 = random.randrange(100, 665)
        y1 = random.randrange(50, 500)

        aux = x1
        auy = y1

        # Criar o Player
        self.player = Player(x, y)

        # Criar bonus
        self.bonus = Bonus(x1, y1)

        # localizalção
        hzrd = 0
        hr = 0
        h_x = random.randrange(125, 665)
        h_y = -500
        t_x = random.randrange(125, 665)
        t_y = -500
        self.timer = 0

        # info hazard
        h_height = 110 # 120 , 130 0 # 130 # 120

        # criar os hazards
        self.hazard.append(Hazard("Images/satelite.png", h_x, h_y))
        self.hazard.append(Hazard("Images/nave.png", h_x, h_y))
        self.hazard.append(Hazard("Images/cometaVermelho.png", h_x, h_y))
        self.hazard.append(Hazard("Images/meteoros.png", h_x, h_y))
        self.hazard.append(Hazard("Images/buracoNegro.png", h_x, h_y))

        self.hazard.append(Hazard("Images/nave2.png", t_x, t_y))
        self.hazard.append(Hazard("Images/meteor2.png", t_x, t_y))
        self.hazard.append(Hazard("Images/meteor3.png", t_x, t_y))
        self.hazard.append(Hazard("Images/meteor4.png", t_x, t_y))
        self.hazard.append(Hazard("Images/plat.png", t_x, t_y))
        self.hazard.append(Hazard("Images/plat2.png", t_x, t_y))

        # Criar trilha sonora
        self.soundtrack = Soundtrack("Sounds/themePrincipal.mp3")
        self.soundtrack.play()

        # Inicializar o relogio e o dt que vai limitar o valor de FPS do jogo
        clock = pygame.time.Clock()
        dt = 16                         # Inicializar o relogio e o dt

        # Inicio do loop principal do programa
        while self.run:
            clock.tick(1000/dt)   # número maximo de FPS

            # Handle input Events
            self.handle_events() # trata eventos

            # Desenha o background buffer
            self.elements_draw()  # Desenha elementos

            # adiciona movimento ao background
            self.background.move(self.screen, self.height, movL_x, movL_y, movR_x, movR_y)
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            # Altera a coordenada x e y de acordo com as mudanças no event_handle() para se mover
            self.player.move(self.mudar_x, self.mudar_y)

            # Desenhar Player
            self.player.draw(self.screen, self.player.x, self.player.y)

            # Mostrar score
            self.score_card(self.screen, h_passou, score)

            # Desenhar shot
            #self.shot.draw(self.screen, shot_x, shot_y)

            # se a imagem ultrapassar a extremidade da tela, move de volta
            if movL_y > 600 and movR_y > 600:
                movL_y -= 600
                movR_y -= 600

            # Restrições do movimento do Player
            # Se o Player bate na lateral não é Game Over
            if self.player.x > 760 - 92 or self.player.x < 40 + 5 or self.player.y > 600 or self.player.y < 0:
                # Som da colisão nas margens
                self.soundtrack.play_sound("Sounds/jump1.wav")

                # Exibe mensagem
                self.write_message("VOCÊ BATEU!", 255, 255, 255, 80, 200)

                pygame.display.update()   # atualiza a tela
                time.sleep(3)
                self.loop()
                self.run = False

            # adicionando movimento ao hazard
            h_y = h_y + velocidade_hazard / 4  # atualização de posição e velocidade
            self.hazard[hzrd].draw(self.screen, h_x, h_y)  # desenhando hazard
            h_y = h_y + velocidade_hazard

            # condiçao de contorno
            # definindo onde hazard vai aparecer, recomeçando a posição do obstaculo e da faixa
            if h_y > self.height:
                h_y = 0 - h_height
                h_x = random.randrange(50, 700 - h_height)
                hzrd = random.randint(0, 4)

                # determinando quantos hazard passaram e a pontuação
                h_passou = h_passou + 1
                score += 10

            # Ao chegar na velocidade 10 irá aparecer dois hazards de uma vez
            if velocidade_background >= 10:  # Adicionando mais hazards na tela

                t_y = t_y + velocidade_hazard / 4  # atualização de posição e velocidade
                self.hazard[hr].draw(self.screen, t_x, t_y)
                t_y = t_y + velocidade_hazard

                # determinando quantos hazard passaram e a pontuação
                if t_y > self.height:
                    h_passou = h_passou + 1
                    score += 10

                if t_y > self.height:
                    t_y = 0 - h_height
                    t_x = random.randrange(50, 700 - h_height)
                    hr = random.randint(5, 10)

                # Desenhar Bonus
                self.bonus.draw(self.screen, x1, y1)

            # Deixando o movimento dos hazard "aleatório"
            if hzrd == 0:  # satelite
                h_x = h_x + 3
                if h_x >= 620:
                    h_x = h_x - 3

            elif hzrd == 2:  # cometa vermelho
                h_x = h_x - 3
                if h_x <= 100:
                    h_x = h_x + 3

            elif hzrd == 1:  # nave
                self.timer += 0.04
                h_x = 250 + math.sin(self.timer) * 200

            """
            elif hzrd == 4:
                if self.ESQUERDA:
                    self.mudar_x += 0.25
                if self.DIREITA:
                    self.mudar_x -= 0.25
                if self.CIMA:
                    self.mudar_y -= 0.2
                else:
                    self.mudar_y += 0.2
            """

            # Colisão e Game Over
            player_rect = self.player.image.get_rect()
            player_rect.topleft = (self.player.x, self.player.y)
            bonus_rect = self.bonus.image.get_rect()
            bonus_rect.topleft = (x1, y1)

            if self.player.x + 50 > h_x and h_y + 100 > self.player.y and self.player.y + 50 > h_y\
                    and h_x + 100 > self.player.x:
                # Emite som da colisão
                self.soundtrack.play_sound("Sounds/crash.wav")

                # Exibe a imagem da explosão
                self.draw_explosion(self.screen, self.player.x - (self.player.image.get_width() / 2),
                self.player.y - (self.player.image.get_height() / 2))

                # Exibe mensagem de Game Over
                self.write_message("GAME OVER!", 255, 0, 0, 80, 200)

                pygame.display.update()
                time.sleep(3)
                self.loop()
                self.run = False

            elif self.player.x + 50 > t_x and t_y + 100 > self.player.y and self.player.y + 50 > t_y\
                    and t_x + 100 > self.player.x:
                # Emite som da colisão
                self.soundtrack.play_sound("Sounds/crash.wav")

                # Exibe a imagem da explosão
                self.draw_explosion(self.screen, self.player.x - (self.player.image.get_width() / 2),
                self.player.y - (self.player.image.get_height() / 2))

                # Exibe mensagem de Game Over
                self.write_message("GAME OVER!", 255, 0, 0, 80, 200)

                pygame.display.update()
                time.sleep(3)
                self.loop()
                self.run = False

            elif player_rect.colliderect(bonus_rect):
                # Player ganha mais score
                # self.soundtrack.play_sound("Sounds/star.wav")
                # self.write_message("+ 30", 255, 255, 255, aux, auy)
                score = score + 30
                x1 = random.randrange(100, 665)
                y1 = random.randrange(50, 500)

            velocidade_background += 0.005
            if score == 60:
                velocidade_hazard += 0.05

            # Atualiza a tela
            pygame.display.update()     # Atualiza a tela
            clock.tick(2000)

            # Vitória do jogador
            if score == 1000:

                # musica da vitoria
                self.soundtrack.play_sound("Sounds/winner.ogg")

                # Desenha area diplomatica
                self.background.draw_freedom(self.screen)

                # Escreve mensagem de vitoria
                self.write_message("1000 PONTOS", 255, 117, 24, 90, 100)
                self.write_message("VOCÊ VENCEU!", 255, 117, 24, 2, 300)

                pygame.display.update()
                time.sleep(4)
                self.run = False

        # while self.run
    # loop()

# Inicia o jogo: Cria o objeto game e chama o loop básico

game = Game("resolution","fullscreen") # instanciar o objeto jogo
game.loop()          # iniciar o jogo

# adicionar som e + 30 ao pegar bonus
# adicionar efeito ao buraco negro