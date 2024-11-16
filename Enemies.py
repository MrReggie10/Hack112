from cmu_graphics import *
import math

class Enemy:
    def __init__(self, health, color):
        self.x = 1300
        self.health = health
        self.size =  .2 * health if health != 5000 else 200
        self.color = color
    def move(self):
        if self.size == 50:
            self.x -= 3
        elif self.size == 100:
            self.x -= 2
        elif self.size == 200:
            self.x -= 0.75
        


def onAppStart(app):
    app.width = 1500
    app.height = 850
    app.enemies = [Enemy(5000, 'red'), Enemy(500, 'black'), Enemy(250, 'green')]
    # app.enemy = Enemy(500, 'black')
    # app.enemy2 = Enemy(1000, 'red')
    # app.enemy3 = Enemy(250, 'green')

def onStep(app):
    for enemy in app.enemies:
        enemy.move()

def redrawAll(app):
    for enemy in app.enemies:
        drawRect(enemy.x, 750, enemy.size, enemy.size, fill=enemy.color, align='bottom')

def main():
    runApp()
main()