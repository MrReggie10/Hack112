import cv2
import numpy as np
from cmu_graphics import *
import math, random
from types import SimpleNamespace
import copy
from Spells import Spell
import os, pathlib

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
    if frame.all != None:
        frameReversed = frame[:, ::-1]
        mask = generateColorMask(frameReversed)

        x, y = computeAveragePosition(mask)
    else:
        x, y = 0

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

def onAppStart(app):
    # sets active screen to home screen
    setActiveScreen('home')

    # sets app size
    app.width = 1500
    app.height = 850

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
    # paused
    app.pausedState = None

    app.calibrationTimer = 0
    app.castedTimer = 0
    app.startingTimer = 0
    app.newStageTimer = 0
    app.loseSoundPlayed = False

    app.spellList = ['circle', 'figureEight', 'star', 'lightningBolt', 'tp', 'duck']
    app.currentSpell = None
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

    # The sounds are from https://www.myinstants.com/
    app.voldemortSound = loadSound('voldemort.mp3')
    app.spellCastSound = loadSound('spellCastSound.wav')
    app.robloxDeath = loadSound('robloxDeath.mp3')
    app.victorySound = loadSound('victorySound.mp3')

    # sets active screen to home screen
    setActiveScreen('home')

    # sets app size
    app.width = 1500
    app.height = 850

    # initializing text color
    app.titleColor = gradient('yellow', 'orange', start = 'left')
    app.playColor = gradient('yellow', 'orange', start = 'left')
    app.instrColor = gradient('yellow', 'orange', start = 'left')
    app.resumeColor = gradient('yellow', 'orange', start = 'left')
    app.backColor = gradient('yellow', 'orange', start = 'left')
    app.redColor = gradient(rgb(157, 2, 8), rgb(208, 0, 0), start = 'left')
    app.blueColor = gradient(rgb(0, 150, 199), rgb(0, 180, 216), start = 'left')
    app.greenColor = gradient(rgb(56, 176, 0), rgb(112, 224, 0), start = 'left')
    app.orangeColor = gradient(rgb(255, 136, 0), rgb(255, 170, 0), start = 'left')
    app.yellowColor = gradient('yellow', 'orange', start = 'left')
    app.purpleColor = gradient(rgb(123, 44, 191), rgb(60, 9, 108), start = 'left')

    # sets game font
    '''Blacksword font is from dafont.com'''
    app.font = 'Blacksword'



def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath) 
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def chooseSpell(app):
    index = random.randrange(len(app.spellList))
    if app.currentSpell == None:
        return app.spellList[index]
    while app.spellList[index] == app.currentSpell:
        index = random.randrange(len(app.spellList))
    return app.spellList[index]

def drawSpell(app, opc = 100):
    if app.currentSpell == 'circle':
        drawPolygon(*circle, fill=None, border='red', opacity=opc)
        drawLabel('Expelliarmus!', app.width/2, app.height*(3/4) + 5, size=40, fill='black', opacity=opc, font = app.font)
        drawLabel('Expelliarmus!', app.width/2, app.height*(3/4), size=40, fill=app.redColor, opacity=opc, font = app.font)
    elif app.currentSpell == 'figureEight':
        drawPolygon(*figureEight, fill=None, border='red', opacity=opc)
        drawLabel('Reducto!', app.width/2, app.height*(3/4) + 5, size=40, fill='black', opacity=opc, font = app.font)
        drawLabel('Reducto!', app.width/2, app.height*(3/4), size=40, fill=app.redColor, opacity=opc, font = app.font)
    elif app.currentSpell == 'star':
        drawPolygon(*star, fill=None, border='red', opacity=opc)
        drawLabel('Wingardium Leviosa!', app.width/2, app.height*(3/4) + 5, size=40, fill='black', opacity=opc, font = app.font)
        drawLabel('Wingardium Leviosa!', app.width/2, app.height*(3/4), size=40, fill=app.redColor, opacity=opc, font = app.font)
    elif app.currentSpell == 'lightningBolt':
        drawPolygon(*lightningBolt, fill=None, border='red', opacity=opc)
        drawLabel('Expecto Patronum!', app.width/2, app.height*(3/4) + 5, size=40, fill='black', opacity=opc, font = app.font)
        drawLabel('Expecto Patronum!', app.width/2, app.height*(3/4), size=40, fill=app.redColor, opacity=opc, font = app.font)
    elif app.currentSpell == 'tp':
        drawPolygon(*tp, fill=None, border='red', opacity=opc)
        drawLabel('The Most Terrifying Spell!', app.width/2, app.height*(3/4) + 5, size=40, fill='black', opacity=opc, font = app.font)
        drawLabel('The Most Terrifying Spell!', app.width/2, app.height*(3/4), size=40, fill=app.redColor, opacity=opc, font = app.font)
    elif app.currentSpell == 'duck':
        drawPolygon(*duck, fill=None, border='red', opacity=opc)
        drawLabel('KING!', app.width/2, app.height*(3/4) + 5, size=40, fill='black', opacity=opc, font = app.font)
        drawLabel('KING!', app.width/2, app.height*(3/4), size=40, fill=app.redColor, opacity=opc, font = app.font)

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

