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

    print(pos)
    return pos

def restartCast(app):
    app.casting = True

camera = cv2.VideoCapture(0)

def onAppStart(app):
    app.position = (0, 0, 0)
    app.state = 'starting'
    # states:
    # starting (press a button to start)
    # calibrating (ensures that the duck is far enough away form the camera)
    # casting (while the spell is going)
    # casted (damaging phase)
    app.calibrationTimer = 0
    app.castedTimer = 0
    app.startingTimer = 0

    app.spellList = ['circle', 'figureEight', 'star', 'lightningBolt', 'tp', 'duck']
    app.currentSpell = chooseSpell(app)
    app.path = []
    app.blueR = 30
    app.stage = 'preparing'
    app.error = 0
    app.errorCalculated = False
    app.castDistance = 40
    app.tooFar = 2

def chooseSpell(app):
    index = random.randrange(len(app.spellList))
    return app.spellList[index]

def drawSpell(app, opc = 100):
    if app.currentSpell == 'circle':
        drawPolygon(*circle, fill=None, border='red', opacity=opc)
        drawLabel('Expelliarmus!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)
    elif app.currentSpell == 'figureEight':
        drawPolygon(*figureEight, fill=None, border='red', opacity=opc)
        drawLabel('Reducto!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)
    elif app.currentSpell == 'star':
        drawPolygon(*star, fill=None, border='red', opacity=opc)
        drawLabel('!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)
    elif app.currentSpell == 'lightningBolt':
        drawPolygon(*lightningBolt, fill=None, border='red', opacity=opc)
        drawLabel('!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)
    elif app.currentSpell == 'tp':
        drawPolygon(*tp, fill=None, border='red', opacity=opc)
        drawLabel('!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)
    elif app.currentSpell == 'duck':
        drawPolygon(*duck, fill=None, border='red', opacity=opc)
        drawLabel('!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)

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
    fractionScore = totalInCast * 100 // (len(spell)/2)
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
        if app.position[2] > app.castDistance:
            app.state = 'casted'

    if app.state == 'casted':
        if not app.errorCalculated:
            app.error = calculateError(app)
            app.currentSpell = chooseSpell(app)
            app.path = []
            app.errorCalculated = True
        app.castedTimer += 1
        if app.castedTimer > 60:
            app.state = 'casting'
            app.errorCalculated = False
    else:
        app.castedTimer = 0
    

def redrawAll(app):

    if app.state == 'starting':
        drawLabel("Ready?", app.width/2, app.height/2, fill='blue', size=28)

    elif app.state == 'calibrating':
        if app.position[2] > app.castDistance:
            drawLabel("Too close!", app.width/2, app.height/2, fill='red', size=28)
        elif app.position[2] < app.tooFar:
            drawLabel("Too far!", app.width/2, app.height/2, fill='red', size=28)
        else:
            drawLabel("Perfect!", app.width/2, app.height/2, fill='green', size=28)

    elif app.state == 'casting':
        drawSpell(app)
        drawCircle(app.position[0], app.position[1], app.blueR, fill='blue')
        for x, y in app.path:
            drawCircle(x, y, app.blueR, fill='blue', opacity=15)

    elif app.state == 'casted':
        drawLabel('Casted!', app.width/2, app.height/2, fill='blue', size=56)
        drawLabel(str(app.error), app.width/2, app.height/2 + 150, size=100, fill='purple')

def main():
    runApp(1500, 850)

main()