# ALL CITATIONS ARE IN TRIPLE SINGLE QUOTES ABOVE THE CODE WHERE THEY ARE FIRST REFERENCED

from cmu_graphics import *

# initialzes all variables
def onAppStart(app):
    # sets active screen to home screen
    setActiveScreen('home')

    # sets app size
    app.width = 1500
    app.height = 850

    # boolean variables, paused and game over, to determine those conditions
    app.paused = False
    app.gameOver = False

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

    # draws instructions
    drawLabel('1) To cast spells, ...', app.width / 2, app.height / 2 - 55, size = 45, fill = 'black', font = app.font)
    drawLabel('1) To cast spells, ...', app.width / 2, app.height / 2 - 60, size = 45, fill = app.instrColor, font = app.font)

    drawLabel('2) To pause the game, press escape', app.width / 2, app.height / 2 + 20, size = 45, fill = 'black', font = app.font)
    drawLabel('2) To pause the game, press escape', app.width / 2, app.height / 2 + 15, size = 45, fill = app.instrColor, font = app.font)

    drawLabel('3) To exit this screen, press escape', app.width / 2, app.height / 2 + 95, size = 45, fill = 'black', font = app.font)
    drawLabel('3) To exit this screen, press escape', app.width / 2, app.height / 2 + 90, size = 45, fill = app.instrColor, font = app.font)

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

    # draws pause menu
    if app.paused:
        # draws box
        drawRect(0, 0, app.width, app.height, fill = 'white', opacity = 50)
        drawRect(app.width / 2 - 200, app.height / 2 - 100, 400, 200, fill = 'black', opacity = 75, border = 'black')

        # draws title
        drawLabel('Paused', app.width / 2, app.height / 2 - 145, size = 55, fill = 'black', font = app.font)
        drawLabel('Paused', app.width / 2, app.height / 2 - 150, size = 55, fill = app.playColor, font = app.font)

        # draws resume button
        drawLabel('Resume', app.width / 2, app.height / 2 - 45, size = 45, fill = 'black', font = app.font)
        drawLabel('Resume', app.width / 2, app.height / 2 - 50, size = 45, fill = app.playColor, font = app.font)

        # draws back to home button
        drawLabel('Go Back to Home', app.width / 2, app.height / 2 + 55, size = 45, fill = 'black', font = app.font)
        drawLabel('Go Back to Home', app.width / 2, app.height / 2 + 50, size = 45, fill = app.playColor, font = app.font)

# performs conditions if key is pressed while playing game
def play_onKeyPress(app, key):
    if key == 'escape':
        app.paused = True

# performs conditions if mouse is pressed while playing game
def play_onMousePress(app, mouseX, mouseY):
    if app.paused:
        if play_isTouchingResume(app, mouseX, mouseY):
            app.paused = False
        elif play_isTouchingGoToHome(app, mouseX, mouseY):
            app.paused = False
            setActiveScreen('home')
        
# checks if user is touching resume button while paused
def play_isTouchingResume(app, x, y):
    return x <= app.width / 2 + 80 and x >= app.width / 2 - 80 and y <= app.height / 2 - 15 and y >= app.height / 2 - 75

# checks if user is touching go to home button while paused
def play_isTouchingGoToHome(app, x, y):
    return x <= app.width / 2 + 180 and x >= app.width / 2 - 180 and y <= app.height / 2 + 85 and y >= app.height / 2 + 25



# ============================================================================================================================================================================
# MAIN
# ============================================================================================================================================================================

def main():
    runAppWithScreens('home')

main()