import math, random, sys, time
import pygame
import pokebase as pb


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

def unpause():
    global pause #declare to change the pause variable
    pause = False
    game_loop()

def paused():
    pauseText = pygame.font.SysFont('freesansbold.ttf', 30)
    textSurf, textRect = text_objects("Paused", pauseText)
    textRect.center = (HALF_WIDTH, HALF_HEIGHT)
    bg = pygame.image.load('BackgroundFinal.png').convert()
    SCREEN.blit(bg, (0, 0))
    #pygame.draw.rect(SCREEN, white, [screenWidth-60, 0, screenWidth, screenHeight-100])
    SCREEN.blit(textSurf, textRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Pokedex", 550, 0, 100, 50, white, light_gray, unpause)
        button("Pokemon", 550, 50, 100, 50, white, light_gray, unpause)
        button("Items", 550, 100, 100, 50, white, light_gray, unpause)
        button("Trainer", 550, 150, 100, 50, white, light_gray, unpause)
        button("Option", 550, 200, 100, 50, white, light_gray, unpause)
        button("QUIT", 550, 250, 100, 50, white, light_gray, quit_game)
        #pauseScreen = pygame.draw.Surface.rect(SCREEN, white, (0, 0, screenWidth, screenHeight), 0)
        #SCREEN.blit(pauseScreen, (490, 0))
        pygame.display.update()
        clock.tick(15)

def checkForPokemon():
    keys = pygame.key.get_pressed()
    routePokemon = [4, 7, 1, 6, 10]
    if keys[pygame.K_UP] or keys[pygame.K_DOWN] \
    or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        playerNum = random.randrange(1, 101)
        if playerNum in routePokemon:
            enemy = pb.pokemon_sprite(playerNum)
            enemy = enemy.path
            #print(playerNum)
            #print(enemy)
            enemy = pygame.image.load(enemy)
            #pokemonBattle(enemy)            
            fightScene(enemy, playerNum)
#define colors            
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
light_gray = (200, 200, 200)

#pokemon generating method, returns pokemon image and name   
def _createPokemon_(dbValue):
    sprite = pygame.image.load(pb.pokemon_sprite(dbValue).path)
    return sprite, pb.pokemon(dbValue)

#flip function
def flipImage(image):
    flipped = pygame.transform.flip(image, True, False)
    return flipped
#called message_display
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text,cX,cY,fontSize):
    largeText = pygame.font.Font('freesansbold.ttf', fontSize)#25
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = (cX, cY) #screenWidth/2, screenHeight/2
    SCREEN.blit(textSurf, textRect)
    #we have to update the screen after adding something
    pygame.display.update()
    #pause the game for 2 seconds to display the message
    #time.sleep(2)
    
#def pokemonBattle(pokemon):
#    SCREEN.blit(pokemon, (360, 360))

def battleWinner(pokename1, pokename2, health1, health2, enemy_damaged, player_damaged):
    clock.tick(15)
    #healthbar full (enemy)
    pygame.draw.rect(SCREEN,green,(100,90,100,10))
    #indicate damage to enemy
    pygame.draw.rect(SCREEN,white,[100,90,enemy_damaged,10])
    #healthbar full (player)
    pygame.draw.rect(SCREEN,green,(3*screenWidth/4 - 25,3*screenHeight/4 - 10,100,10))
    #indicate damage to player
    pygame.draw.rect(SCREEN,white,[3*screenWidth/4 - 25,3*screenHeight/4 - 10,player_damaged,10])
    
    if health1 == 0:    
        message_display(pokename2 + ' Fainted!',screenWidth/2, screenHeight/2, 25)
        time.sleep(1)
        pygame.mixer.music.stop()
        game_loop()
    elif health2 == 0:
        message_display(pokename1 + ' Fainted!',screenWidth/2, screenHeight/2, 25)
        time.sleep(1)
        pygame.mixer.music.stop()
        game_loop()
    else:
        return True
 ##################################################################################################################  
