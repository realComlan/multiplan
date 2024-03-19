
import Treasure, MyAgent, MyAgentChest

class Environment:

    def __init__(self, tailleX, tailleY, posUnload):
        self.tailleX = tailleX
        self.tailleY = tailleY
        self.grilleTres = [[None for j in range(tailleY)] for j in range(tailleX)] # locations of Treasures
        self.grilleAgent = [[None for j in range(tailleY)] for j in range(tailleX)] # locations of agents
        self.posUnload = posUnload # a couple of positions x and y, where the agents can unload tresor
        self.score = 0 # quantity of treasure unload at the right place (posUnload)
        self.agentSet = dict() # the set of agents acting in the environment


    # add an agent to the environment
    def addAgent(self, agent:MyAgent):
        posX, posY = agent.getPos()
        self.grilleAgent[posX][posY] = agent

    #add a treasure to the environment
    def addTreasure(self, tresor : Treasure, x, y):
        self.grilleTres[x][y] =  tresor

    # add an agent to the set of agents
    def addAgentSet(self, dictAgent):
        self.agentSet = dictAgent

    # check whether the agent is at position (x,y)
    def isAt(self, agent:MyAgent, x, y):
        return self.grilleAgent[x][y] == agent

    # make the agent moves from (x1, y1) to (x2, y2)
    def move(self, agent:MyAgent, x1, y1, x2, y2):
        if x2 <0 or y2 < 0 or x2 >= self.tailleX or y2 >= self.tailleY or ( x2 != x1 -1 and  x2 != x1+1 and x2 != x1) \
                or ( y2!= y1 -1 and  y2 != y1+1 and y2!=y1) : # invalid move
            print("invalid move")
            return False
        if ( not self.isAt(agent, x1, y1)) or self.grilleAgent[x2][y2] != None  : # position already occupied
            print("position not free")
            return False
        else :
            self.grilleAgent[x2][y2] = agent
            self.grilleAgent[x1][y1] = None
            return True

    # return the quanity of treasure unloaded at the collector place
    def getScore(self):
        return self.score

    # make an agent unload her bakcpack
    def unload(self, agent:MyAgent):

        if self.isAt(agent, self.posUnload[0], self.posUnload[1]) :
            self.score = self.score + agent.getTreasure()
            print("unload tres : {}".format(agent.getTreasure()))

    # make a Chest Agent open the chest
    def open(self, agent:MyAgentChest, x, y):
        if(self.grilleAgent[x][y] == agent and self.grilleTres[x][y] != None) :
            self.grilleTres[x][y].openChest()
            print("chest open !")

    # make an agent load some treasure
    def load(self, agent ):
        x , y = agent.getPos()
        if(self.grilleTres[x][y] != None  and self.grilleTres[x][y].getType() == agent.getType() ) :
            print("load OK")
            agent.addTreasure(self.grilleTres[x][y].getValue())
            self.grilleTres[x][y].resetValue()
        else :
            print("load fail")

    #make an agent send a message
    def send(self,idSender, idReceiver, textContent):
        self.agentSet[idReceiver].receive(idSender, textContent)

    def __str__(self):
        str = ""
        for i in range(0, self.tailleX) :
            str = str + "\n"
            for j in range(0, self.tailleY) :
                b = True
                if(self.grilleTres[i][j] != None) :
                    b = False
                    if(self.grilleTres[i][j].getType() == 1):
                        str = str + " G "
                    else :
                        str = str + " S "
                if(self.grilleAgent[i][j] != None) :
                    str = str + " A "
                    b = False
                if b :
                    str = str + " - "
                str = str + "|"
        return str