from cmu_graphics import *
import math, random
from types import SimpleNamespace


###Enemies with damage that scales on how well you follow the spell path
#Objects: enemies ?
#Make list of spells

def onAppStart(app):
    app.width = 800
    app.height = 600
    app.cx, app.cy = 200, 200
    app.spellList = ['circle']
    app.currentSpell = chooseSpell(app)
    app.error = 0
    app.path = []
    app.fun = True
    

def redrawAll(app):
    drawCircle(app.cx, app.cy, 15, fill='blue')
    drawSpell(app)
    drawLabel(f'{app.error}', app.width/6, app.height/6)
    for x, y in app.path:
        drawCircle(x, y, 15, fill='blue', opacity=50)

def onMouseMove(app, mouseX, mouseY):
    app.cx, app.cy = mouseX, mouseY
    # app.error = calculateError(app)
    app.path.append((mouseX, mouseY))


def chooseSpell(app):
    index = random.randrange(len(app.spellList))
    return app.spellList[index]

def drawSpell(app):
    if app.currentSpell == 'circle':
        drawCircle(app.width/2, app.height/2, 100, fill=None, border='red')
        drawLabel('Expelliarmus!', app.width/2, app.height/2, size=16, fill='red')

def calculateError(app):
    if app.currentSpell == 'circle':
        dist = distance(app.cx, app.cy, app.width/2, app.height/2)
        return (dist - 100) / 100

def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1 - y0)**2)**0.5

def main():
    runApp()
    
main()
