"""

Initially pulled from online as blueprint to practice with

"""

import pygame as pg

pg.init()

width = 1000
height = 700

screen_res = (width, height)
pg.display.set_caption('First Trick')
screen = pg.display.set_mode(screen_res)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

ball = pg.draw.circle(surface=screen, color=red, center=[50, 50], radius=10)
speed = [1, 1]

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    screen.fill(black)
    ball = ball.move(speed)

    if ball.left <= 0 or ball.right >= width:
        speed[0] = -speed[0]
    if ball.top <= 0 or ball.bottom >= height:
        speed[1] = -speed[1]

    pg.draw.circle(surface=screen, color=red, center=ball.center, radius=20)

    pg.display.flip()
