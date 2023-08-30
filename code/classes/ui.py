import pygame

class UI:
    def __init__(self, surface):
        self.displaySurface = surface

        #health
        self.healthUI = pygame.image.load('./graphics/ui/heart.png')

        #coins
        self.coin = pygame.image.load('./graphics/ui/coin.png')
        self.coinRect = self.coin.get_rect(topleft = (15, 61))
        self.font = pygame.font.Font('./graphics/ui/ARCADEPI.ttf', 30)

    def showHealth(self, current, full):
        for i in range(full):
            self.displaySurface.blit(self.healthUI, (i * 20 + 10, 10))

    def showCoins(self, amount):
        self.displaySurface.blit(self.coin, self.coinRect)
        coinAmountSurface = self.font.render(str(amount), False, 'WHITE')
        cointAmountRect = coinAmountSurface.get_rect(midleft = (self.coinRect.right + 5, self.coinRect.centery))
        self.displaySurface.blit(coinAmountSurface, cointAmountRect)