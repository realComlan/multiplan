from MyAgent import MyAgent

import pygame

#inherits MyAgent

class MyAgentGold(MyAgent):

    def __init__(self, id, initX, initY, env, capacity):
        MyAgent.__init__(self, id, initX, initY, env)
        self.gold = 0 # the quantity of gold collected and not unloaded yet
        self.backPack = capacity #capacity of the agent's back pack

    #return quantity of gold collected and not unloaded yet
    def getTreasure(self):
        return self.gold

    #unload gold in the pack back at the current position
    def unload(self):
        self.env.unload(self)
        self.gold = 0

    #return the agent's type
    def getType(self):
        return 0

    # add some gold to the backpack of the agent (quantity t)
    # if the quantity exceeds the back pack capacity, the remaining is lost
    def addTreasure (self, t):
        if (self.gold+t <= self.backPack) :
            self.gold = self.gold + t
        else :
            self.gold = self.backPack

    #load the treasure at the current position
    def load(self,env):
        env.load(self)

    def __str__(self):
        res = "agent Gold "+  self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res
