
from Environment import Environment
from MyOwnAgentGold import  MyOwnAgentGold
from MyOwnAgentChest import MyOwnAgentChest
from MyOwnAgentStones import MyOwnAgentStones
from Board import Board
from Treasure import Treasure
from environments.env_generator import Generator
import random
import gc

class PlanManager:

    instance = None

    def __init__(self, env_file=None):
        self.env_file = env_file
        if not env_file: 
            self.env_file = Generator.generate_environment_description()
        env, agents = self.load_file_config(self.env_file)
        self.env = env
        self.agents = agents
        self.tasks_allocation()

    def go(self):
        Board.get_instance().go()

    def get_instance(env_file=None):
        if not PlanManager.instance:
            PlanManager.instance = PlanManager(env_file)
        return PlanManager.instance

    # For the "NEW" button
    def get_new_instance(env_file=None):
        PlanManager.instance = None
        gc.collect()
        # Now we build a new instance
        PlanManager.get_instance()
        Board.get_instance().update_scene_params()
        return PlanManager.instance 

    # For the "RESTART" button
    def rewind(self):
        env, agents = self.load_file_config(self.env_file)
        self.env = env
        self.agents = agents
        self.tasks_allocation()

    def tasks_allocation(self):
        # Let the manager organize the auctions
        # For chest openers
        ChestOpenersAuction(self.env).go()
        # For the gold chest collectors
        RamasseursAuction(self.env, agent_type=0).go()
        # For the stones chests collectors
        RamasseursAuction(self.env, agent_type=1).go()

    def load_file_config(self, env_file) :
    
        file = open(env_file)
        lines = file.readlines()
        tailleEnv = lines[1].split()
        tailleX = int(tailleEnv[0])
        tailleY = int(tailleEnv[1])
        zoneDepot = lines[3].split()
        self.treasures = []
        cPosDepot =  (int(zoneDepot[0]), int(zoneDepot[1]))
        dictAgent = dict()
    
        env = Environment(tailleX, tailleY, cPosDepot)
    
        cpt = 0
    
        for ligne in lines[4:] :
            ligneSplit = ligne.split(":")
            # Adding a new treasure
            if(ligneSplit[0]=="tres"):
                x, y = int(ligneSplit[2]), int(ligneSplit[3])
                load = int(ligneSplit[4])
                if(ligneSplit[1]=="or"):
                    tres = Treasure(0, x, y, load)
                    env.addTreasure(tres, x, y)
                    self.treasures.append(tres)
                elif(ligneSplit[1]=="pierres"):
                    tres = Treasure(1, x, y, load)
                    env.addTreasure(tres, x, y)
                    self.treasures.append(tres)
            # Adding a new agent
            elif(ligneSplit[0]=="AG") :
                x, y = int(ligneSplit[2]), int(ligneSplit[3])
                if(ligneSplit[1]=="or"):
                    idNum = "agent" + str(cpt)
                    capacity = int(ligneSplit[4])
                    agent = MyOwnAgentGold(idNum, x, y, env, capacity)
                    dictAgent[idNum] = agent
                    env.addAgent(agent)
                    cpt = cpt+1
                elif(ligneSplit[1]=="pierres"):
                    idNum = "agent" + str(cpt)
                    capacity = int(ligneSplit[4])
                    agent = MyOwnAgentStones(idNum, x, y, env, capacity)
                    dictAgent[idNum] = agent
                    env.addAgent(agent)
                    cpt = cpt+1
                elif (ligneSplit[1] == "ouvr"):
                    idNum = "agent" + str(cpt)
                    agent = MyOwnAgentChest(idNum, x, y, env)
                    dictAgent[idNum] = agent
                    env.addAgent(agent)
                    cpt = cpt+1
        file.close()
        env.addAgentSet(dictAgent)
        return (env, dictAgent)
    
class Auction:

    def __init__(self, env):
        self.env = env
        self.participants = dict()
        self.resources = dict()
        self.evaluations = dict()

    def go(self):
        self.gather_people()
        self.gather_resources()
        self.allocate()

    def allocate(self):
        while len(self.resources) > 0:
            for agent in self.participants.values():
                # each agent sends only the resource that it ranked 
                # best for them
                self.evaluations[agent.getId()] = agent.evaluate(self.resources)
            minEval = 0xfffffffffffff
            minAgent = None
            minRes = None
            # we shuffle the keys in order to avoid getting 
            # cases of discrimination
            shuffled_keys = list(self.evaluations.keys())
            random.shuffle(shuffled_keys)
            for agentId in shuffled_keys:
                evaluation = self.evaluations[agentId]
                eval = evaluation[1] 
                if eval < minEval:
                    minRes = evaluation[0]
                    minEval = eval
                    minAgent = agentId
            if minRes in self.resources:
                value = str(self.resources[minRes])
                self.env.send("allocator", minAgent, minRes+":"+value)
                self.participants[minAgent].receive_offer()
                self.resources.pop(minRes)
            else:
                print("non good res ", minRes, "val ", minEval, "by agent ", minAgent)
        
class ChestOpenersAuction(Auction):

    def gather_people(self):
        for agent in self.env.agentSet.values():
            if agent.getType() == 2:
                self.participants[agent.id] = agent

    def gather_resources(self):
        from itertools import product
        for x, y in product(range(self.env.tailleX), range(self.env.tailleY)):
            # agent type 0 (gold)   take treasure type 1 (gold chests)
            # agent type 1 (stones) take treasure type 2 (stones chests)
            tres = self.env.grilleTres[x][y]
            if tres:
                self.resources[str(x)+":"+str(y)] = tres.getValue()

class RamasseursAuction(Auction):

    def __init__(self, env, agent_type):
        super().__init__(env)
        self.agent_type = agent_type # 0 for gold, 1 for stones

    # Here we gather the collectors that will participate in
    # each auction, one auction for gold chests and another one for 
    # stones chests
    def gather_people(self):
        for agent in self.env.agentSet.values():
            if agent.getType() == self.agent_type:
                self.participants[agent.id] = agent

    # Here we collect a list of the treasure chests corresponding
    # to the current agent type that we are considering
    def gather_resources(self):
        from itertools import product
        for x, y in product(range(self.env.tailleX), range(self.env.tailleY)):
            tres = self.env.grilleTres[x][y]
            if tres and tres.getType() == self.agent_type: 
                self.resources[str(x)+":"+str(y)] = tres.getValue()

