#Brian Kilburn
#Nov 19, 2017
#Pokemon project prototype

import pygame
import pokebase as pb
import time
import random

#start pygame
pygame.init()



 #pokemon generating method, returns pokemon image and name   
def _createPokemon_(dbValue):
    sprite = pygame.image.load(pb.pokemon_sprite(dbValue).path)
    return sprite, pb.pokemon(dbValue)


#set display width and height
display_width = 800
display_height = 600

#store pokemon ID's for api database access
pokemon_Id = [random.randrange(1, 152),random.randrange(1, 152),random.randrange(1, 152)]

#create characters generation 1 pokemon
poke1, pokename1 = _createPokemon_(pokemon_Id[0])
poke2, pokename2 = _createPokemon_(pokemon_Id[1])
poke3, pokename3 = _createPokemon_(pokemon_Id[2])
 
print("poke1:",pokename1)
print("poke2:",pokename2)
print("poke3:",pokename3)

#see ability print in console
str = pb.ability(1)
print(str)
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
        gameDisplay.blit(poke1, (display_width//2,display_height//2))
        gameDisplay.blit(flipImage(poke2), (display_width//2 - 100,display_height//2))
        gameDisplay.blit(poke3, (display_width//2 + 100,display_height//2))
        
        
        pygame.display.update()
game_loop()

    



