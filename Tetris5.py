import random,time,pygame,sys,shelve
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 480
WINDOWHEIGHT = 400
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
EMPTY = '.'
TRACK =0

#movement frequency of pieces
MOVESIDEWAYSFREQ = 0.05
MOVEDOWNFREQ = 0.05

#margin from top 
TOPMARGIN = WINDOWHEIGHT-(BOARDHEIGHT*BOXSIZE)-5

#set up colors
WHITE = (255,255,255)
GRAY = (185,185,185)
GREY = (171,163,163)
BLACK = (0,0,0)
RED = (255,51,51)
LIGHTRED = (255,102,102)
GREEN = (0,204,0)
LIGHTGREEN = (204,255,153)
BLUE = (51,51,255)
LIGHTBLUE = (153,153,255)
YELLOW = (155,155,0)
LIGHTYELLOW = (255,255,102)
CYAN = (0,255,255)
LIGHTCYAN = (224,255,255)
VIOLETTE = (226,16,233)
LIGHTVIOLETTE = (238,129,242)
ORANGE = (255,128,0)
LIGHTORANGE = (255,178,102)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS =( BLUE,GREEN,RED,YELLOW,CYAN,VIOLETTE,ORANGE)
LIGHTCOLORS = (LIGHTBLUE,LIGHTGREEN,LIGHTRED,LIGHTYELLOW,LIGHTCYAN,LIGHTVIOLETTE,LIGHTORANGE)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                      '.....',
                      '..OO.',
                      '.OO..',
                      '.....'],
                    ['.....',
                      '..O..',
                      '..OO.',
                      '...O.',
                      '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                      '.....',
                      '.OO..',
                      '..OO.',
                      '.....'],
                    ['.....',
                      '..O..',
                      '.OO..',
                      '.O...',
                      '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

SHAPES = {'S':S_SHAPE_TEMPLATE,
          'Z':Z_SHAPE_TEMPLATE,
          'J':J_SHAPE_TEMPLATE,
          'L':L_SHAPE_TEMPLATE,
          'I':I_SHAPE_TEMPLATE,
          'O':O_SHAPE_TEMPLATE,
          'T':T_SHAPE_TEMPLATE}


def mixerStart():
    randomtrack = ['1','2','3','4','5']
    pygame.mixer.init()
    track = 0
    s1 = pygame.mixer.Sound('s1.ogg')
    s2 = pygame.mixer.Sound('s2.ogg')
    s3 = pygame.mixer.Sound('s3.ogg')
    s4 = pygame.mixer.Sound('s4.ogg')
    s5 = pygame.mixer.Sound('s5.ogg')
    pygame.mixer.music.load('s'+ randomtrack[0] +'.ogg')
    pygame.mixer.music.play(-1, 0.0)
    return track,randomtrack
 
def mixer(track,randomtrack):
    track = (track+1) % 5
    pygame.mixer.music.load('s'+ randomtrack[track] +'.ogg')
    pygame.mixer.music.play(-1, 0.0)
    return track

def getHighScore():
    #load previous highscore if exists
    d = shelve.open('score.txt')
    try:
        highscore = d['highscore']
    except:
        highscore = 0
    d.close()
    return highscore

def newHighScore(score,highscore):
    d = shelve.open('score.txt')
    if score > highscore:
        d['highscore'] = score
    d.close()

def showVideo():
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie('Intro.mpg')
    movie_screen = pygame.Surface(movie.get_size()).convert()

    movie.set_display(movie_screen)
    movie.play()

    playing = True
    while playing and movie.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False
        DISPLAYSURF.blit(movie_screen,(70,70))
        pygame.display.update()
        clock.tick(FPS)

def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT,BIGFONT,GRIDSURF,WHERESURF,background,randomtrack
    background = pygame.image.load('background.png')
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.Font(None,40)
    BIGFONT = pygame.font.Font(None,100)
    pygame.display.set_caption('TetrisGK')
    pygame.mixer.quit()
    showVideo()
    pygame.mixer.init()
    DISPLAYSURF.fill(BLACK)
    showTextScreen('TetrisGK')
    track,randomtrack = mixerStart()
    while True:
        score,highscore = runGame(track,randomtrack)
        newHighScore(score,highscore)
        pygame.mixer.music.stop()
        showTextScreen('Game Over')
        pygame.mixer.init()
        track = mixer(track,randomtrack)

def runGame(track,randomtrack):
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False #for knowing when to create new piece
    movingLeft = False
    movingRight = False
    score = 0
    level,fallFreq = calculateLevelAndFallFreq(score)
    highscore = getHighScore()
    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    musicplaying = True

    while True:#game loop
        if fallingPiece == None: #we need to create a new piece
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() #reset time
            if not isValidPosition(board,fallingPiece):#no more space , player has lost
                return score,highscore
        checkForQuit()
        for event in pygame.event.get(): #check for keys pressed loop
            if (event.type == KEYUP):
                if(event.key == K_p): #Pause game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.pause()
                    showTextScreen('Paused')
                    pygame.mixer.music.unpause()
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif(event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif(event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif(event.key == K_DOWN or event.key == K_s):
                    movingDown = False
            elif (event.type == KEYDOWN):
                #move sideways
                if((event.key == K_LEFT or event.key == K_a) and isValidPosition(board,fallingPiece,adjX = -1)):
                   #fallingPiece['x'] -= 1 for some reason i have to do that
                   movingRight = False
                   movingLeft = True
                   lastMoveSideWaysTime = time.time()
                elif((event.key == K_RIGHT or event.key == K_d) and isValidPosition(board,fallingPiece,adjX = 1)):
                     fallingPiece['x'] += 1
                     movingLeft = False
                     movingRight = True
                     lastMoveSidewaysTime = time.time()
                #rotate block
                elif(event.key == K_UP or event.key == K_w):
                     fallingPiece['rotation'] = (fallingPiece['rotation']+1)%len(SHAPES[fallingPiece['shape']])
                     if(not isValidPosition(board,fallingPiece)):
                         fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                elif(event.key == K_q):#rotate other direction
                     fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                     if(not isValidPosition(board, fallingPiece)):
                         fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
                elif(event.key == K_DOWN or event.key == K_s):#make block fall faster
                     movingDown = True
                     if(isValidPosition(board,fallingPiece,adjY =1)):
                        fallingPiece['y'] += 1
                     lastMoveDownTime = time.time()
                elif(event.key == K_n):
                    if(musicplaying == True):
                        track = mixer(track,randomtrack)
                elif(event.key == ord('m')):
                    if(musicplaying == True):
                        pygame.mixer.music.pause()#check why not stopping
                        musicplaying = False
                    else:
                        pygame.mixer.music.unpause()
                        musicplaying = True
                elif(event.key == K_SPACE):#move block down to final position
                        movingDown = False
                        movingLeft = False
                        movingRight = False
                        for i in range(1,BOARDHEIGHT):
                            if (not isValidPosition(board,fallingPiece,adjY=i)):
                                break
                        fallingPiece['y'] +=i-1
                                
        #block movement because of player pressing keys
        if((movingLeft or movingRight) and time.time() - lastMoveSidewaysTime >  MOVESIDEWAYSFREQ):
            if(movingLeft and isValidPosition(board,fallingPiece,adjX=-1)):
               fallingPiece['x'] -= 1
            elif(movingRight and isValidPosition(board,fallingPiece,adjX=1)):
                 fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time()-lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        #let piece fall
        if time.time() - lastFallTime > fallFreq:
            #check if piece has contact from the down side
            if not isValidPosition(board,fallingPiece,adjY=1):
                 #piece landed , add it to board
                 addToBoard(board,fallingPiece)
                 score += removeCompleteLines(board)
                 level,fallFreq = calculateLevelAndFallFreq(score)
                 fallingPiece = None
            else:
                 #piece just moves down 1 block size
                 fallingPiece['y'] += 1
                 lastFallTime = time.time()

        #update screen
        DISPLAYSURF.fill(BGCOLOR)
        if fallingPiece != None:
            drawBoard(board,fallingPiece)
        else:
            drawBoard(board,None)
        DISPLAYSURF.blit(background,(BOARDWIDTH*BOXSIZE+5,0))
        drawStatus(score,level,highscore)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text,font,color):
    surf = font.render(text,True,color)
    return surf,surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN,KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text):
    #for showing text in middle of screen until key is pressed
    titleSurf,titleRect = makeTextObjs(text,BIGFONT,TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2))
    DISPLAYSURF.blit(titleSurf,titleRect)

    #Draw text
    pressKeySurf,pressKeyRect = makeTextObjs('Press a key to play.',BASICFONT,TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)+50)
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT):#get all quit events
        terminate()
    for event in pygame.event.get(KEYUP):#get all KEYUP events
        if event.key == K_ESCAPE:
            terminate() #terminate if the KEYUP event was for esc key
        pygame.event.post(event)#put other objects back

