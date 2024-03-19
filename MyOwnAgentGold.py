from MyAgent import MyAgent
from MyAgentGold import MyAgentGold
from Board import Color
import pygame
from Board import Board

#inherits MyAgent

class MyOwnAgentGold(MyAgentGold):

    def __init__(self, id, initX, initY, env, backPack):
        super().__init__(id, initX, initY, env, backPack)
        self.color = Color.GOLD
        self.local_plan = []
        self.evaluating_from = self.posX, self.posY
        self.evaluating_with_load = 0
        self.evaluating_dist_so_far = 0
        self.roaming_around_directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.currendt_dir = 0
        self.font = Board.get_instance().agents_font
        pygame.init()
        
    def draw(self, screen, cell_size):
        pygame.draw.circle(screen, Color.WHITE, (self.posY * cell_size + cell_size//2, self.posX * cell_size + cell_size//2), cell_size//3+2)
        circ = pygame.draw.circle(screen, self.color, (self.posY * cell_size + cell_size//2, self.posX * cell_size + cell_size//2), cell_size//3)
        text = str(self.gold)
        text_surface = self.font.render(text, True, Color.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = circ.center
        screen.blit(text_surface, text_rect)