def play_onStep(app):

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
            app.errorCalculated = False

    if app.state == 'casted':
        if not app.errorCalculated:
            app.spellCastSound.play()
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
                app.victorySound.play()
            else:
                app.state = 'starting'
                app.robloxDeath.play()
    else:
        app.newStageTimer = 0
    
    if app.state == 'lose':
        if app.loseSoundPlayed == False:
            app.voldemortSound.play(loop=True)
            app.loseSoundPlayed = True
    else:
        app.loseSoundPlayed = False


def home_redrawAll(app):
    # draws background of game
    drawImage(app.backgroundURL, 0, 0, width = app.width, height = app.height)

    # draws game title w/ shadow
    drawLabel('Game Title', app.width / 2, app.height / 5 + 5, size = 75, fill = 'black', font = app.font)
    drawLabel('Game Title', app.width / 2, app.height / 5, size = 75, fill = app.titleColor, font = app.font)

    # draws play game button w/ shadow
    drawLabel('Play Game', app.width / 2, app.height / 2 - 15, size = 45, fill = 'black', font = app.font)
    drawLabel('Play Game', app.width / 2, app.height / 2 - 20, size = 45, fill = app.playColor, font = app.font)

    # draws instructions button w/ shadow
    drawLabel('Instructions', app.width / 2, app.height / 2 + 70, size = 45, fill = 'black', font = app.font)
    drawLabel('Instructions', app.width / 2, app.height / 2 + 65, size = 45, fill = app.instrColor, font = app.font)

# performs actions on mouse press while on home screen
def home_onMousePress(app, mouseX, mouseY):
    if home_isTouchingPlay(app, mouseX, mouseY):
        setActiveScreen('play')
        app.playColor = gradient('yellow', 'orange', start = 'left')
    if home_isTouchingInstr(app, mouseX, mouseY):
        setActiveScreen('instr')
        app.instrColor = gradient('yellow', 'orange', start = 'left')

# performs actions on mouse move while on home screen
def home_onMouseMove(app, mouseX, mouseY):
    if home_isTouchingPlay(app, mouseX, mouseY):
        app.playColor = 'white'
    else:
        app.playColor = gradient('yellow', 'orange', start = 'left')
    if home_isTouchingInstr(app, mouseX, mouseY):
        app.instrColor = 'white'
    else:
        app.instrColor = gradient('yellow', 'orange', start = 'left')

# checks if play button is touched
def home_isTouchingPlay(app, x, y):
    return x >= (app.width / 2 - 120) and x <= app.width / 2 + 120 and y <= app.height / 2 + 40 and y >= app.height / 2 - 45

# checks if instructions button is touched
def home_isTouchingInstr(app, x, y):
    return x >= (app.width / 2 - 120) and x <= app.width / 2 + 120 and y <= app.height / 2 + 100 and y >= app.height / 2 + 40



# ============================================================================================================================================================================
# INSTRUCTIONS SCREEN
# ============================================================================================================================================================================

# draws instructions screen
def instr_redrawAll(app):
    # draws background of game
    drawImage(app.backgroundURL, 0, 0, width = app.width, height = app.height)

    # draws title
    drawLabel('Instructions', app.width / 2, app.height / 5 + 5, size = 75, fill = 'black', font = app.font)
    drawLabel('Instructions', app.width / 2, app.height / 5, size = 75, fill = app.titleColor, font = app.font)

    # draws instructions
    drawLabel('1) To cast spells, move the duck to an appropriate distance from the screen,', app.width / 2, app.height / 2 - 130, size = 35, fill = 'black', font = app.font)
    drawLabel('1) To cast spells, move the duck to an appropriate distance from the screen,', app.width / 2, app.height / 2 - 135, size = 35, fill = app.instrColor, font = app.font)
    drawLabel(' then trace the outline of the spell, and cast the spell by pushing the duck forward', app.width / 2, app.height / 2 - 55, size = 35, fill = 'black', font = app.font)
    drawLabel(' then trace the outline of the spell, and cast the spell by pushing the duck forward', app.width / 2, app.height / 2 - 60, size = 35, fill = app.instrColor, font = app.font)

    drawLabel('2) To pause the game, press escape', app.width / 2, app.height / 2 + 20, size = 35, fill = 'black', font = app.font)
    drawLabel('2) To pause the game, press escape', app.width / 2, app.height / 2 + 15, size = 35, fill = app.instrColor, font = app.font)

    drawLabel('3) To exit this screen, press escape', app.width / 2, app.height / 2 + 95, size = 35, fill = 'black', font = app.font)
    drawLabel('3) To exit this screen, press escape', app.width / 2, app.height / 2 + 90, size = 35, fill = app.instrColor, font = app.font)

# performs actions on key press in instructions screen
def instr_onKeyPress(app, key):
    if key == 'escape':
        setActiveScreen('home')

