# ALL CITATIONS ARE IN TRIPLE SINGLE QUOTES ABOVE THE CODE WHERE THEY ARE FIRST REFERENCED

from cmu_graphics import *

# initialzes all variables
def onAppStart(app):
    # sets active screen to home screen
    setActiveScreen('home')

    # sets app size
    app.width = 1000
    app.height = 600

    # initializing text color
    app.titleColor = gradient('yellow', 'orange', start = 'left')
    app.playColor = gradient('yellow', 'orange', start = 'left')
    app.instrColor = gradient('yellow', 'orange', start = 'left')

    # sets game font
    '''Blacksword font is from dafont.com'''
    app.font = 'Blacksword'

    # sets background image
    '''The background image is from wallpapersden.com and is titled Hogwarts Harry Potter School Wallpaper'''
    app.backgroundURL = 'hogwartsbg.jpg'



# ============================================================================================================================================================================
# HOME SCREEN
# ============================================================================================================================================================================

# draws home screen
def home_redrawAll(app):
    # calculations for proper image positioning
    imageWidth, imageHeight = getImageSize(app.backgroundURL)
    widthReduction = imageWidth / app.width
    imageRealWidth = imageWidth / widthReduction
    heightReduction = imageHeight / app.height
    imageRealHeight = imageHeight / heightReduction

    # draws background of game
    drawImage(app.backgroundURL, 0, 0, width = imageRealWidth, height = imageRealHeight)

    # draws game title w/ shadow
    drawLabel('Game Title Here', app.width / 2, app.height / 5 + 5, size = 75, fill = 'black', font = app.font)
    drawLabel('Game Title Here', app.width / 2, app.height / 5, size = 75, fill = app.titleColor, font = app.font)

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
    if home_isTouchingInstr(app, mouseX, mouseY):
        setActiveScreen('instr')

# # performs actions on mouse move while on home screen // IGNORE FOR NOW (laggy)
# def home_onMouseMove(app, mouseX, mouseY):
#     if home_isTouchingPlay(app, mouseX, mouseY):
#         app.playColor = 'white'
#     else:
#         app.playColor = gradient('yellow', 'orange', start = 'left')
#     if home_isTouchingInstr(app, mouseX, mouseY):
#         app.instrColor = 'white'
#     else:
#         app.instrColor = gradient('yellow', 'orange', start = 'left')

# checks if play button is touched
def home_isTouchingPlay(app, x, y):
    return x >= (app.width / 2 - 120) and x <= app.width / 2 + 120 and y <= app.height / 2 + 45 and y >= app.height / 2 - 45

# checks if instructions button is touched
def home_isTouchingInstr(app, x, y):
    return x >= (app.width / 2 - 120) and x <= app.width / 2 + 120 and y <= app.height / 2 + 100 and y >= app.height / 2 + 40



# ============================================================================================================================================================================
# INSTRUCTIONS SCREEN
# ============================================================================================================================================================================

# draws instructions screen
def instr_redrawAll(app):
    # calculations for proper image positioning
    imageWidth, imageHeight = getImageSize(app.backgroundURL)

    widthReduction = imageWidth / app.width
    imageRealWidth = imageWidth / widthReduction

    heightReduction = imageHeight / app.height
    imageRealHeight = imageHeight / heightReduction

    # draws background of game
    drawImage(app.backgroundURL, 0, 0, width = imageRealWidth, height = imageRealHeight)

    # draws title
    drawLabel('Instructions', app.width / 2, app.height / 5 + 5, size = 75, fill = 'black', font = app.font)
    drawLabel('Instructions', app.width / 2, app.height / 5, size = 75, fill = app.titleColor, font = app.font)

# performs actions on key press in instructions screen
def instr_onKeyPress(app, key):
    if key == 'escape':
        setActiveScreen('home')



# ============================================================================================================================================================================
# PLAY SCREEN
# ============================================================================================================================================================================

# draws play screen
def play_redrawAll(app):
    # calculations for proper image positioning
    imageWidth, imageHeight = getImageSize(app.backgroundURL)

    widthReduction = imageWidth / app.width
    imageRealWidth = imageWidth / widthReduction

    heightReduction = imageHeight / app.height
    imageRealHeight = imageHeight / heightReduction

    # draws background of game
    drawImage(app.backgroundURL, 0, 0, width = imageRealWidth, height = imageRealHeight)

    drawLabel('Play screen', app.width / 2, app.height / 5 + 5, size = 75, fill = 'black', font = app.font)
    drawLabel('Play screen', app.width / 2, app.height / 5, size = 75, fill = app.titleColor, font = app.font)


# ============================================================================================================================================================================
# MAIN
# ============================================================================================================================================================================

def main():
    runAppWithScreens('home')

main()