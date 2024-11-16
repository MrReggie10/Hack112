import cv2
import numpy as np

camera = cv2.VideoCapture(0)

def generateColorMask(img):
    lowerBound = np.array([10, 210, 190])
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

while True:
    ret, frame = camera.read()
    frameReversed = frame[:, ::-1]
    mask = generateColorMask(frameReversed)
    cv2.imshow('WIZARD', mask)

    x, y = computeAveragePosition(mask)

    pos = (x, y, int(np.mean(mask, (0, 1)) * 50))

    print(pos)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()