import pygame

import pokebase as pb

import random, math, sys, time

import pygame.gfxdraw

import multiprocessing
#exit the program

def events():

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()
            
#define colors            
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

fightThread = multiprocessing.Process
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
    time.sleep(2)
   ##################################################################################################################  
#fight scene function, for this to work there needs to be a user defined pokedex with id#, and random draw for enemies to battle
def fightScene():
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
    
    #create fighting loop
    while True:
        
        #enemy entrance left to right                
        if slideEnemy:
            #load and play beginning ecounter music
            pygame.mixer.music.load('BeginningofPokemonEncounter.wav')
            pygame.mixer.music.play(1)
            for x in range(screenWidth - 125):
                SCREEN.blit(poke1, (x,100))
                time.sleep(.003)
                pygame.draw.rect(SCREEN,white,[x-25,100,20,200])
                pygame.display.update()
            SCREEN.fill(white)
            SCREEN.blit(poke1, (x,100))
            #encounter loop music
            pygame.mixer.music.load('PokemonTrainerBattle.wav')
            pygame.mixer.music.play(-1)   
         
            #give user a chance to select their available pokemon
            while(not keyDown):
                #wipe any previous messages in center of screen
                pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 65])
                message_display('Select Your pokemon[1- '+str(len(pokemon_Id))+']',screenWidth/2, screenHeight/2, 25)
                for event in pygame.event.get():
                    #check for keys pressed down
                    if event.type == pygame.KEYDOWN:
                        #check for the number key pressed and if there are enough pokemon in the players pokedex
                        if event.key == pygame.K_LEFT:
                            return
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
        
        #draw stat boxes, names
        message_display(str(pokename1), 150, 75, 25)
        message_display(pokename, screenWidth - 125, screenHeight - 145, 25)
        
        
        #attack game mechanics
        while(poke1hp >= 0 and poke2hp >= 0):
            #reset damage taken
            damageTakenEnemy = 0
            damageTakenplayer = 0
          
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
                        if event.key == pygame.K_LEFT:
                            pygame.mixer.music.stop()                            
                            return
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
                        for x in range(screenWidth - 200):
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
                
                if enemyAttackSuccess == 3:
                    message_display(str(pb.ability(pokemon_Id[0])),screenWidth/2, screenHeight/2, 25)
                    time.sleep(1)
                    pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 100])
                    player_damaged += 20
                    damageTakenplayer = 20
                    contestantTurn = 1
                    enemyAttackSuccess = 0
                else:
                    message_display(str(pb.move(pokemon_Id[0])),screenWidth/2, screenHeight/2, 25)
                    time.sleep(1)
                    pygame.draw.rect(SCREEN,white,[0, screenHeight/2-50,screenWidth, 100])
                    player_damaged += 10
                    damageTakenplayer = 10
                    contestantTurn = 1
                    enemyAttackSuccess += 1
                
                #shake enemy player simulate an attack
                shift = 0
                for x in range(screenWidth - 200):
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
            
        #check key event for end scene (debug)
        for event in pygame.event.get():
            #check for keys pressed down
            if event.type == pygame.KEYDOWN:
                #exit scene (debug)
                if event.key == pygame.K_LEFT:
                    pygame.mixer.music.stop()                            
                    return
        #need healthbar, attack messaging, attack animations here, could write in while loop until a player dies or is captured
        pygame.display.update()
    ##################################################################################################################   
        
      
#defining the display surface

screenWidth = 640#800 #640

screenHeight = 480#600 #480

######################

halfScreenWidth = screenWidth/2

halfScreenHeight = screenHeight/2

#################################

SCREEN_AREA = screenWidth * screenHeight

########################################


################character creation ############
#store pokemon ID's for api database access
pokemon_Id = [random.randrange(1, 152),random.randrange(1, 152),random.randrange(1, 152)]

#create characters generation 1 pokemon
poke1, pokename1 = _createPokemon_(pokemon_Id[0])
#poke2, pokename2 = _createPokemon_(pokemon_Id[1])
#poke3, pokename3 = _createPokemon_(pokemon_Id[2])
 
print("poke1:",pokename1)
#print("poke2:",pokename2)
#print("poke3:",pokename3)

#initialize the display

pygame.init()

CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((screenWidth,screenHeight))

FPS = 500



#Defining a list of colors in case they are needed

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

