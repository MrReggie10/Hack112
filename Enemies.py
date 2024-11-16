from cmu_graphics import *

class Enemy:
    def __init__(self, stage):
        self.x = 1300
        self.stage = stage
        if stage == 1:
            self.health = 150
            self.color = 'green'
            self.size = 100
        elif stage == 2:
            self.health = 300
            self.color = 'black'
            self.size = 200
        elif stage == 3:
            self.health = 800
            self.color = 'red'
            self.size = 300
    def move(self):
        if self.stage == 1:
            self.x -= 2
        elif self.stage == 2:
            self.x -= 1.5
        elif self.stage == 3:
            self.x -= 0.75
    def takeDamageReturnIsDead(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            return True
        return False

def onAppStart(app):
    app.width = 1500
    app.height = 850
    app.enemies = [Enemy(1), Enemy(2), Enemy(3)]

    app.sideTA = 'sideTA.jpeg'
    app.frontTA = 'frontTA.jpeg'
    app.austin = 'austin.jpeg'
    app.koz = 'kosbie.jpeg'

def onStep(app):
    for enemy in app.enemies:
        enemy.move()

def redrawAll(app):
    drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
    drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)
    for enemy in app.enemies:
        if enemy.stage == 1:
            drawImage(app.sideTA, enemy.x, 750, align='bottom-left', width=enemy.size, height=enemy.size, )
        else:
            drawImage(app.frontTA, enemy.x, 750, align='bottom-left', width=enemy.size, height=enemy.size)

def main():
    runApp()
main()