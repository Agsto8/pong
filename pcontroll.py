from pygame import *
import pyautogui
from random import randint
import os

here = os.path.dirname(os.path.abspath(__file__))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, sizex, sizey, player_speed, window):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (sizex, sizey))
        self.speed = player_speed
        self.original_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.x = sizex
        self.sx, self.sy = pyautogui.size()
        self.window = window
        self.points = 0

    def reset(self):
        self.window.blit(self.image, (self.rect.x, self.rect.y))

    def mover(self):
        s = self.speed
        keys=key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= s
        if keys[K_DOWN] and self.rect.y < 690:
            self.rect.y += s

    def movel(self):
        s = self.speed
        keys=key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= s
        if keys[K_s] and self.rect.y < 690:
            self.rect.y += s

class Ball(sprite.Sprite):
    def __init__(self, img, sizex, sizey, window):
        super().__init__()
        self.image = transform.scale(image.load(img), (sizex, sizey))
        self.lvl = 15
        self.speed = self.lvl/5
        self.original_speed = self.speed
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
        self.sx, self.sy = pyautogui.size()
        self.window = window
        self.ru = False
        self.rd = True
        self.lu = False
        self.ld = False
        

    def move(self):
        if self.rd:
            self.rect.x += self.speed
            self.rect.y += self.speed
        elif self.ru:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        elif self.ld:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        if self.lu:
            self.rect.x -= self.speed
            self.rect.y -= self.speed

    def reset(self):
        self.window.blit(self.image, (self.rect.x, self.rect.y))

    def check(self, p1, p2):
        if self.rect.y >= 680:
            if self.rd:
                self.rd = False
                self.ru = True
            else:
                self.ld = False
                self.lu = True
        if self.rect.y <= 0:
            if self.ru:
                self.ru = False
                self.rd = True
            else:
                self.lu = False
                self.ld = True

        if self.rect.x <= 0:
            p2.points += 1
            self.rect.x = 400
            self.rect.y = 400
        elif self.rect.x >= 680:
            p1.points += 1
            self.rect.x = 400
            self.rect.y = 400

        if sprite.collide_rect(self,p1):
            if self.lu:
                self.lu = False
                self.ru = True
            elif self.ld:
                self.ld = False
                self.rd = True
            self.lvl += 1
            self.speed = self.lvl/5

        if sprite.collide_rect(self,p2):
            if self.ru:
                self.ru = False
                self.lu = True
            elif self.rd:
                self.rd = False
                self.ld = True
            self.lvl += 1
            self.speed = self.lvl/5

class PauseButton():
    def __init__(self, x, y ,window):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.window = window

        self.paused = False

        self.fillColors = {
            'normal': '#f55142',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonRect = Rect(self.x, self.y, self.width, self.height)
        self.paus = transform.scale(image.load(os.path.join(here, "pauseb.png")),(self.width,self.height))
        self.play = transform.scale(image.load(os.path.join(here, "playb.png")),(self.width,self.height))

        self.alreadyPressed = False
        self.paused = False

        self.cor = self.paus

    def process(self, sprites):

        mousePos = mouse.get_pos()
        
        if self.buttonRect.collidepoint(mousePos):

            if mouse.get_pressed(num_buttons=3)[0]:

                if not self.alreadyPressed:
                    self.paused = not self.paused
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False
                

        if self.paused:
            self.cor = self.play
            for spr in sprites:
                spr.speed = 0
        else:
            self.cor = self.paus
            for spr in sprites:
                spr.speed = spr.original_speed

        self.window.blit(self.cor,(self.x,self.y))
       # draw.circle(self.window, (0,0,255), (self.x, self.y), 30, 5)