RED = (255, 0, 0)

BLUE = (0, 0, 255)

GREEN = (0, 255, 0)

#########################

def game_loop():

    #setting the background image and use convert because the pixels of the image may not be the 

    #same as the background. Convert saves time

    pokemonRoute = pygame.image.load('GreatMarsh.png').convert()

    #finding out what the background width and background height are of the pokemon route

    backgroundWidth, backgroundHeight = pokemonRoute.get_rect().size

    #setting the width of the route will stop the player from being able to exit the bounds of the 

    #pokemon route and will stop the background from scrolling out of bounds of the display surface

    routeWidth = backgroundWidth #* 2
    
    routePositionX = 0



    scrollingRoutePositionX = halfScreenWidth



    #this is a circle for now, but can be changed to the player later on

    circleRadius = 25

    circlePositionX = circleRadius



    #difining the player positions

    playerPositionX = circleRadius

    playerPositionY = 345

    #tells the stage what direction to move

    playerVelocityX = 0
    playerVelocityY = 0




    #setting the game loop done variable to false initially

    done = False

    #main loop

    while not done:

        #calling the events function to see if the user has left the game

        events()



        #finding out what keys have been pressed

        KEY_PRESSED = pygame.key.get_pressed()

        #if the user presses the right key, then move in the positive x direction

        if KEY_PRESSED[pygame.K_RIGHT]:

            playerVelocityX = 1
            fightScene()           
        #if the user presses the left key, then move in the negative x direction

        elif KEY_PRESSED[pygame.K_LEFT]:

            playerVelocityX = -1
        
        #if the user presses the up key, then move subtract y position
        elif KEY_PRESSED[pygame.K_UP]:
            
            playerVelocityY = -1
        
        #if the user presses the down key, then move add y position
        elif KEY_PRESSED[pygame.K_DOWN]:
            
            playerVelocityY = 1
        #if no key is pressed, then do not move and remain in the same position

        else:

            playerVelocityX = 0
            playerVelocityY = 0

        playerPositionY += playerVelocityY
        playerPositionX += playerVelocityX

        #if the playerposition in the x direction is greater than the width

        #of the route minus the circle radius, then push the player to the 

        #righthand edge of the screen

        if playerPositionX > routeWidth - circleRadius:

            playerPositionX = routeWidth - circleRadius
        
        elif playerPositionY > screenHeight + 5:
            playerPositionY =  screenHeight + 5
        
        elif playerPositionY < 50:
            playerPositionY = 50
        #if the playerposition in the x direction is less than the radius

        #of the cirle, then push the player to the lefthand corner of the screen

        elif playerPositionX < circleRadius:

            playerPositionX = circleRadius

        #if the player position in the x direction is less than the scrollingrouteposition

        #then the ball will be located in the center and move with the screen

        elif playerPositionX < scrollingRoutePositionX:

            circlePositionX = playerPositionX
            

        #if the playerposition is greater than the routewidth minus

        #the scrolling route position in the x direction, then the ball will

        #not be in the center, and it will be located at route width minus

        #the scrolling route position plus the width of the screen

        elif playerPositionX > routeWidth - scrollingRoutePositionX:

            circlePositionX = playerPositionX - routeWidth + screenWidth

        #else the circle is in the middle of the screen

        else:

            circlePositionX = scrollingRoutePositionX

            routePositionX += -playerVelocityX



        relativePositionX = routePositionX % backgroundWidth

        #print("Route Position" + str(routePositionX))

        #print("Background Width" + str(backgroundWidth))

        #print("Relative Position" + str(relativePositionX))

        SCREEN.blit(pokemonRoute, (relativePositionX - backgroundWidth, 0))
       
        if relativePositionX < screenWidth:

            SCREEN.blit(pokemonRoute, (relativePositionX, 0))
            
            
        #blit characters
        #SCREEN.blit(poke1, (screenWidth//2 + 20,screenHeight//2 + 20))
        #SCREEN.blit(flipImage(poke2), (screenWidth//2 - 100,15))
        #SCREEN.blit(poke3, (backgroundWidth//4 + 185,70))
        pygame.draw.circle(SCREEN, WHITE, (playerPositionX, playerPositionY - circleRadius), circleRadius, 0)



        pygame.display.update()

        CLOCK.tick(FPS)

        SCREEN.fill(BLACK)
    
game_loop()

