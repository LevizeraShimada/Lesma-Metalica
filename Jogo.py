from obj import Player, Obj, Bg
import pygame
import pyautogui

X, Y = pyautogui.size()
print(X, Y)

all_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Listas para testes no PC local, ajustes por conta do tamanho da tela

PC_LOCAL_PLAYER = [120, 470, 100, 30]  # Posição x, y/ Comprimento, altura
PC_UNASP_PLAYER = [120, 670]

PC_LOCAL_PLAT = [0, 550, 120, 1500]
PC_UNASP_PLAT = [0, 775, 55, 55]

PC_LOCAL_PEDRA = [300, 530, 50, 50]
PC_UNASP_PEDRA = [300, 760]


class Jogo:

    def __init__(self):
        self.window = pygame.display.set_mode([X * 0.85, Y * 0.85])
        self.all_assets = pygame.sprite.Group()
        self.all_platforms = pygame.sprite.Group()

        self.bg1 = Bg("assets/BG_FOREST.png", 0, 0, self.all_assets)

        """self.platform1 = Dirt(self.window, "assets/DIRT_PLATUP2.png", PC_UNASP_PLAT[0], PC_UNASP_PLAT[1],
                              PC_LOCAL_PLAT[2], PC_LOCAL_PLAT[3], self.all_assets)"""
        # Teste - PC Faculdade

        self.platform1 = Obj("assets/DIRT_PLATUP2.png", PC_LOCAL_PLAT[0], PC_LOCAL_PLAT[1],
                             PC_LOCAL_PLAT[2], PC_LOCAL_PLAT[3], 'piso', 1, 0.15, self.all_assets, obstacles_group)

        self.platform2 = Obj("assets/TREE_P.png", 500, 425,
                             25, 75, 'plataforma', 0.05, 0.2, self.all_platforms, obstacles_group)

        self.platform2 = Obj("assets/TREE_P_T.png", 565, 435,
                             25, 75, 'plataforma', 0.05, 0.05, self.all_platforms, obstacles_group)

        self.platform3 = Obj("assets/TREE_P_T.png", 625, 435,
                             25, 75, 'plataforma', 0.05, 0.05, self.all_platforms, obstacles_group)

        self.platform4 = Obj("assets/TREE_P_T.png", 685, 435,
                             25, 75, 'plataforma', 0.05, 0.05, self.all_platforms, obstacles_group)

        self.platform5 = Obj("assets/TREE_P_T.png", 745, 435,
                             25, 75, 'plataforma', 0.05, 0.05, self.all_platforms, obstacles_group)

        self.platform6 = Obj("assets/TREE_P_T.png", 805, 435,
                             25, 75, 'plataforma', 0.05, 0.05, self.all_platforms, obstacles_group)

        self.platform7 = Obj("assets/TREE_P.png", 865, 425,
                             25, 75, 'plataforma', 0.05, 0.2, self.all_platforms, obstacles_group)
        # Teste em casa - PC LOCAL

        # self.rock = Rock("assets/ROCK.png", PC_UNASP_PEDRA[0], PC_UNASP_PEDRA[1], 65, 60, self.all_assets)
        # Teste - PC Faculdade

        """self.rock = Obj("assets/ROCK.png", PC_LOCAL_PEDRA[0], PC_LOCAL_PEDRA[1],
                        PC_LOCAL_PEDRA[2], PC_LOCAL_PEDRA[3], 'obstaculo', 0.05, 0.08,
                        self.all_assets, obstacles_group)
        # Teste em casa - PC LOCAL"""

        # all_sprites.add(self.platform1, self.platform2, self.rock)
        # self.player = Player(PC_UNASP_PLAYER[0], PC_UNASP_PLAYER[1], 60, 140, 'jogador', self.all_assets)
        # Teste - PC Faculdade

        self.player = Player(PC_LOCAL_PLAYER[0], PC_LOCAL_PLAYER[1], PC_LOCAL_PLAYER[2], PC_LOCAL_PLAYER[3],
                             'jogador', self.all_assets, player_group)
        # Teste em casa - PC LOCAL
        # all_sprites.add(self.player)

    def draw(self, window):
        self.all_assets.draw(window)
        self.all_platforms.draw(window)

    def check_collisions(self):
        for obstacle in obstacles_group:
            if self.player.rect.colliderect(obstacle.rect):
                if self.player.jspeed > 0:
                    # Player caindo
                    self.player.rect.bottom = obstacle.rect.y
                    self.player.is_jumping = False

                if self.player.jspeed == 0:
                    if self.player.rect.left > obstacle.rect.left:
                        if self.player.rect.y < obstacle.rect.bottom:
                            pass
                        elif self.player.rect.y > obstacle.rect.top:
                            self.player.rect.right = obstacle.rect.left
                            self.player.rect.y = obstacle.rect.top

                    elif self.player.rect.right < obstacle.rect.right:
                        if self.player.rect.y < obstacle.rect.bottom:
                            pass
                        elif self.player.rect.y > obstacle.rect.top:
                            self.player.rect.left = obstacle.rect.right
                            self.player.rect.y = obstacle.rect.top

        if pygame.sprite.spritecollide(self.player, obstacles_group, False):
            pass

    def update(self):
        self.all_assets.update(self.window)
        self.player.update(self.window)
        self.check_collisions()
