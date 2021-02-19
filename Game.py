import os.path

import pygame
import pygame_menu
from pygame.locals import *

import math
import time

import random

class Game(object):

    def __init__(self):
        self.sound = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((640, 400))
        self.fond = pygame.image.load("img/util/earth.png").convert()
        self.fondrect = self.fond.get_rect()

    # Fonction principale du jeu
    def main(self):
        pygame.init()
        self.draw_menu_screen()
        pygame.quit()

    # Reinitialisation du jeu
    def setup(self):
        self.closingGame = False
        self.score = 0
        self.ship = Ship(pygame.image.load(
            "img/ships/ship.gif").convert(), self.screen, self.sound)
        self.ship.rect.y = 400 - 25
        self.fond = pygame.image.load("img/util/earth.png").convert()
        self.fondrect = self.fond.get_rect()
        self.explosion = -20
        self.enemies = []
        self.enemies.append(Enemy(self.screen, {"x": 0, "y": 0}, self.sound))
        self.enemies.append(Enemy(self.screen, {"x": 200, "y": 0}, self.sound))
        self.enemies.append(Enemy(self.screen, {"x": 400, "y": 0}, self.sound))

    def draw_menu_screen(self):
        menu = pygame_menu.Menu(400, 640, 'Space-invader',
                                theme=pygame_menu.themes.THEME_DARK)
        menu.add_text_input('Pseudo :', default='USER')
        menu.add_selector(
            'Difficulty : ', [('Facile', 1), ('Intermediaire', 2), ('Difficile', 3)], onchange=set_difficulty)
        menu.add_selector(
            'Son : ', [('Sans', 1, False), ('Avec', 2, True)], onchange=set_sound)
        menu.add_button('Jouer', self.start_the_game)
        menu.add_button('Quitter', pygame_menu.events.EXIT)
        menu.mainloop(self.screen, bgfun=self.draw_background)

    def start_the_game(self):
        self.setup()
        self.main_loop()

    # Boucle de jeu
    def main_loop(self):
        while not self.closingGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closingGame = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        self.closingGame = True

            for obj in self.enemies:
                obj.update()

            self.update_kills()
            self.game_over()
            self.ship.update()

            if len(self.enemies) == 0:
                self.invoqueEnnemies()

            self.draw_game_screen()

    def update_kills(self):
        for allyMissile in self.ship.missiles:
            for enemy in self.enemies:
                if(pygame.sprite.collide_rect(allyMissile, enemy)):
                    self.ship.missiles.remove(allyMissile)
                    self.enemies.remove(enemy)
                    self.score += 1
                    break

        if(self.ship.invincibility > 0):
            self.ship.invincibility -= 1
        else:
            for enemy in self.enemies:
                if(self.ship.invincibility == 0):
                    for enemyMissile in enemy.missiles:
                        if(pygame.sprite.collide_rect(enemyMissile, self.ship)):
                            self.ship.lives -= 1
                            self.ship.invincibility = 100
                            break
                    if(pygame.sprite.collide_rect(enemy, self.ship)):
                        self.ship.lives -= 1
                        self.ship.invincibility = 100
                        break

    def game_over(self):
        if self.ship.lives < 1:
            if(self.explosion < 0):
                self.explosion = 1400

            if(self.explosion >= 0):
                if(self.explosion == 1400):
                    self.ship.image = pygame.image.load("img/util/explode_1.gif").convert()
                elif(self.explosion == 1200):
                    self.ship.image = pygame.image.load("img/util/explode_2.gif").convert()
                elif(self.explosion == 1000):
                    self.ship.image = pygame.image.load("img/util/explode_3.gif").convert()
                elif(self.explosion == 800):
                    self.ship.image = pygame.image.load("img/util/explode_4.gif").convert()
                elif(self.explosion == 600):
                    self.ship.image = pygame.image.load("img/util/explode_5.gif").convert()
                elif(self.explosion == 400):
                    self.ship.image = pygame.image.load("img/util/explode_6.gif").convert()
                elif(self.explosion == 200):
                    self.ship.image = pygame.image.load("img/util/explode_7.gif").convert()
                elif(self.explosion == 0):
                    self.ship.image = pygame.image.load("img/util/explode_8.gif").convert()

                    self.fond = pygame.image.load("img/util/explode.gif").convert()
                    self.fond = pygame.transform.scale(
                        self.fond, (640, 400))
                    self.screen.blit(self.fond, self.fondrect)

                    font = pygame.font.Font('freesansbold.ttf', 80)
                    text = font.render('GAME OVER', True, (255, 255, 255), (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (320, 200)
                    self.screen.blit(text, textRect)

                    font = pygame.font.Font('freesansbold.ttf', 40)
                    text = font.render('Score : ' + str(self.score),
                                    True, (255, 255, 255), (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (330, 300)
                    self.screen.blit(text, textRect)

                    pygame.display.flip()

                    if self.sound:
                        pygame.mixer.music.play()

                    time.sleep(2)
                    self.closingGame = True

                self.explosion -= 20

    def invoqueEnnemies(self):
        if self.score < 9:
            self.enemies.append(Enemy(self.screen, {"x": 0, "y": 0}, self.sound))
            self.enemies.append(Enemy(self.screen, {"x": 200, "y": 0}, self.sound))
            self.enemies.append(Enemy(self.screen, {"x": 400, "y": 0}, self.sound))
        elif self.score < 24:
            self.enemies.append(EnemyHorisontal(self.screen, {"x": 0, "y": 0}, self.sound))
            self.enemies.append(EnemyHorisontal(self.screen, {"x": 120, "y": 50}, self.sound))
            self.enemies.append(EnemyHorisontal(self.screen, {"x": 240, "y": 0}, self.sound))
            self.enemies.append(EnemyHorisontal(self.screen, {"x": 360, "y": 50}, self.sound))
            self.enemies.append(EnemyHorisontal(self.screen, {"x": 480, "y": 0}, self.sound))
            self.enemies.append(EnemyHorisontal(self.screen, {"x": 600, "y": 50}, self.sound))
        else:
            self.enemies.append(EnemySprint(self.screen, {"x": 0, "y": 0}, self.sound))
            self.enemies.append(EnemySprint(self.screen, {"x": 250, "y": 0}, self.sound))
            self.enemies.append(EnemySprint(self.screen, {"x": 500, "y": 0}, self.sound))

    # Rafraichissement de l'ecran
    def draw_game_screen(self):
        # Affichage du fond du jeu
        self.screen.blit(self.fond, self.fondrect)

        if(self.ship.lives > 0):

            # Affichage du vaisseau
            if(self.ship.invincibility > 0):
                if(self.ship.invincibility % 5):
                    image_invincible = pygame.image.load("img/ships/ship.gif").convert()
                    image_invincible.set_alpha(0)
                    self.screen.blit(image_invincible, self.ship.rect)
                else:
                    self.screen.blit(self.ship.image, self.ship.rect)
            else:
                self.screen.blit(self.ship.image, self.ship.rect)
        else:
            self.screen.blit(self.ship.image, self.ship.rect)

        # Affichage des missiles de notre vaisseau
            for obj in self.ship.missiles:
                if (obj.rect.y < 0 - obj.height):
                    self.ship.missiles.remove(obj) # On enleve la balle hors de l'ecran
                else:
                    self.screen.blit(obj.image, obj.rect)  # On affiche le missile

        # Affichage des missiles des ennemies
        for enemy in self.enemies:  # pour chaque ennemi
            for obj in enemy.missiles:  # pour chacun de ses missiles
                if (obj.rect.y > self.screen.get_rect().height - obj.height):
                    enemy.missiles.remove(obj) # On enleve la balle hors de l'ecran
                else:
                    self.screen.blit(obj.image, obj.rect) # On affiche le missile

        # Affichage des ennemis
        for obj in self.enemies:
            self.screen.blit(obj.image, obj.rect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Vies : ' + str(self.ship.lives),
                           True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (595, 355)
        self.screen.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Score : ' + str(self.score),
                           True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (595, 385)
        self.screen.blit(text, textRect)

        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(60)

    def draw_background(self):
        self.screen.blit(self.fond, self.fondrect)

############################################################
####################### ENEMIES ############################
############################################################

class EnemyMissile():

    # Appel du constructeur de la Classe
    def __init__(self, speed, image):
        self.width = 10
        self.height = 10
        self.image = image
        self.rect = image.get_rect()
        self.speed = speed

# Meme chose que 'self.rect.y = self.rect.y - speed'
    def update(self):
        self.rect.y += self.speed


id = 0

class Enemy(pygame.sprite.Sprite):

    # Appel du constructeur de la fonction (a l'appel de la classe)
    def __init__(self, screen, rect, isSound):
        pygame.sprite.Sprite.__init__(self)

        # proprietes du vaisseau
        self.id = id + 1
        self.image = pygame.image.load("img/ennemies/ennemy.gif").convert()
        self.rect = pygame.image.load("img/ennemies/ennemy.gif").convert().get_rect()
        self.screen = screen
        self.rect.x = rect["x"]
        self.rect.y = rect["y"]
        self.missiles = []
        self.delayShot = 60
        self.delayMove = 2
        self.sound = pygame.mixer.Sound("sons/shoot.wav")
        self.is_sound = isSound

    def update(self):

        for obj in self.missiles:
            obj.update()
        # Mouvements de l'Enemy
        if self.delayMove == 0:
            self.delayMove = 2
            self.rect.y += 1
        if self.delayMove > 0 and self.rect.y < 400:
            self.delayMove -= 1
        else:
            setattr(game.ship, "lives", getattr(game.ship, "lives")-1)
            enemies = getattr(game, "enemies")
            for enemy in enemies:
                if self.id == enemy.id:
                    enemies.remove(enemy)
            setattr(game, "enemies", enemies)
        # Tirs de l'Enemy
        if (self.delayShot == 0):
            self.delayShot = 60
            self.missiles.append(EnemyMissile(
                8, pygame.image.load("img/shots/shot.gif").convert()))
            self.missiles[len(self.missiles) - 1].rect.x = self.rect.x + 16
            self.missiles[len(self.missiles) - 1].rect.y = self.rect.y + 33
            if self.is_sound:
                self.sound.play()
        else:
            self.delayShot -= 1


class EnemyHorisontal(Enemy):
    # Appel du constructeur de la fonction (a l'appel de la classe)
    def __init__(self, screen, rect, isSound):
        super().__init__(screen, rect, isSound)

        # proprietes du vaisseau
        self.image = pygame.image.load("img/ennemies/ennemy_2.gif").convert()
        self.rect = pygame.image.load("img/ennemies/ennemy_2.gif").convert().get_rect()
        self.rect.x = rect["x"]
        self.rect.y = rect["y"]

        self.delayShot = 30
        self.delayMove = 2
        self.sound = pygame.mixer.Sound("sons/shoot.wav")

    def update(self):

        for obj in self.missiles:
            obj.update()
        # Mouvements de l'Enemy
        if self.delayMove == 0:
            self.delayMove = 2
            if self.rect.x < 640:
                self.rect.x += 3
            if (self.rect.x > 640):
                self.rect.x = -20
        else:
            self.delayMove -= 1

        # Tirs de l'Enemy
        if (self.delayShot == 0):
            self.delayShot = 30
            self.missiles.append(EnemyMissile(
                8, pygame.image.load("img/shots/shot.gif").convert()))
            self.missiles[len(self.missiles) - 1].rect.x = self.rect.x + 16
            self.missiles[len(self.missiles) - 1].rect.y = self.rect.y + 33

            if self.is_sound:
                self.sound.play()

        # Ajouter le tir d'un ennemi
        if (self.delayShot > 0):
            self.delayShot -= 1


class EnemySprint(Enemy):
    # Appel du constructeur de la fonction (a l'appel de la classe)
    def __init__(self, screen, rect, isSound):
        super().__init__(screen, rect, isSound)

        # proprietes du vaisseau
        self.image = pygame.image.load("img/ennemies/ennemy_2.gif").convert()
        self.rect = pygame.image.load("img/ennemies/ennemy_2.gif").convert().get_rect()
        self.rect.x = rect["x"]
        self.rect.y = rect["y"]

        self.delayShot = 30
        self.delayMove = 2
        self.sound = pygame.mixer.Sound("sons/shoot.wav")

    def update(self):
        for obj in self.missiles:
            obj.update()
        # Mouvements de l'Enemy
        if self.delayMove == 0:
            self.delayMove = 2
            self.rect.y += 3
        if self.delayMove > 0 and self.rect.y < 400:
            self.delayMove -= 1
        else:
            setattr(game.ship, "lives", getattr(game.ship, "lives")-1)
            enemies = getattr(game, "enemies")
            for enemy in enemies:
                if self.id == enemy.id:
                    enemies.remove(enemy)
            setattr(game, "enemies", enemies)
        # Tirs de l'Enemy
        if (self.delayShot == 0):
            self.delayShot = 90
            self.missiles.append(EnemyMissile(
                8, pygame.image.load("img/shots/shot.gif").convert()))
            self.missiles[len(self.missiles) - 1].rect.x = self.rect.x + 16
            self.missiles[len(self.missiles) - 1].rect.y = self.rect.y + 33
            if self.is_sound:
                self.sound.play()
        else:
            self.delayShot -= 1


############################################################
######################### ALLY #############################
############################################################

class AllyMissile(pygame.sprite.Sprite):

    # Appel du constructeur de la Classe
    def __init__(self, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.width = 10
        self.height = 10
        self.image = image
        self.rect = image.get_rect()
        self.speed = speed

 # Meme chose que 'self.rect.y = self.rect.y - speed'
    def update(self):
        self.rect.y -= self.speed


# Creation de la classe Ship
class Ship():
    # Appel du constructeur de la fonction (a l'appel de la classe)
    def __init__(self, image, screen, isSound):
        # proprietes du vaisseau
        self.width = 30
        self.height = 18
        self.image = image
        self.screen = screen
        self.rect = image.get_rect()
        self.missiles = []
        self.latency = 0
        self.lives = 3
        self.invincibility = 100
        self.sound = pygame.mixer.Sound("sons/shoot.wav")
        self.is_sound = isSound
        pygame.mixer.music.load("sons/sf_explosion_01.mp3")

    def update(self):

        if(self.lives > 0):
            # raffraichir la position des missiles
            for obj in self.missiles:
                obj.update()

            # raffraichir la position du vaisseau
            self.latency += 1
            k = pygame.key.get_pressed()
            if (k[K_RIGHT] and self.rect.x < self.screen.get_rect().width - self.width):
                self.rect.x = self.rect.x + 6
            if (k[K_LEFT] and self.rect.x > 0):
                self.rect.x = self.rect.x - 6
            if (k[K_UP] and self.rect.y > 0):
                self.rect.y = self.rect.y - 6
            if (k[K_DOWN] and self.rect.y < self.screen.get_rect().height - self.height):
                self.rect.y = self.rect.y + 6
            if (k[K_SPACE]) and self.latency >= 8:
                self.missiles.append(AllyMissile(
                    8, pygame.image.load("img/shots/shot.gif").convert()))
                self.missiles[len(self.missiles) - 1].rect.x = self.rect.x + 10
                self.missiles[len(self.missiles) - 1].rect.y = self.rect.y - 15

                if self.is_sound:
                    self.sound.play()

                self.latency = 0

def set_difficulty(value, difficulty):
    print("TODO")

def set_sound(value, index, boolean):
    setattr(game, "sound", boolean)

# animation()
game = Game()
game.main()