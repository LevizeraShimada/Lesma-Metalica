import pygame
# from obj import Player, Bg, Dirt, Rock
from Jogo import Jogo
import pyautogui

X, Y = pyautogui.size()
pygame.mixer.init()
pygame.mixer.music.load('assets/SONGS/SONG_3.mpeg')
pygame.mixer.music.set_volume(0.09)
pygame.mixer.music.play(-1)


class Main:

    def __init__(self):

        # Definição de tela
        self.window = pygame.display.set_mode([X * 0.85, Y * 0.85])
        pygame.display.set_caption("Lesma Metálica")
        self.loop = True
        self.fps = pygame.time.Clock()

        self.jogo = Jogo()

    def draw(self):
        self.jogo.draw(self.window)

    def evento(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.loop = False

    def update(self):
        while self.loop:
            self.draw()
            self.evento()
            self.jogo.update()
            pygame.display.update()
            self.fps.tick(30)


Main().update()