#fight scene function, for this to work there needs to be a user defined pokedex with id#, and random draw for enemies to battle
def fightScene(poke1, num):
    #define variable flags to track character entrance and key presses
    slideEnemy = True
    slidePlayer = True
    poke2 = None
    keyDown = False
    
    poke1hp = 100
    poke2hp = 100
    
    enemy_damaged = 0
    player_damaged = 0
    
    #track successful attacks after 3 success then special ability becomes available
    playerAttackSuccess = 0
    enemyAttackSuccess = 0
    #white screen to open the scene
    pygame.draw.rect(SCREEN,white,[0,0,screenWidth,screenHeight])
    
    #roll for who attacks first
    contestantTurn = random.randrange(1,3)
    clock.tick(15)
    #create fighting loop
    while True:
        
        #enemy entrance left to right                
        if slideEnemy:
            clock.tick(60)
            #load and play beginning ecounter music
            pygame.mixer.music.load('BeginningofPokemonEncounter.wav')
            pygame.mixer.music.play(1)
            time.sleep(2.5)
            #encounter loop music 
            pygame.mixer.music.load('PokemonTrainerBattle.wav')
            pygame.mixer.music.play(-1)
            for x in range(screenWidth - 125):
                SCREEN.blit(poke1, (x,100))
                time.sleep(.003)
                pygame.draw.rect(SCREEN,white,[x-25,100,20,200])
                pygame.display.update()
            SCREEN.fill(white)
            SCREEN.blit(poke1, (x,100))
        #SCREEN.fill(white)
 
         
        #give user a chance to select their available pokemon
            while(not keyDown):
                clock.tick(15)
                #wipe any previous messages in center of screen
                pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 65])
                message_display('Select Your pokemon[1- '+str(len(pokemon_Id))+']',screenWidth/2, screenHeight/2, 25)
                for event in pygame.event.get():
                    #check for keys pressed down
                    if event.type == pygame.KEYDOWN:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        #check for the number key pressed and if there are enough pokemon in the players pokedex   
                        elif event.key == pygame.K_1: 
                            playerSelection = 0
                        elif event.key == pygame.K_2 and len(pokemon_Id) > 1:
                            playerSelection = 1
                        elif event.key == pygame.K_3 and len(pokemon_Id) > 2: 
                            playerSelection = 2
                        elif event.key == pygame.K_4 and len(pokemon_Id) > 3:
                            playerSelection = 3

                        elif event.key == pygame.K_5 and len(pokemon_Id) > 4: 
                            playerSelection = 4
                        elif event.key == pygame.K_6 and len(pokemon_Id) > 5:
                            playerSelection = 5
                        else:
                            #wipe previous messages, then print new message
                            pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 65])
                            message_display('Invalid selection',screenWidth/2, screenHeight/2, 25)
                            playerSelection = 0
                            continue
                        #user has made their selection
                        keyDown = True
            slideEnemy = False
        #player pokemon has not yet been selected
        if(poke2 == None):
            poke2, pokename2 = _createPokemon_(pokemon_Id[playerSelection])
            pokename = str(pokename2)     
        #enter player pokemon (right to left)
        if slidePlayer:
            clock.tick(60)
            for x in range(screenWidth - 200):
                SCREEN.blit(flipImage(poke2), ((screenWidth - x) - 100,375))
                time.sleep(.003)
                pygame.draw.rect(SCREEN,white,[(screenWidth + 100) - x,375,screenWidth,200])
                pygame.display.update()
            #fill screen and draw new image at final position    
            SCREEN.fill(white)
            SCREEN.blit(flipImage(poke2), (screenWidth - x - 100 ,375))
            slidePlayer = False
            
        #draw the contestants final positions within the fight scene    
        SCREEN.blit(poke1, (x,100))
        SCREEN.blit(flipImage(poke2), (screenWidth - x - 100,375))
        
        #get enemy pokemon name
        enemyName = str(pb.pokemon(num))
        print(enemyName)
        #draw stat boxes, names
        message_display(enemyName, 150, 75, 25)
        message_display(pokename, screenWidth - 125, screenHeight - 145, 25)
        
        
        #attack game mechanics
        while(battleWinner(pokename, enemyName, poke1hp, poke2hp, enemy_damaged, player_damaged)):
            
            #reset damage taken
            damageTakenEnemy = 0
            damageTakenplayer = 0
            clock.tick(15)
            print(poke1hp)
            print(poke2hp)
            
            #healthbar full (enemy)
            pygame.draw.rect(SCREEN,green,(100,90,100,10))
            #indicate damage to enemy
            pygame.draw.rect(SCREEN,white,[100,90,enemy_damaged,10])
            #healthbar full (player)
            pygame.draw.rect(SCREEN,green,(3*screenWidth/4 - 25,3*screenHeight/4 - 10,100,10))
            #indicate damage to player
            pygame.draw.rect(SCREEN,white,[3*screenWidth/4 - 25,3*screenHeight/4 - 10,player_damaged,10])
            ###############
            #player
            if contestantTurn == 1:
                
                #check key event for end scene (debug)
                for event in pygame.event.get():
                    #check for keys pressed down
                    if event.type == pygame.KEYDOWN:
                        #exit scene (debug)
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        #player move
                        if event.key == pygame.K_1:
                            message_display(str(pokename) +' used '+str(pb.move(pokemon_Id[playerSelection])),screenWidth/2, screenHeight/2, 25)
                            time.sleep(1)
                            pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 100])
                            enemy_damaged += 10
                            damageTakenEnemy = 10
                            playerAttackSuccess += 1
                            contestantTurn = 2
                        #special ability    
                        if event.key == pygame.K_2:
                            if playerAttackSuccess == 3:
                                message_display(str(pb.ability(pokemon_Id[playerSelection])),screenWidth/2, screenHeight/2, 25)
                                time.sleep(1)
                                pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 100])
                                enemy_damaged += 20
                                damageTakenEnemy = 20
                                contestantTurn = 2
                                #reset attack success
                                playerAttackSuccess = 0
                            else:
                                message_display('cannot use special',screenWidth/2, screenHeight/2, 25)
                                time.sleep(1)
                                pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 100])
                                continue
                        #shake enemy player simulate an attack
                        shift = 0
                        for x in range(100):
                            clock.tick(30)
                            if shift == 0:
                                pygame.draw.rect(SCREEN,white,[screenWidth - 200,100,150,100])
                                SCREEN.blit(poke1, (screenWidth - 200 - 5,100))
                                time.sleep(.003)                       
                                shift = 5
                                pygame.display.update()
                            else:
                                pygame.draw.rect(SCREEN,white,[screenWidth - 200 + shift,100,150,100])
                                SCREEN.blit(poke1, (screenWidth - 200 + shift,100))
                                time.sleep(.003)                                
                                shift = 0
                                pygame.display.update()
                        
                        pygame.draw.rect(SCREEN,white,[screenWidth - 200 -5,100,120,100])
                        pygame.display.update()
                        SCREEN.blit(poke1, (screenWidth - 200,100))
                            
                    poke1hp -= damageTakenEnemy
                    
            
            #computer AI
            else:
                events()
                if enemyAttackSuccess == 3:
                    message_display(str(pb.ability(num)),screenWidth/2, screenHeight/2, 25)
                    time.sleep(1)
                    pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 100])
                    player_damaged += 20
                    damageTakenplayer = 20
                    contestantTurn = 1
                    enemyAttackSuccess = 0
                else:
                    message_display(str(pb.move(num)),screenWidth/2, screenHeight/2, 25)
                    time.sleep(1)
                    pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 100])
                    player_damaged += 10
                    damageTakenplayer = 10
                    contestantTurn = 1
                    enemyAttackSuccess += 1
                
                #shake enemy player simulate an attack
                shift = 0
                for x in range(100):
                    clock.tick(30)
                    if shift == 0:
                        pygame.draw.rect(SCREEN,white,[screenWidth - (screenWidth - 100) - 5,375,150,100])
                        SCREEN.blit(flipImage(poke2), (screenWidth - (screenWidth - 100) - 5,375))
                        time.sleep(.003)                       
                        shift = 5
                        pygame.display.update()
                    else:
                        pygame.draw.rect(SCREEN,white,[screenWidth - (screenWidth - 100) + shift,375,150,100])
                        SCREEN.blit(flipImage(poke2), (screenWidth - (screenWidth - 100) + shift,375))
                        time.sleep(.003)                                
                        shift = 0
                        pygame.display.update()
                        
                poke2hp -= damageTakenplayer        
                
                
                pygame.draw.rect(SCREEN,white,[screenWidth - (screenWidth - 100),375,150,100])
                pygame.display.update()
                SCREEN.blit(flipImage(poke2), (screenWidth - (screenWidth - 100),375))
                           
            #healthbar when hit
            pygame.display.update()

        #need healthbar, attack messaging, attack animations here, could write in while loop until a player dies or is captured
        pygame.display.update()
    ##################################################################################################################
    
