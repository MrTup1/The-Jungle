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

    def showHealth(self, current, full):
        for i in range(current):
            self.displaySurface.blit(self.healthUI, (i * 20 * 1.2 + 10, 10))

    def showCoins(self, amount):
        self.displaySurface.blit(self.coin, self.coinRect)
        coinAmountSurface = self.font.render(str(amount), False, 'WHITE')
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
    
    def drawBlackOverlay(self):
        overlay = pygame.Surface((screenWidth, screenHeight))
        overlay.fill("BLACK")
        overlay.set_alpha(160)
        self.displaySurface.blit(overlay, (0,0))