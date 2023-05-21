from pygame import *
from time import sleep
from random import randint
from pcontroll import *
import os

window = display.set_mode((800, 800))

display.set_caption("pong")
here = os.path.dirname(os.path.abspath(__file__))

sprites = []

pdl = os.path.join(here, "padl.png")

lp = GameSprite(pdl, 0, 350, 15, 100, 5, window)
rp = GameSprite(pdl, 785, 350, 15, 100, 5, window)
sprites.append(lp)
sprites.append(rp)
bll = os.path.join(here, "ball.png")
ball = Ball(bll, 120, 120, window)
sprites.append(ball)

bc = os.path.join(here, "bsg.png")
background = transform.scale(image.load(bc), (800, 800))

pb = PauseButton(10, 720, window)

font.init()
f = font.SysFont(None, 50)
p1tsl = f.render("P1:", True, (0, 0, 0))
p2tsl = f.render("P2:", True, (0, 0, 0))
p1tl = f.render("0", True, (0, 0, 0))
p2tl = f.render("0", True, (0, 0, 0))

fps = 30
clock = time.Clock()

game = True
while game:
    window.blit(background, (0, 0))
    lp.movel()
    lp.reset()
    rp.mover()
    rp.reset()
    pb.process(sprites)

    ball.move()
    ball.check(lp, rp)
    ball.reset()

    p1ts = lp.points
    p2ts = rp.points

    for e in event.get():
        if e.type == QUIT:
            game = False

    p1tl = f.render(str(p1ts), True, (0, 0, 0))
    p2tl = f.render(str(p2ts), True, (0, 0, 0))

    window.blit(p1tsl, (5, 5))
    window.blit(p1tl, (60, 5))
    window.blit(p2tsl, (705, 5))
    window.blit(p2tl, (760, 5))

    display.update()
    clock.tick(fps)
