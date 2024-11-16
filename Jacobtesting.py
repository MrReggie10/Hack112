import cv2
import numpy as np
from cmu_graphics import *

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

def onStep(app):

    if app.state == 'starting':
        app.startingTimer += 1
        if app.startingTimer > 60:
            app.state = 'calibrating'
    else:
        app.startingTimer = 0

    if app.state == 'calibrating':
        app.position = capturePosition()
        if app.position[2] > 30 or app.position[2] < 3:
            app.calibrationTimer = 0
        else:
            app.calibrationTimer += 1
            if app.calibrationTimer > 60:
                app.state = 'casting'

    if app.state == 'casting':
        app.position = capturePosition()
        if app.position[2] > 30:
            app.state = 'casted'

    if app.state == 'casted':
        app.castedTimer += 1
        if app.castedTimer > 60:
            app.state = 'casting'
    else:
        app.castedTimer = 0

def redrawAll(app):
    if app.state == 'starting':
        drawLabel("Ready?", app.width/2, app.height/2, fill='blue', size=28)

    elif app.state == 'calibrating':
        if app.position[2] > 30:
            drawLabel("Too close!", app.width/2, app.height/2, fill='red', size=28)
        elif app.position[2] < 3:
            drawLabel("Too far!", app.width/2, app.height/2, fill='red', size=28)
        else:
            drawLabel("Perfect!", app.width/2, app.height/2, fill='green', size=28)

    elif app.state == 'casting':
        drawCircle(app.position[0], app.position[1], 10, fill='red')

    elif app.state == 'casted':
        drawLabel('Casted!', app.width/2, app.height/2, fill='blue', size=56)

def main():
    runApp(1500, 850)

main()