from cmu_graphics import *
import math, random
from types import SimpleNamespace
import copy
from Spells import Spell

spells = Spell()
circle = spells.getCircle()
figureEight = spells.getFigureEight()

###Enemies with damage that scales on how well you follow the spell path
#Objects: enemies ?
#Make list of spells

def onAppStart(app):
    app.width = 1500
    app.height = 850
    app.cx, app.cy = 200, 200
    app.spellList = ['circle', 'figureEight']
    app.currentSpell = chooseSpell(app)
    app.path = []
    app.blueR = 15
    app.steps = 0
    app.stage = 'preparing'
    app.error = 0
    

def redrawAll(app):
    if app.stage == 'preparing':
        drawSpell(app, opc = 20)
    elif app.stage == 'drawing':
        drawSpell(app)
        drawCircle(app.cx, app.cy, app.blueR, fill='blue')
        for x, y in app.path:
            drawCircle(x, y, app.blueR, fill='blue', opacity=15)
    elif app.stage == 'resting':
        count = math.floor((-1/30)*(app.steps-180) + 7)
        drawLabel(str(count), app.width/2, app.height/2, size=100, fill='purple')
        drawLabel(str(app.error), app.width/2, app.height*(3/4), size=100, fill='purple')

def onMouseMove(app, mouseX, mouseY):
    app.cx, app.cy = mouseX, mouseY
    if app.stage == 'drawing':
        app.path.append((mouseX, mouseY))

def chooseSpell(app):
    index = random.randrange(len(app.spellList))
    return app.spellList[index]

def drawSpell(app, opc = 100):
    if app.currentSpell == 'circle':
        drawPolygon(*circle, fill=None, border='red', opacity=opc)
        drawLabel('Expelliarmus!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)
    if app.currentSpell == 'figureEight':
        drawPolygon(*figureEight, fill=None, border='red', opacity=opc)
        drawLabel('Reducto!', app.width/2, app.height/2, size=16, fill='red', opacity=opc)

def calculateError(app):
    if app.currentSpell == 'circle':
        spell = copy.copy(circle)
    elif app.currentSpell == 'figureEight':
        spell = copy.copy(figureEight)
    totalInCast = 0
    spellCopy = copy.copy(spell)
    while len(spellCopy) >= 2:
        y = spellCopy.pop()
        x = spellCopy.pop()
        if isInCast(app, x, y):
            totalInCast += 1
    fractionScore = totalInCast / (len(spell)/2)
    return fractionScore

def isInCast(app, x, y):
    for blueX, blueY in app.path:
        if distance(x, y, blueX, blueY) <= app.blueR:
            return True
    return False


def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

def onStep(app):
    takeStep(app)

def takeStep(app):
    app.steps += 1

    if app.steps <= 90:    #loading time
        app.stage = 'preparing'
        if app.steps == 1:
            app.path = []
    elif app.steps <= 180:    #drawing time
        app.stage = 'drawing'
    elif app.steps <= 360:
        app.stage = 'resting'
        if app.steps == 181:
            app.error = calculateError(app)
            app.currentSpell = chooseSpell(app)
    else:
        app.steps = 0

def main():
    runApp()
    
main()
