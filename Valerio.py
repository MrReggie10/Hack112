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

def redrawAll(app):
    drawCircle(app.cx, app.cy, 15, fill='blue')
    drawSpell(app)

def onMouseMove(app, mouseX, mouseY):
    app.cx, app.cy = mouseX, mouseY

def chooseSpell(app):
    index = random.randrange(len(app.spellList))
    return app.spellList[index]

def drawSpell(app):
    if app.currentSpell == 'circle':
        drawCircle(app.width/2, app.height/2, 100, fill=None, border='purple')
        drawLabel('Expelliarmus!', app.width/2, app.height/2, size=16, fill='purple')

def main():
    runApp()
    
main()
