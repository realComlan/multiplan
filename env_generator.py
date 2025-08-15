import os
import random

class Generator:

    def generate_environment_description():
        # Random environment size
        env_width = random.randint(15, 40)
        env_height = env_width#random.randint(15, 30)#
        
        # Start building the content
        content = []
        content.append("#taille env")
        content.append(f"{env_width} {env_height}")
    
        # Generate all possible pairs
        all_pairs = [(x, y) for x in range(0, env_width) for y in range(0, env_height)]
        
        # We first decide the number of each component
        numGoldChests = random.randint(1, env_width*env_height//10)
        numStonesChests = random.randint(1, env_width*env_height//10)
        numGoldAgents = random.randint(1, numGoldChests)#numGoldChests//2)
        numStonesAgents = random.randint(1, numStonesChests)#numStonesChests//2)
        numChestAgents = random.randint(1, numGoldAgents)#(numGoldChests+numStonesChests)//2)
        
        # Then we randomly select unique pairs
        # of positions on the grid
        unique_pairs = random.sample(all_pairs, numGoldChests + numStonesChests + numGoldAgents + numStonesAgents + numChestAgents + 1)
        
        # A counter for picking unique pairs
        # from the set of unique pairs constructed
        # right above
        counter = 0
        # Position depot
        content.append("# position depot")
        depotX = unique_pairs[counter][0]
        depotY = unique_pairs[counter][1]
        content.append(f"{depotX} {depotY}")
        
        counter += 1
    
        # Gold chests
        content.append("# tresors")
        for _ in range(numGoldChests):  # Random number of treasures
            posX = unique_pairs[counter][0]
            posY = unique_pairs[counter][1]
            value = random.randint(1, 10)
            content.append(f"tres:or:{posX}:{posY}:{value}")
            counter += 1
        
        # Stones chests
        for _ in range(numStonesChests):  # Random number of treasures
            posX = unique_pairs[counter][0]
            posY = unique_pairs[counter][1]
            value = random.randint(1, 10)
            content.append(f"tres:pierres:{posX}:{posY}:{value}")
            counter += 1

        # Gold agents
        content.append("#agents")
        for _ in range(numGoldAgents):  # Random number of treasures
            posX = unique_pairs[counter][0]
            posY = unique_pairs[counter][1]
            backpack = random.randint(5, 20)
            content.append(f"AG:or:{posX}:{posY}:{backpack}")
            counter += 1
            
        # Stones agents
        for _ in range(numStonesAgents):  # Random number of treasures
            posX = unique_pairs[counter][0]
            posY = unique_pairs[counter][1]
            backpack = random.randint(5, 20)
            content.append(f"AG:pierres:{posX}:{posY}:{backpack}")
            counter += 1
            
        # Chess opening agents
        for _ in range(numChestAgents):  # Random number of treasures
            posX = unique_pairs[counter][0]
            posY = unique_pairs[counter][1]
            content.append(f"AG:ouvr:{posX}:{posY}")
            counter += 1
    
        # Find a unique filename
        file_number = 1
        while os.path.exists(f"environments/env_{file_number:05d}.txt"):
            file_number += 1
        filename = f"environments/env_{file_number:05d}.txt"
    
        content = '\n'.join(content)
        
        # Save to a file
        with open(filename, 'w') as file:
            file.write(content)
        
        return filename
    
