import pygame
from settings import *

class UI:
    def __init__(self, surface):
        self.displaySurface = surface

        #health
        self.healthUI = pygame.image.load('./graphics/ui/heart.png').convert_alpha()

        #coins
        self.coin = pygame.image.load('./graphics/ui/coin.png').convert_alpha()
        self.coinRect = self.coin.get_rect(topleft = (15, 45))
        self.font = pygame.font.Font('./graphics/ui/ARCADEPI.ttf', 15)

        #GameOver
        self.font2 = pygame.font.Font('./graphics/ui/ARCADEPI.ttf', 40)
        self.font_gameOver = pygame.font.Font('./graphics/ui/ARCADEPI.ttf', 20)

        #Dash Ability
        self.dashImage = pygame.image.load('./graphics/ui/speedGraphic.png').convert_alpha()
        self.dashRect = self.coin.get_rect(center = (screenWidth // 2 - 100, screenHeight // 2 - 125))
        self.doubleImage = pygame.image.load('./graphics/ui/jumpBoost.png').convert_alpha()
        self.doubleRect = self.coin.get_rect(center = (screenWidth // 2 - 100, screenHeight // 2 - 125))
        self.fontEnter = pygame.font.Font('./graphics/ui/ARCADEPI.ttf', 10)

    def showHealth(self, current, full):
        for i in range(current):
            self.displaySurface.blit(self.healthUI, (i * 20 * 1.2 + 10, 10))

    def showCoins(self, amount): #Display coin counter UI
        self.displaySurface.blit(self.coin, self.coinRect) #Display coin sprite
        coinAmountSurface = self.font.render(str(amount), False, 'WHITE') #Displays total coins collected (integer number), from level class
        cointAmountRect = coinAmountSurface.get_rect(midleft = (self.coinRect.right + 5, self.coinRect.centery))
        self.displaySurface.blit(coinAmountSurface, cointAmountRect)
    
    def showGameOver(self):
        gameOverSurface = self.font2.render("GAME OVER", False, 'RED') #Foreground Font
        gameOverBg = self.font2.render("GAME OVER", False, "#009468") #Background Font
        gameOverRect = gameOverSurface.get_rect(center = (screenWidth // 2, screenHeight // 2)) #Foreground rect
        gameOver_Bg_Rect = gameOverSurface.get_rect(topleft = (gameOverRect.x + 2, gameOverRect.y + 2)) #Background shifted by 2 pixels in x and y direction
        self.displaySurface.blit(gameOverBg, gameOver_Bg_Rect )
        self.displaySurface.blit(gameOverSurface, gameOverRect)

        gameOverText = self.font_gameOver.render("Press ENTER to restart from Level One", False, "WHITE") #Restart text in bottom
        gameOverTextRect = gameOverText.get_rect(center = (screenWidth // 2, screenHeight // 2 + 50)) #Slightly below game over text
        self.displaySurface.blit(gameOverText, gameOverTextRect) 

    def unlockdashAbility(self):
        self.displaySurface.blit(self.dashImage, self.dashRect)
        unlockSurface = self.font2.render("DASH ABILITY UNLOCKED", False, 'GREEN') #Foreground Font
        unlockBg = self.font2.render("DASH ABILITY UNLOCKED", False, "#009468") #Background Font
        unlockRect = unlockSurface.get_rect(center = (screenWidth // 2, screenHeight // 2 + 100)) #Foreground rect
        unlockBg_Rect = unlockSurface.get_rect(topleft = (unlockRect.x + 2, unlockRect.y + 2)) #Background shifted by 2 pixels in x and y direction
        self.displaySurface.blit(unlockBg, unlockBg_Rect)
        self.displaySurface.blit(unlockSurface, unlockRect)

        unlockText = self.font_gameOver.render("Press C to dash forwards", False, "WHITE") #Restart text in bottom
        unlockTextRect = unlockText.get_rect(center = (screenWidth // 2, screenHeight // 2 + 150)) #Slightly below game over text
        self.displaySurface.blit(unlockText, unlockTextRect) 

        enterText = self.fontEnter.render("Press enter to return to main menu", False, "WHITE") #Enter text in bottomQ
        enterRect = enterText.get_rect(center = (screenWidth//2, screenHeight //2 + 170)) #Slightly below unlock text
        self.displaySurface.blit(enterText, enterRect) 

    def unlockDoubleAbility(self):
        self.displaySurface.blit(self.doubleImage, self.doubleRect)
        unlockSurface = self.font2.render("DOUBLE JUMP ABILITY UNLOCKED", False, 'GREEN') #Foreground Font
        unlockBg = self.font2.render("DOUBLE JUMP ABILITY UNLOCKED", False, "#009468") #Background Font
        unlockRect = unlockSurface.get_rect(center = (screenWidth // 2, screenHeight // 2 + 100)) #Foreground rect
        unlockBg_Rect = unlockSurface.get_rect(topleft = (unlockRect.x + 2, unlockRect.y + 2)) #Background shifted by 2 pixels in x and y direction
        self.displaySurface.blit(unlockBg, unlockBg_Rect)
        self.displaySurface.blit(unlockSurface, unlockRect)

        unlockText = self.font_gameOver.render("Press Z in mid air to jump a 2nd time!", False, "WHITE") #Restart text in bottom
        unlockTextRect = unlockText.get_rect(center = (screenWidth // 2, screenHeight // 2 + 150)) #Slightly below game over text
        self.displaySurface.blit(unlockText, unlockTextRect) 

        enterText = self.fontEnter.render("Press enter to return to main menu", False, "WHITE") #Enter text in bottomQ
        enterRect = enterText.get_rect(center = (screenWidth//2, screenHeight //2 + 170)) #Slightly below unlock text
        self.displaySurface.blit(enterText, enterRect) 
    
    def drawBlackOverlay(self): #Draws black overlay that is translucent in front of game, but behind UI elements
        overlay = pygame.Surface((screenWidth, screenHeight))
        overlay.fill("BLACK")
        overlay.set_alpha(160) #Semi transparent alpha value
        self.displaySurface.blit(overlay, (0,0))