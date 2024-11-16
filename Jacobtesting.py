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

    cv2.imshow('lol', frameReversed)
    cv2.imshow('WIZARD', mask)

    x, y = computeAveragePosition(mask)

    pos = (x * 1000 // (mask[0].size), y * 600 // (mask[:,0].size), int(np.mean(mask, (0, 1)) * 50))

    return pos

camera = cv2.VideoCapture(0)

def onAppStart(app):
    app.position = (0, 0, 0)
    app.casting = True

def onStep(app):
    if app.casting:
        app.position = capturePosition()

    if app.position[2] > 30:
        app.casting = False

def redrawAll(app):
    if app.casting:
        drawCircle(app.position[0], app.position[1], 10, fill='red')
    else:
        drawLabel('Casted!', app.width/2, app.height/2, fill='blue', size=56)

def main():
    runApp(1000, 600)

main()