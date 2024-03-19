from MyAgentChest import MyAgentChest
from MyAgent import MyAgent
from Board import Board
from Board import Color
import pygame
import random

#inherits MyAgentChest

class MyOwnAgentChest(MyAgentChest) :
    
    def __init__(self, id, initX, initY, env):
        super().__init__(id, initX, initY, env)
        self.allocating = True
        self.planning = False
        self.executing = False
        self.local_plan = []
        self.color = Color.BLUE
        self.evaluating_from = self.posX, self.posY
        self.evaluating_dist_so_far = 0
        self.roaming_around_directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.currendt_dir = 0
        self.font = Board.get_instance().agents_font
        pygame.init()

    def draw(self, screen, cell_size):
        pygame.draw.circle(screen, Color.WHITE, (self.posY * cell_size + cell_size//2, self.posX * cell_size + cell_size//2), cell_size//3+2)
        circ = pygame.draw.circle(screen, self.color, (self.posY * cell_size + cell_size//2, self.posX * cell_size + cell_size//2), cell_size//3)

    def evaluate(self, resources):
        minEval = 0xffffffffff
        # default value that is garanteed to 
        # not be selected by the allocator
        bestChoice = ("", minEval)
        resources_keys = list(resources.keys())
        random.shuffle(resources_keys)
        for pos in resources_keys:
            x, y = pos.split(":")
            x, y = int(x), int(y)
            eval = MyAgent.distance(self.evaluating_from, to=(x, y))+1
            eval += self.evaluating_dist_so_far
            if eval < minEval:
                minEval = eval
                bestChoice = (str(x)+":"+str(y), eval)
        return bestChoice

    # Here we have a function describing
    # the way chest agents act and move around
    def act(self):
        currentX, currentY = self.getPos()
        if len(self.local_plan) == 0:
            self.roam_around((currentX, currentY))
            return
        if self.env.isAt(self, self.local_plan[0][0], self.local_plan[0][1]):
            self.env.open(self, self.local_plan[0][0], self.local_plan[0][1])
            self.local_plan.pop(0)
        else:
            goalX, goalY = self.local_plan[0][0], self.local_plan[0][1]
            nextX, nextY = currentX, currentY
            nextX += 1 if currentX < goalX else -1 if currentX > goalX else 0
            nextY += 1 if currentY < goalY else -1 if currentY > goalY else 0
            if self.move(currentX, currentY, nextX, nextY) < 0 and self.failure_count < 5:
                self.failure_count += 1
            else:
                self.failure_count = 0
                self.move_randomly((currentX, currentY))
