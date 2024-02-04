import pygame
from settings import *
from functions.button import Button
class Start():
    def __init__(self, currentLevel, surface, createOverworld):
        self.displaySurface = surface
        self.createOverworld = createOverworld
        self.currentLevel = currentLevel
        self.quit = False
        #Import assets for start menu
        self.background = pygame.image.load('./graphics/ui/menu.png').convert_alpha()
        self.JungleText = pygame.image.load('./graphics/ui/JungleText.png').convert_alpha()
        self.JungleTextRect = self.JungleText.get_rect(center = (screenWidth // 2, screenHeight // 2 - 50))
        #Import Buttons
        self.startImg = pygame.image.load("./graphics/ui/Start.png").convert_alpha()
        self.optionsImg = pygame.image.load("./graphics/ui/Options.png").convert_alpha()
        self.quitImg = pygame.image.load("./graphics/ui/Quit.png").convert_alpha() 
        #Create button class
        self.startButton = Button(200, 380, self.startImg, 1)
        self.optionsButton = Button(400, 380, self.optionsImg, 1)
        self.quitButton = Button(600, 380, self.quitImg, 1)

    def drawButton(self):
        if self.startButton.draw(self.displaySurface):
            self.createOverworld(self.currentLevel, 0) #Create overworld if start pressed
        if self.optionsButton.draw(self.displaySurface):
            print("Options") #Placeholder
        if self.quitButton.draw(self.displaySurface):
            print("Quit")
            self.quit = True #Set quit attribute to true 
    
    def getQuit(self):
        return self.quit
    
    def run(self):
        self.displaySurface.blit(self.background, (0,0))
        self.displaySurface.blit(self.JungleText, self.JungleTextRect)
        self.drawButton()