def calculateLevelAndFallFreq(score):
    #Based on score return level the player is on and
    #how many seconds pass until a falling piece falls one space
    level = int(score/10) + 1
    fallFreq = 0.27 -(level * 0.02)
    return level,fallFreq

def getNewPiece():
    #return a random new piece in random rotation and color
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape':shape,
                'rotation':random.randint(0,len(SHAPES[shape])-1),
                'x':int(BOARDWIDTH/2)-int(TEMPLATEWIDTH/2),
                'y':-2,#start it above the board (i.e less than 0)
                'color':random.randint(0,len(COLORS)-1)}
    return newPiece

def addToBoard(board,piece):
    #fill in the board based on piece's location,shape and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != EMPTY:
                board[x + piece['x']][y + piece['y']] = piece['color']

def getBlankBoard():
    #create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK]*BOARDHEIGHT)
    return board

def isOnBoard(x,y):
    return x>=0 and x<BOARDWIDTH and y <BOARDHEIGHT

def isValidPosition(board,piece,adjX=0,adjY=0):
    #Return True if the piece is within board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == EMPTY:
                continue
            if not isOnBoard(x+piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != EMPTY:
                return False
    return True 

def isCompleteLine(board,y):
    #Return True if the line filled with boxes with no gaps
    for x in range(BOARDWIDTH):
        if board[x][y] == EMPTY:
            return False
    return True

def removeCompleteLines(board):
    #Remove any completed lines on the board,move everything above the down,
    #and return the number of complete lines
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1#start y at the bottom of the board
    while y>=0:
        if isCompleteLine(board,y):
            #Remove the line and pull boxes down by one line
            for pullDownY in range(y,0,-1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            #Set very top line to blank
            for x in range(BOARDWIDTH):
                board[x][0] = EMPTY
            numLinesRemoved += 1
            #On next iteration of loop y is the same
            #This is so that if the line that was pulled down is also
            #complete will be removed
        else:
            y -= 1#next row
    return numLinesRemoved

def convertToPixelCoords(boxx,boxy):
    #Convert the given xy coordinates of the board to xy
    #coordinates of the location on the screen
    return(2+(boxx*BOXSIZE)),(TOPMARGIN+(boxy*BOXSIZE))

def drawBox(boxx,boxy,color,pixelx=None,pixely=None):
    #draw a single box(each tetris piece has four boxes)
    #at xy coordinates on the board.Or,pixelx and pixely
    #are specified, draw to the pixel coordinates stored in
    #pixelx and pixely (this is used for next piece)
    if color == EMPTY:
        return
    if pixelx ==None and pixely == None:
        pixelx,pixely = convertToPixelCoords(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF,COLORS[color],(pixelx+1,pixely+1,BOXSIZE-1,BOXSIZE-1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))                

def drawBoard(board,isPiece):
    #draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, ( 0, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 3, (BOARDHEIGHT * BOXSIZE) +8), 5)

    #fill background
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (3, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    drawgrid(isPiece,board)
    #draw the individual boxes on board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x,y,board[x][y])

def drawStatus(score,level,highscore):
    #draw the score text
    scoreSurf = BASICFONT.render('Score %s'%score,True,TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH-180,20)
    DISPLAYSURF.blit(scoreSurf,scoreRect)
    #draw highscore
    highscoreSurf = BASICFONT.render('Highscore %s'%highscore,True,TEXTCOLOR)
    highscoreRect = highscoreSurf.get_rect()
    highscoreRect.topleft = (WINDOWWIDTH - 180, 50)
    DISPLAYSURF.blit(highscoreSurf,highscoreRect)
    #draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 180, 80)
    DISPLAYSURF.blit(levelSurf, levelRect)

def drawPiece(piece,pixelx=None,pixely=None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
    #draw each block that make a piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != EMPTY:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))
                
def drawNextPiece(piece):
    #draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 180, 180)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    pygame.draw.circle(DISPLAYSURF,BLACK,(WINDOWWIDTH-180 + 2*BOXSIZE + 10,270 + 2*BOXSIZE + 10),60,0)
    drawPiece(piece, pixelx=WINDOWWIDTH-180, pixely=270)

def drawgrid(isPiece,board):
    #draw the game grid
    GRIDSURF = pygame.Surface((int(BOARDWIDTH*BOXSIZE),int(BOARDHEIGHT*BOXSIZE)))
    if(isPiece != None):
        drawWherePieceGoes(isPiece,board,GRIDSURF)
    for y in range(BOARDHEIGHT):
        pygame.draw.line(GRIDSURF,GREY,(3,y*BOXSIZE-5),(BOARDWIDTH*BOXSIZE+3,y*BOXSIZE-5),1)
    for x in range(1,BOARDWIDTH):
        pygame.draw.line(GRIDSURF,GREY,(x*BOXSIZE+2,0),(x*BOXSIZE+2,BOARDHEIGHT*BOXSIZE-5),1)       
    GRIDSURF.set_alpha(30)
    DISPLAYSURF.blit(GRIDSURF,(0,0))

def drawWherePieceGoes(piece,board,GRIDSURF):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    for i in range(1,BOARDHEIGHT):
        if (not isValidPosition(board,piece,adjY=i)):
            break
    x = piece['x']
    y = piece['y'] + i-1
    pixelx, pixely = convertToPixelCoords(x, y)
    for xx in range(TEMPLATEWIDTH):
        for yy in range(TEMPLATEHEIGHT):
            if shapeToDraw[yy][xx] != BLANK:
                pygame.draw.rect(GRIDSURF,WHITE,((xx*BOXSIZE)+pixelx,(yy*BOXSIZE)+pixely,BOXSIZE,BOXSIZE))

if __name__ == '__main__':
    main()
                   
                      
