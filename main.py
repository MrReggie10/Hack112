import cv2
import numpy as np
from cmu_graphics import *
import math, random
from types import SimpleNamespace
import copy
from Spells import Spell

spells = Spell()
circle = spells.getCircle()
figureEight = spells.getFigureEight()
star = spells.getStar()
lightningBolt = spells.getLightningBolt()
tp = spells.getTP()
duck = spells.getDuck()






# Michael Reeves: https://www.youtube.com/watch?v=USKD3vPD6ZA&t=726s
def generateColorMask(img):
    lowerBound = np.array([10, 190, 150])
    upperBound = np.array([30, 255, 255])

    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsvImg, lowerBound, upperBound)

def computeAveragePosition(img):
    avgX = 0
    avgY = 0
    counter = 0
    for x in range(0, img[0].size, 10):
        for y in range(0, img[:,0].size, 10):
            if img[y, x] == 255:
                avgX += x
                avgY += y
                counter += 1
    if counter > 0:
        avgX //= counter
        avgY //= counter
    return avgX, avgY

def capturePosition():
    ret, frame = camera.read()
    frameReversed = frame[:, ::-1]
    mask = generateColorMask(frameReversed)

    x, y = computeAveragePosition(mask)

    pos = (x * 1500 // (mask[0].size), y * 850 // (mask[:,0].size), int(np.mean(mask, (0, 1)) * 100))

    return pos

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
        if self.size == 100:
            self.x -= 2
        elif self.size == 200:
            self.x -= 1.5
        elif self.size == 300:
            self.x -= 0.75
    def takeDamageReturnIsDead(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            return True
        return False

camera = cv2.VideoCapture(0)

def onAppStart(app):
    app.position = (0, 0, 0)
    app.state = 'starting'
    # states:
    # starting (press a button to start)
    # calibrating (ensures that the duck is far enough away form the camera)
    # casting (while the spell is going)
    # casted (damaging phase)
    # newStage (between enemies)
    # win
    # lose
    app.calibrationTimer = 0
    app.castedTimer = 0
    app.startingTimer = 0
    app.newStageTimer = 0

    app.spellList = ['circle', 'figureEight', 'star', 'lightningBolt', 'tp', 'duck']
    app.currentSpell = chooseSpell(app)
    app.path = []
    app.blueR = 30
    app.stage = 'preparing'
    app.error = 0
    app.errorCalculated = False
    app.castDistance = 40
    app.tooFar = 2

    app.currentEnemy = None
    app.stage = 1

    app.sideTA = 'sideTA.jpeg'
    app.frontTA = 'frontTA.jpeg'
    app.austin = 'austin.jpeg'
    app.koz = 'kosbie.jpeg'

    # sets background image
    '''The background image is from wallpapersden.com and is titled Hogwarts Harry Potter School Wallpaper'''
    app.backgroundURL = 'hogwartsbgTiny.jpeg'

def chooseSpell(app):
    index = random.randrange(len(app.spellList))
    return app.spellList[index]

def drawSpell(app, opc = 100):
    if app.currentSpell == 'circle':
        drawPolygon(*circle, fill=None, border='red', opacity=opc)
        drawLabel('Expelliarmus!', app.width/2, app.height*(3/4), size=40, fill='red', opacity=opc)
    elif app.currentSpell == 'figureEight':
        drawPolygon(*figureEight, fill=None, border='red', opacity=opc)
        drawLabel('Reducto!', app.width/2, app.height*(3/4), size=40, fill='red', opacity=opc)
    elif app.currentSpell == 'star':
        drawPolygon(*star, fill=None, border='red', opacity=opc)
        drawLabel('Wingardium Leviosa!', app.width/2, app.height*(3/4), size=40, fill='red', opacity=opc)
    elif app.currentSpell == 'lightningBolt':
        drawPolygon(*lightningBolt, fill=None, border='red', opacity=opc)
        drawLabel('Expecto Patronum!', app.width/2, app.height*(3/4), size=40, fill='red', opacity=opc)
    elif app.currentSpell == 'tp':
        drawPolygon(*tp, fill=None, border='red', opacity=opc)
        drawLabel('The Most Terrifying Spell!', app.width/2, app.height*(3/4), size=40, fill='red', opacity=opc)
    elif app.currentSpell == 'duck':
        drawPolygon(*duck, fill=None, border='red', opacity=opc)
        drawLabel('KING!', app.width/2, app.height*(3/4), size=40, fill='red', opacity=opc)

def calculateError(app):
    if app.currentSpell == 'circle':
        spell = copy.copy(circle)
    elif app.currentSpell == 'figureEight':
        spell = copy.copy(figureEight)
    elif app.currentSpell == 'star':
        spell = copy.copy(star)
    elif app.currentSpell == 'lightningBolt':
        spell = copy.copy(lightningBolt)
    elif app.currentSpell == 'tp':
        spell = copy.copy(tp)
    elif app.currentSpell == 'duck':
        spell = copy.copy(duck)
    totalInCast = 0
    spellCopy = copy.copy(spell)
    while len(spellCopy) >= 2:
        y = spellCopy.pop()
        x = spellCopy.pop()
        if isInCast(app, x, y):
            totalInCast += 1
    fractionScore = int(totalInCast * 100 // (len(spell)/2))
    return fractionScore

def isInCast(app, x, y):
    for blueX, blueY in app.path:
        if distance(x, y, blueX, blueY) <= app.blueR:
            return True
    return False

def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

def onStep(app):

    if app.state == 'starting':
        app.startingTimer += 1
        if app.startingTimer > 60:
            app.currentEnemy = Enemy(app.stage)
            app.state = 'calibrating'
    else:
        app.startingTimer = 0

    if app.state == 'calibrating':
        app.position = capturePosition()
        if app.position[2] > app.castDistance or app.position[2] < app.tooFar:
            app.calibrationTimer = 0
        else:
            app.calibrationTimer += 1
            if app.calibrationTimer > 60:
                app.state = 'casting'

    if app.state == 'casting':
        app.position = capturePosition()
        app.path.append((app.position[0], app.position[1]))
        app.currentEnemy.move()
        if app.currentEnemy.x <= 200:
            app.state = 'lose'
        if app.position[2] > app.castDistance:
            app.state = 'casted'

    if app.state == 'casted':
        if not app.errorCalculated:
            app.error = calculateError(app)
            app.currentSpell = chooseSpell(app)
            app.path = []
            if app.currentEnemy.takeDamageReturnIsDead(app.error):
                app.currentEnemy = None
                app.state = 'newStage'
            app.errorCalculated = True
        app.castedTimer += 1
        if app.castedTimer > 60:
            app.state = 'casting'
            app.errorCalculated = False
    else:
        app.castedTimer = 0
    
    if app.state == 'newStage':
        app.newStageTimer += 1
        if app.newStageTimer > 60:
            app.stage += 1
            if app.stage == 4:
                app.state = 'win'
            else:
                app.state = 'starting'
    else:
        app.newStageTimer = 0
    


def redrawAll(app):
    # draws background of game
    drawImage(app.backgroundURL, 0, 0, width = app.width, height = app.height)

    if app.state == 'starting':
        drawLabel("Ready?", app.width/2, app.height/2, fill='blue', size=28)
        if app.currentEnemy != None:
            if app.currentEnemy.stage == 1:
                drawImage(app.sideTA, app.currentEnemy.x, 750,
                           width=app.currentEnemy.size, height=app.currentEnemy.size, align='bottom-left')
            else:
                drawImage(app.frontTA, app.currentEnemy.x, 750, align='bottom-left', 
                          width=app.currentEnemy.size, height=app.currentEnemy.size)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)

    elif app.state == 'calibrating':
        if app.position[2] > app.castDistance:
            drawLabel("Too close!", app.width/2, app.height/2, fill='red', size=28)
        elif app.position[2] < app.tooFar:
            drawLabel("Too far!", app.width/2, app.height/2, fill='red', size=28)
        else:
            drawLabel("Perfect!", app.width/2, app.height/2, fill='green', size=28)
        if app.currentEnemy != None:
            if app.currentEnemy.stage == 1:
                drawImage(app.sideTA, app.currentEnemy.x, 750,
                           width=app.currentEnemy.size, height=app.currentEnemy.size, align='bottom-left')
            else:
                drawImage(app.frontTA, app.currentEnemy.x, 750, align='bottom-left', 
                          width=app.currentEnemy.size, height=app.currentEnemy.size)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)

    elif app.state == 'casting':
        if app.currentEnemy != None:
            if app.currentEnemy.stage == 1:
                drawImage(app.sideTA, app.currentEnemy.x, 750,
                           width=app.currentEnemy.size, height=app.currentEnemy.size, align='bottom-left')
            else:
                drawImage(app.frontTA, app.currentEnemy.x, 750, align='bottom-left', 
                          width=app.currentEnemy.size, height=app.currentEnemy.size)
        drawSpell(app)
        drawCircle(app.position[0], app.position[1], app.blueR, fill='blue')
        for x, y in app.path:
            drawCircle(x, y, app.blueR, fill='blue', opacity=15)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)

    elif app.state == 'casted':
        drawLabel('Cast!', app.width/2, app.height/2, fill='blue', size=56)
        drawLabel(str(app.error), app.width/2, app.height/2 + 150, size=100, fill='purple')
        if app.currentEnemy != None:
            if app.currentEnemy.stage == 1:
                drawImage(app.sideTA, app.currentEnemy.x, 750,
                           width=app.currentEnemy.size, height=app.currentEnemy.size, align='bottom-left')
            else:
                drawImage(app.frontTA, app.currentEnemy.x, 750, align='bottom-left', 
                          width=app.currentEnemy.size, height=app.currentEnemy.size)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)

    elif app.state == 'newStage':
        drawLabel('Victory!', app.width/2, app.height/2, fill='yellow', size=56)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)
    
    elif app.state == 'win':
        drawLabel('You are win!', app.width/2, app.height/2, fill='orange', size=56)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)
    
    elif app.state == 'lose':
        drawLabel('Game over :(', app.width/2, app.height/2, fill='orange', size=56)

def main():
    runApp(1500, 850)

main()