def keyPresses():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("up")
            elif event.key == pygame.K_DOWN:
                print("up")
            elif event.key == pygame.K_LEFT:
                print("left")
            elif event.key == pygame.K_RIGHT:
                print("right")
            else:
                print('Nothing pressed')

def button(msg, x, y, w, h, ic, ac, action=None):

    click = pygame.mouse.get_pressed()
    #print(click)
    mouse = pygame.mouse.get_pos()

    #print(mouse)
    if (x + w) > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(SCREEN, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
            
    else:
        pygame.draw.rect(SCREEN, ic, (x, y, w, h))

    smallText = pygame.font.SysFont('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ( (x+(w/2)), (y+(h/2)) )
    SCREEN.blit(TextSurf, TextRect)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        SCREEN.fill(white)
        largeText = pygame.font.SysFont('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Pokemon", largeText)
        TextRect.center = (HALF_WIDTH, HALF_HEIGHT-200)
        SCREEN.blit(TextSurf, TextRect)

        button('Continue', screenWidth-100, 100, 100, 50, green, bright_green, game_loop)
        button('New Game', screenWidth-100, 150, 100, 50, green, bright_green, game_loop)
        button('QUIT', screenWidth-100, 200, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

#grass rgb = 36634e
#define the display surface
screenWidth = 640
screenHeight = 480

HALF_WIDTH = int(screenWidth/2)
HALF_HEIGHT = int(screenHeight/2)

AREA = screenWidth * screenHeight


#store pokemon ID's for api database access
pokemon_Id = [random.randrange(1, 152),random.randrange(1, 152),random.randrange(1, 152)]

######################################################################

#initialize the display
pygame.init()
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
background = pygame.image.load('BackgroundFinal.png')
pygame.display.set_caption("Pokemon CSC170")
FPS = 5
###################################################################################

#define some colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
bright_red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 200, 0)
bright_green = (0, 255, 0)
######################################################################

class Spritesheet:
    #telling the sprite sheet class the filename of the sprite sheet, the number of 
    #columns in the spritesheet, and the number of rows in the spritesheet
    def __init__(self, filename, columns, rows):
        self.sheet = pygame.image.load(filename)#.convert_alpha()

        self.columns = columns
        self.rows = rows
        self.totalCellCount = columns * rows
        #self.totalCellCount = 8 #this will ensure that only the first sprite in the sheet is used

        #returns the width and height of the sprite sheet
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / columns
        h = self.cellHeight = self.rect.height / rows
        hw, hh = self.cellCenter = (w/2, h/2)

        #building a list of cells that reference each cell in the sprite sheet
        #where the index references the individual sprite located in the sheet
        self.cells = list([(index % columns*w, index / columns*h, w, h) for index in range(self.totalCellCount)])        
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h)
        ])

    def draw(self, surface, cellIndex, x, y, handle=0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])

