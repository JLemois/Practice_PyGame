"""

Initially pulled from online as blueprint to practice with

"""

import pygame as pg
import random as random

pg.init()

WIDTH, HEIGHT = 600, 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pg.font.Font('freesansbold.ttf', 20)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Brick Break")

clock = pg.time.Clock()
FPS = 30


class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        self.strikerRect = pg.Rect(self.posx, self.posy, self.width, self.height)
        self.striker = pg.draw.rect(screen, self.color, self.strikerRect)

    def display(self):
        self.striker = pg.draw.rect(screen, self.color, self.strikerRect)

    def update(self, xFac):
        self.posx += self.speed * xFac

        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.strikerRect = pg.Rect(self.posx, self.posy, self.width, self.height)

    def getRect(self):
        return self.strikerRect


class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        self.blockRect = pg.Rect(self.posx, self.posy, self.width, self.height)
        self.block = pg.draw.rect(screen, self.color, self.blockRect)

    def display(self):
        if self.health > 0:
            self.block = pg.draw.rect(screen, self.color, self.blockRect)

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

        self.ball = pg.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def display(self):
        self.ball = pg.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.xFac * self.speed
        self.posy = self.yFac * self.speed

        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1

        if self.posy <= 0:
            self.yFac *= -1

        if self.posy >= HEIGHT:
            return True
        return False

    def reset(self):
        self.posx = 0
        self.posy = HEIGHT
        self.xFac, self.yFac = 1, -1

    def hit(self):
        self.yFac *= -1

    def getRect(self):
        return self.ball


def collisionChecker(rect, ball):
    if pg.Rect.colliderect(rect, ball):
        return True
    return False


def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlocks = []

    for i in range(0, WIDTH, blockWidth + horizontalGap):
        for j in range(0, HEIGHT // 2, blockHeight + verticalGap):
            listOfBlocks.append(Block(i, j, blockWidth, blockHeight, random.choice([WHITE, GREEN])))
    return listOfBlocks


def gameOver():

    while gameOver:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return True


def main():
    running = True
    lives = 3
    score = 0

    scoreText = font.render("Score: " + str(score), True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (20, HEIGHT - 10)

    livesText = font.render("Lives: " + str(lives), True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (120, HEIGHT - 10)

    striker = Striker(0, HEIGHT - 50, 100, 20, 10, WHITE)
    strikerXFac = 0

    ball = Ball(0, HEIGHT - 150, 7, 5, WHITE)

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

    while running:
        screen.fill(BLACK)
        screen.blit(scoreText, scoreTextRect)
        screen.blit(livesText, livesTextRect)

        scoreText = font.render("Score: " + str(score), True, WHITE)
        livesText = font.render("Lives: " + str(lives), True, WHITE)

        if not listOfBlocks:
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

        if lives <= 0:
            running = gameOver()

            while listOfBlocks:
                listOfBlocks.pop(0)

            lives = 3
            score = 0
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        strikerXFac = -1
                    if event.key == pg.K_RIGHT:
                        strikerXFac = 1

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        strikerXFac = 0

                if collisionChecker(striker.getRect(), ball.getRect()):
                    ball.hit()

                for block in listOfBlocks:
                    if collisionChecker(block.getRect(), ball.getRect()):
                        ball.hit()
                        block.hit()

                        if block.getHealth() <= 0:
                            listOfBlocks.pop(listOfBlocks.index(block))
                            score += 5

                striker.update(strikerXFac)
                lifeLost = ball.update()

                if lifeLost:
                    lives -= 1
                    ball.reset()
                    print(lives)

                striker.display()
                ball.display()

                for block in listOfBlocks:
                    block.display()

                pg.display.update()
                clock.tick(FPS)


if __name__ == '__main__':
    main()
    pg.quit()
