#Brian Kilburn
#Nov 19, 2017
#Pokemon project prototype

import pygame
import pokebase as pb
import time
import random

#start pygame
pygame.init()

#set display width and height
display_width = 800
display_height = 600

#create characters
bulbasaur = pygame.image.load(pb.pokemon_sprite(1).path)
charmander = pygame.image.load(pb.pokemon_sprite(4).path)
charizard = pygame.image.load(pb.pokemon_sprite(6).path)

characters = []
#set variable to contain the game display and change the title caption
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pokemon")

#set the icon

#flip function
def flipImage(image):
    flipped = pygame.transform.flip(image, True, False)
    return flipped
#retrieve the background image
backgroundImg = pygame.image.load('DesertBackground.png')
#create the game loop       
def game_loop():
    
    while True:
        #check user activity
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        #draw image to the background
        gameDisplay.blit(backgroundImg, (0,0))
        gameDisplay.blit(bulbasaur, (display_width//2,display_height//2))
        gameDisplay.blit(flipImage(charizard), (display_width//2 - 100,display_height//2))
        gameDisplay.blit(charmander, (display_width//2 + 100,display_height//2))
        
        pygame.display.update()
game_loop()

    