def quit_game():
    pygame.quit()
    quit()
#main loop
pause = False
def game_loop():
    global pause
    #spritesheet with the name of the file, the columns, and the rows
    s = Spritesheet("SpriteSheet2.png", 3, 4)

    #this will centralize the image over the x and y coordinates
    CENTER_HANDLE = 4

    playerVelocityX = 0
    playerVelocityY = 0

    playerx = 300
    playery = 300
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if playery > screenHeight - 160:
                playerVelocityY = -40
                index = 6
                playery += playerVelocityY
        elif keys[pygame.K_DOWN]:
            if playery < screenHeight - 80:
                playerVelocityY = 40
                index = 0
                playery += playerVelocityY
        elif keys[pygame.K_LEFT]:
            if 80 < playerx:
                playerVelocityX = -40
                index = 9
                playerx += playerVelocityX
        elif keys[pygame.K_RIGHT]:
            if screenWidth-80 > playerx:
                playerVelocityX = 40
                index = 3
                playerx += playerVelocityX
        elif keys[pygame.K_p]:
            pause = True
            paused()
        else:
            #print('No movement')
            playerVelocityX = 0
            playerVelocityY = 0
        #check for pokemon after buttons have or have not been pressed
        checkForPokemon()
        #blitting the background after all events have been accounted for, but
        #before the player is able to move around
        SCREEN.blit(background, (0, 0))
        #blit the sprite on the screen, increment the index value by 1 on each cycle of the main loop, the mod
        #operator will ensure that the index does not exceed the max index value in the sprite sheet and then blit 
        #the image on the center of the display surface
        #checkCoordinates(playerx, playery, playerVelocityX, playerVelocityY)
        s.draw(SCREEN, (index % s.totalCellCount), playerx, playery, CENTER_HANDLE)
        
        
        #move to the next index value
        #index += 1

        #pygame.draw.circle(screen, WHITE, (HALF_WIDTH, HALF_HEIGHT), 2, 0)
        pygame.display.update()
        clock.tick(FPS)
        SCREEN.fill(black)
game_intro()
game_loop()
