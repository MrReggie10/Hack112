from cmu_graphics import *
import math

class Enemy:
    def __init__(self, health):
        self.x = 1300
        self.health = health
        self.size =  .2 * health if health != 2500 else 200
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
    app.enemies = [Enemy(2500), Enemy(500), Enemy(250)]
    # app.enemy = Enemy(500, 'black')
    # app.enemy2 = Enemy(1000, 'red')
    # app.enemy3 = Enemy(250, 'green')
    app.sideTA = 'sideTA.jpeg'
    app.frontTA = 'frontTA.jpeg'
    app.austin = 'austin.jpeg'
    app.koz = 'kosbie.jpeg'

    app.sideWidth, app.sideHeight = getRealSize(app, app.sideTA)
    app.frontWidth, app.frontHeight = getRealSize(app, app.frontTA)

    app.sideX = 1300

def getRealSize(app, image):
    # calculations for proper image positioning
    imageWidth, imageHeight = getImageSize(image)
    widthReduction = imageWidth / app.width
    imageRealWidth = imageWidth / widthReduction
    heightReduction = imageHeight / app.height
    imageRealHeight = imageHeight / heightReduction
    return imageRealWidth, imageRealHeight

def onStep(app):
    for enemy in app.enemies:
        enemy.move()

def redrawAll(app):
    drawImage(app.austin, 100, 750, align='bottom', width=200, height=200)
    drawImage(app.koz, 40, 650, align='bottom', width=75, height=75)
    for enemy in app.enemies:
        if enemy.size == 50:
            drawImage(app.sideTA, enemy.x, 750, width=100, height=100, align='bottom')
        elif enemy.size == 100:
            drawImage(app.frontTA, enemy.x, 750, align='bottom', width=150, height=200)
        elif enemy.size == 200:
            drawImage(app.frontTA, enemy.x, 750, align='bottom', width=300, height=300)
        
def main():
    runApp()
main()