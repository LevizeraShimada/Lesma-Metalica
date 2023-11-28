import pygame
import pyautogui

X, Y = pyautogui.size()
pygame.mixer.init()


class Obj(pygame.sprite.Sprite):

    def __init__(self, imagem, x, y, a, c, type, escalax, escalay, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(imagem)
        self.alt = a  # Altura do objeto
        self.comp = c  # Comprimento do objeto
        self.tipo = type
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scale = [escalax, escalay]

        if self.tipo == 'piso':
            self.image = pygame.transform.scale(self.image, (X * self.scale[0], Y * self.scale[1]))
            # Adequa a imagem para um tamanho cabível

            self.alt = a
            self.comp = c
            self.offput_x = 0
            self.offput_y = 40

            self.hitbox = pygame.Rect(x, y, self.comp, self.alt - 40)  # Teste de hitbox de objeto

        if self.tipo == 'obstaculo':
            self.image = pygame.transform.scale(self.image, (X * self.scale[0], Y * self.scale[1]))
            self.alt = a
            self.comp = c
            self.offput_x = 10
            self.offput_y = 0
            self.rect = self.image.get_rect(topleft=(x, y))
            self.hitbox = pygame.Rect(x, y, self.comp, self.alt)

        if self.tipo == 'plataforma':
            self.image = pygame.transform.scale(self.image, (X * self.scale[0], Y * self.scale[1]))
            self.alt = a
            self.comp = c
            self.offput_x = 0
            self.offput_y = 0
            self.rect = self.image.get_rect(topleft=(x, y))
            self.hitbox = pygame.Rect(x, y, self.comp, self.alt)

    def update(self, win):
        if self.tipo == 'piso':
            self.hitbox.topleft = (self.rect.x + self.offput_x, self.rect.y + self.offput_y)
            pygame.draw.rect(win, (255, 255, 255), self.hitbox, 1)

        if self.tipo == 'obstaculo':
            self.hitbox.topleft = (self.rect.x + self.offput_x, self.rect.y + self.offput_y)
            pygame.draw.rect(win, (255, 255, 255), self.hitbox, 1)

        if self.tipo == 'plataforma':
            self.hitbox.topleft = (self.rect.x + self.offput_x, self.rect.y + self.offput_y)
            pygame.draw.rect(win, (255, 255, 255), self.hitbox, 1)


class Bg(pygame.sprite.Sprite):

    def __init__(self, imagem, x, y, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(imagem)
        self.image = pygame.transform.scale(self.image, (X * 0.85, Y * 0.85))
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, a, c, type, *groups):
        super().__init__(*groups)

        if type == 'jogador':

            # Declaração das imagens estáticas do player
            self.images = [pygame.image.load(f'assets/PLAYER/IDLE/SOL{i}.png') for i in range(1, 6)]

            """OBS: A função "in range" dentro do "image.load" serve para pegar a extensão total de imagens dentro da pasta:
            IDLE/, utilizando a variável "i" para carregar imagens diferentes, dependendo do seu número final"""

            self.index = 0
            self.image = self.images[self.index]

            # Declaração das imagens de corrida do player
            self.images_run = [pygame.image.load(f'assets/PLAYER/MOVE/RUN{i}.png') for i in range(1, 8)]
            self.index_run = 0
            self.image_run = self.images_run[self.index_run]
            self.image_run = pygame.transform.scale(self.image_run, (X * 0.07, Y * 0.14))
            self.run_sound = pygame.mixer.Sound('assets/PLAYER/MOVE/FALL1.mp3')
            self.run_sound.set_volume(0.05)

            # Declaração das imagens de tiro do player
            self.images_shot = [pygame.image.load(f'assets/PLAYER/SHOOT/SHOOT{i}.png') for i in range(1, 4)]
            self.index_shot = 0
            self.image_shot = self.images_shot[self.index_shot]
            self.image_shot = pygame.transform.scale(self.image_shot, (X * 0.07, Y * 0.14))
            self.shooting = False
            self.shot_duration = 75  # Duração do tiro
            self.shot_timer = 0
            self.shot_sound = pygame.mixer.Sound('assets/PLAYER/SHOOT/SHOT.mp3')
            self.shot_sound.set_volume(0.3)

            # Declaração das imagens de pulo do player
            self.images_jump = pygame.image.load(f'assets/PLAYER/JUMP/JUMP1.png')
            self.index_jump = 1
            self.image_jump = self.images_jump
            self.image_jump = pygame.transform.scale(self.image_jump, (X * 0.07, Y * 0.14))

            # Variáveis para a  checagem de Hitbox
            self.alt = a
            self.comp = c
            self.w = 1500
            self.h = y
            self.rect = self.image.get_rect(topleft=(x, y))
            self.hitbox = pygame.Rect(x, y, self.comp, self.alt)

            # Variáveis para o pulo/gravidade
            self.jspeed = 0
            self.jump_limit = -15
            self.is_jumping = False
            self.idle = True
            self.speed = 5

            self.flip = False
            self.flip_shoot = False
            self.movement_anim_timer = pygame.time.get_ticks()
            self.movement_anim_speed = 100  # Ajuste para a animação correndo (Quanto maior, mais lento)
            self.idle_anim_timer = pygame.time.get_ticks()
            self.idle_anim_speed = 100  # Ajuste para a animação imóvel (Quanto maior, mais lento)

    # Função de animações
    def update_animation(self):
        keys = pygame.key.get_pressed()

        # Animação de pulo
        if self.is_jumping:
            self.image = self.images_jump
            self.image = pygame.transform.scale(self.image, (X * 0.07, Y * 0.145))
            if self.flip:
                self.image = self.images_jump
                self.image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.scale(self.image, (X * 0.07, Y * 0.135))
                self.flip = True
            else:
                self.image = pygame.transform.flip(self.image, False, False)
                self.flip = False

        # Para animação de movimento/ correr para a direita e esquerda
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if pygame.time.get_ticks() - self.movement_anim_timer > self.movement_anim_speed:
                self.index_run += 1
                if self.index_run == 4 and not self.is_jumping:
                    self.run_sound.play(0)
                if self.index_run >= len(self.images_run):
                    self.index_run = 0
                    self.run_sound.play(0)
                self.image = self.images_run[self.index_run]
                self.image = pygame.transform.scale(self.image, (int(X * 0.07), int(Y * 0.14)))
                if keys[pygame.K_LEFT]:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = True
                elif keys[pygame.K_RIGHT]:
                    self.image = pygame.transform.flip(self.image, False, False)
                    self.flip = False
                self.movement_anim_timer = pygame.time.get_ticks()

        # Animação de tiro
        elif keys[pygame.K_SPACE]:
            if not self.shooting:  # Se o personagem não estiver atirando/começar a atirar, entrar IF
                if pygame.time.get_ticks() - self.shot_timer > self.shot_duration:
                    self.index_shot += 1
                    if self.index_shot == 2:
                        self.shot_sound.play(0)
                        # Som de tiro
                    if self.index_shot >= len(self.images_shot):
                        self.index_shot = 0
                    self.image = self.images_shot[self.index_shot]
                    self.image = pygame.transform.scale(self.image, (X * 0.085, Y * 0.14))
                    # Foi ajustado o tamanho do X, pela imagem do tiro ser mais larga que a de idle/corrida

                    self.movement_anim_timer = pygame.time.get_ticks()
                    self.flip_shoot = False
                    if self.flip:
                        self.flip_shoot = True
                        self.image = pygame.transform.flip(self.image, True, False)

                    self.shooting = True
                    self.shot_timer = pygame.time.get_ticks()

            else:
                if pygame.time.get_ticks() - self.shot_timer > self.shot_duration:
                    self.shooting = False

        # Animação estática/personagem parado
        else:
            if pygame.time.get_ticks() - self.idle_anim_timer > self.idle_anim_speed:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
                self.image = pygame.transform.scale(self.image, (X * 0.07, Y * 0.14))
                self.idle_anim_timer = pygame.time.get_ticks()
                if self.flip:  # Vira a imagem estática para a esquerda
                    self.image = pygame.transform.flip(self.image, True, False)
                self.idle_anim_timer = pygame.time.get_ticks()

    def update(self, win):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and not self.is_jumping:
            self.jspeed = self.jump_limit
            self.is_jumping = True

        self.rect.y += self.jspeed

        if self.is_jumping:
            self.jspeed += 0.7

        if self.rect.y >= self.h:
            self.rect.y = self.h
            self.is_jumping = False
            self.jspeed = 0

        if self.flip_shoot:
            self.hitbox.topleft = (self.rect.x + 70, self.rect.y)
            # pygame.draw.rect(win, (255, 255, 255), self.hitbox, 1)
            if pygame.KEYUP:
                self.flip_shoot = False

        if keys[pygame.K_p]:
            pygame.mixer.music.stop()
            pygame.display.flip()
            self.hitbox.topleft = (self.rect.x + 30, self.rect.y)
            self.update_animation()

        else:
            self.update_animation()