# draws play screen
def play_redrawAll(app):
    # draws background of game
    drawImage(app.backgroundURL, 0, 0, width = app.width, height = app.height)

    if app.state == 'starting':
        drawLabel("Ready?", app.width/2, app.height/2 + 5, fill='black', size=28, font = app.font)
        drawLabel("Ready?", app.width/2, app.height/2, fill=app.blueColor, size=28, font = app.font)
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
            drawLabel("Too close!", app.width/2, app.height/2 + 5, fill='black', size=50, font = app.font)
            drawLabel("Too close!", app.width/2, app.height/2, fill=app.redColor, size=50, font = app.font)
        elif app.position[2] < app.tooFar:
            drawLabel("Too far!", app.width/2, app.height/2 + 5, fill='black', size=50, font = app.font)
            drawLabel("Too far!", app.width/2, app.height/2, fill=app.redColor, size=50, font = app.font)
        else:
            drawLabel("Perfect!", app.width/2, app.height/2 + 5, fill='black', size=50, font = app.font)
            drawLabel("Perfect!", app.width/2, app.height/2, fill=app.greenColor, size=50, font = app.font)
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
        drawLabel('Cast!', app.width/2, app.height/2 + 5, fill='black', size=56, font = app.font)
        drawLabel('Cast!', app.width/2, app.height/2, fill=app.blueColor, size=56, font = app.font)
        drawLabel(str(app.error), app.width/2, app.height/2 - 145, size=100, fill='black', font = app.font)
        drawLabel(str(app.error), app.width/2, app.height/2 - 150, size=100, fill=app.purpleColor, font = app.font)
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
        drawLabel('Victory!', app.width/2, app.height/2 + 5, fill=app.yellowColor, size=56, font = app.font)
        drawLabel('Victory!', app.width/2, app.height/2, fill=app.yellowColor, size=56, font = app.font)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)
    
    elif app.state == 'win':
        drawLabel('You are win!', app.width/2, app.height/2 + 5, fill='black', size=56, font = app.font)
        drawLabel('You are win!', app.width/2, app.height/2, fill=app.orangeColor, size=56, font = app.font)
        drawImage(app.austin, 0, 750, align='bottom-left', width=200, height=200)
        drawImage(app.koz, 0, 650, align='bottom-left', width=75, height=75)
    
    elif app.state == 'lose':
        drawLabel('Game over :(', app.width/2, app.height/2 + 5, fill='black', size=80, font = app.font)
        drawLabel('Game over :(', app.width/2, app.height/2, fill=app.orangeColor, size=80, font = app.font)

    elif app.state == 'paused':

        # draws box
        drawRect(0, 0, app.width, app.height, fill = 'white', opacity = 50)
        drawRect(app.width / 2 - 200, app.height / 2 - 100, 400, 200, fill = 'black', opacity = 75, border = 'black')

        # draws title
        drawLabel('Paused', app.width / 2, app.height / 2 - 145, size = 55, fill = 'black', font = app.font)
        drawLabel('Paused', app.width / 2, app.height / 2 - 150, size = 55, fill = app.playColor, font = app.font)

        # draws resume button
        drawLabel('Resume', app.width / 2, app.height / 2 - 45, size = 45, fill = 'black', font = app.font)
        drawLabel('Resume', app.width / 2, app.height / 2 - 50, size = 45, fill = app.resumeColor, font = app.font)

        # draws back to home button
        drawLabel('Go Back to Home', app.width / 2, app.height / 2 + 55, size = 45, fill = 'black', font = app.font)
        drawLabel('Go Back to Home', app.width / 2, app.height / 2 + 50, size = 45, fill = app.backColor, font = app.font)

# performs conditions if key is pressed while playing game
def play_onKeyPress(app, key):
    if key == 'escape':
        app.pausedState = app.state
        app.state = 'paused'

# performs conditions if mouse is pressed while playing game
def play_onMousePress(app, mouseX, mouseY):
    if app.state == 'paused':
        if play_isTouchingResume(app, mouseX, mouseY):
            app.state = app.pausedState
        elif play_isTouchingGoToHome(app, mouseX, mouseY):
            app.playingGame = False
            setActiveScreen('home')
        
# checks if user is touching resume button while paused
def play_isTouchingResume(app, x, y):
    return x <= app.width / 2 + 80 and x >= app.width / 2 - 80 and y <= app.height / 2 - 15 and y >= app.height / 2 - 75

# checks if user is touching go to home button while paused
def play_isTouchingGoToHome(app, x, y):
    return x <= app.width / 2 + 180 and x >= app.width / 2 - 180 and y <= app.height / 2 + 85 and y >= app.height / 2 + 25

# performs actions on mouse move while playing game
def play_onMouseMove(app, mouseX, mouseY):
    if app.state == 'paused':
        if play_isTouchingResume(app, mouseX, mouseY):
            app.resumeColor = 'white'
        else:
            app.resumeColor = gradient('yellow', 'orange', start = 'left')
        if play_isTouchingGoToHome(app, mouseX, mouseY):
            app.backColor = 'white'
        else:
            app.backColor = gradient('yellow', 'orange', start = 'left')

camera = cv2.VideoCapture(0)

def main():
    runAppWithScreens('home')

main()