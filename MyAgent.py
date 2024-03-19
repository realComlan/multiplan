
import Environment as Environment
from Board import Color
import pygame
import random

class MyAgent:

    def __init__(self, id, initX, initY, env:Environment):
        self.id = id
        self.posX = initX
        self.posY = initY
        self.env = env
        self.mailBox = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.getId() == self.getId()
        return False

    #make the agent moves from (x1,y1) to (x2,y2)
    def move(self, x1, y1, x2, y2) :
        if x1 == self.posX and y1 == self.posY :
            print("departure position OK")
            if self.env.move(self, x1, y1, x2, y2) :
                self.posX = x2
                self.posY = y2
                print("deplacement OK")
                return 1
        return -1

    #return the id of the agent
    def getId(self):
        return self.id

    #return the position of the agent
    def getPos(self):
        return (self.posX, self.posY)

    # add a message to the agent's mailbox
    def receive(self, idReceiver, textContent):
        self.mailBox.append((idReceiver, textContent))

    #the agent reads a message in her mailbox (FIFO mailbox)
    #return a tuple (id of the sender, message  text content)
    def readMail (self):
        idSender, textContent = self.mailBox.pop(0)
        print("mail received from {} with content {}".format(idSender,textContent))
        return (idSender, textContent)

    #send a message to the agent whose id is idReceiver
    # the content of the message is some text
    def send(self, idReceiver, textContent):
        self.env.send(self.id, idReceiver, textContent)

    def __str__(self):
        res = self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res
    

    # Added functions
    #

    def distance(fr, to):
        return max(abs(fr[0] - to[0]), abs(fr[1] - to[1]))+1
        #return max((fr[0] - to[0])**2, (fr[1] - to[1])**2)+1

    def has_mail(self):
        return len(self.mailBox) > 0

    # This evaluation method is used by the 
    # ramasseurs only. The chest openers 
    # have defined their own evaluation 
    # method in MyOwnAgentChest
    def evaluate(self, resources):
        minEval = 0xfffffffffffff
        # default value that is garanteed to 
        # not be selected by the allocator
        bestChoice = ("", minEval)
        #backPack_is_full = True
        only_big_chests_left = True
        resources_keys = list(resources.keys())
        #random.shuffle(resources_keys) 
        for pos in resources_keys:
            x, y = pos.split(":")
            x, y = int(x), int(y)
            value = resources[pos]
            eval = MyAgent.distance(self.evaluating_from, to=(x, y))
            eval += self.evaluating_dist_so_far
            new_load = self.evaluating_with_load + value
            if new_load <= self.backPack:
                #backPack_is_full = False
                only_big_chests_left = False
                if eval < minEval:
                    minEval = eval
                    bestChoice = (str(x)+":"+str(y), eval)
        # not only_big_chests_left
        if not only_big_chests_left:
            #print("not only big", resources[pos])
            return bestChoice
        # only_big_chests_left and self.evaluating_with_load == 0
        elif self.evaluating_with_load == 0:
            # if there are only big chests left we take 
            # one that we can fill maximally.
            # so we must be empty handed first
            # then the planmanager will select 
            # the one with the biggest packpack
            for pos, tres in resources.items():
                x, y = pos.split(":")
                x, y = int(x), int(y)
                # pas besoin de les comparer
                # ils sont tous trop grands pour moi
                # on revoit donc simplement le premier
                #print("big chest chosen", str(x)+":"+str(y), "with my backpack", self.backPack)
                bestChoice = (str(x)+":"+str(y), 0xfffffffffffff-self.backPack)
                return bestChoice
        # only_big_chests_left and self.evaluating_with_load != 0
        else: 
            depotX, depotY = self.env.posUnload[0], self.env.posUnload[1]
            self.local_plan.append((depotX, depotY))
            self.local_plan.append("unload")
            self.evaluating_with_load = 0
            self.evaluating_dist_so_far += MyAgent.distance(self.evaluating_from, (depotX, depotY))
            self.evaluating_from = depotX, depotY
            # the agent realized she has to unload her bag first
            # and then reavaluate her best choice only after that
            return self.evaluate(resources)
    
    def act(self):
        currentX, currentY = self.getPos()
        if hasattr(self, "gold"):
            in_bag = self.gold
        else:
            in_bag = self.stone
        # if the agent is a the end of her plan 
        # she has to unload her load to the depot...
        if len(self.local_plan) == 0 and in_bag > 0:
            depotX, depotY = self.env.posUnload[0], self.env.posUnload[1]
            self.local_plan.append((depotX, depotY))
            self.local_plan.append("unload")
            return True
        # et apres que cela a ete fait
        # elle va se balader aux abords du terrain
        # pour reduire le bruit ajoute aux mouvements
        # des autres agents
        elif len(self.local_plan) == 0: 
            self.roam_around((currentX, currentY))
            return False

        # when the agent has arrived at his current goal...
        if self.env.isAt(self, self.local_plan[0][0], self.local_plan[0][1]):
            # if the current location is a depot zone we unload
            if len(self.local_plan) > 1 and self.local_plan[1] == "unload":
                self.env.unload(self)
                if hasattr(self, "gold"):
                    self.gold = 0
                else:
                    self.stone = 0
                self.local_plan.pop(0)
                self.local_plan.pop(0)
            # either, it is a load goad and the in this case
            # the agent simply loads the chest at the current
            # location
            else:
                avoirs_before_load = in_bag
                if self.env.grilleTres[currentX][currentY].open: # load successful
                    self.env.load(self)
                    self.local_plan.pop(0)
                else:
                    goalX, goalY = self.local_plan[0][0], self.local_plan[0][1]
                    self.move_randomly((currentX, currentY))
        # if the agent has still not arrived at its next goal
        # it keeps moving in the direction of the goal
        else:
            currentX, currentY = self.getPos()
            goalX, goalY = self.local_plan[0]
            nextX, nextY = currentX, currentY
            nextX += 1 if currentX < goalX else -1 if currentX > goalX else 0
            nextY += 1 if currentY < goalY else -1 if currentY > goalY else 0
            # if the move attempt fail, it means that another agent is 
            # in the way. The solution is to make a random move away
            # and then get back to the plan at the next timestep
            if self.move(currentX, currentY, nextX, nextY) < 0:
                self.move_randomly((currentX, currentY))
        return True

    # Cette methode est utilisee pour sortir d'une situation 
    # d'echec (de mouvement ou d'ouverture de coffre)
    # en faisant un mouvement aleatoire puis essayer encore
    # 
    def move_randomly(self, currentPos):
        currentX, currentY = currentPos
        iii = [-1, 1, 0] 
        jjj = [-1, 1, 0]
        random.shuffle(iii)
        random.shuffle(jjj)
        for i in iii:
            for j in jjj:
                # pour que l'immobilite soit seulement
                # le dernier recours possible
                if i == 0 and j == 0: continue
                nextX = currentX + i
                nextY = currentY + j
                if self.move(currentX, currentY, nextX, nextY) > 0:
                    break
    
    # Cette methode est utilisee pour faire mouvoir les 
    # agents ayant fini l'execution de leurs plans
    # locaux, sur les bords de la grille pour limiter 
    # au maximum qu'ils perturbent le mouvement des 
    # autres agents
    def roam_around(self, currentPos):
        currentX, currentY = currentPos
        nextX = currentX + self.roaming_around_directions[self.currendt_dir][0]
        nextY = currentY + self.roaming_around_directions[self.currendt_dir][1]
        if self.move(currentX, currentY, nextX, nextY) < 0:
            self.currendt_dir += 1
            self.currendt_dir %= 4

    def receive_offer(self):
        if self.has_mail():
            message = self.readMail()
            x, y, value = message[1].split(":")
            x, y = int(x), int(y)
            self.evaluating_dist_so_far += MyAgent.distance(self.evaluating_from, (x, y))
            self.evaluating_from = x, y
            self.failure_count = 0
            self.local_plan.append((x, y))
            
            if self.getType() < 2: # for ramasseurs agents only
                self.evaluating_with_load += int(value)