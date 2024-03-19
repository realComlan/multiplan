import pygame
from Board import Board
from Board import Color

class Treasure:

    def __init__(self, type, x, y, value):
        self.type = type # 0 for gold, 1 for precious stones
        self.open = False
        self.posX = x
        self.posY = y
        self.value = value
        self.color = Color.GOLD if self.type == 0 else Color.STONE
        self.font = Board.get_instance().treasures_font
        pygame.init()

    # return True if the chest is open, False otherwise
    def isOpen(self):
        return self.open

    #open the Chest
    def openChest(self) :
        print("ouverture du coffre")
        self.open = True
        self.color = Color.LIGHT_RED if self.getType() == 1 else Color.LIGHT_YELLOW

    #return the type of treasure in the Chest
    def getType(self):
        return self.type

    # return the quantity of treasure
    def getValue(self):
        return self.value

    #set the quantity of treasure to 0
    def resetValue(self):
        self.value = 0

    def draw(self, screen, cell_size):
        text = str(self.value)
        text_surface = self.font.render(text, True, Color.GREEN if self.open else Color.BLACK if self.type == 0 else Color.WHITE)
        text_rect = text_surface.get_rect()
        rect = pygame.draw.rect(screen, self.color, (self.posY * cell_size, self.posX * cell_size, cell_size, cell_size))
        text_rect.center = rect.center
        screen.blit(text_surface, text_rect)
