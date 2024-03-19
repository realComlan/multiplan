import pygame
import sys

class Board:

    instance = None

    treasures_font = None
    agents_font = None
    button_font = None

    PAUSE_BUTTON_TEXT = "go"
    RESTART_BUTTON_TEXT = "restart"
    NEW_BUTTON_TEXT = "new"
    MESSAGE_BOARD_TEXT = "Press 'go' to start!"
    SPEED_PLUS_BUTTON_TEXT = "+"
    SPEED_MINUS_BUTTON_TEXT = "-"

    def __init__(self): 
        # Frame per second rate of refresh
        self.fps = 7
        # Initialize Pygame
        pygame.init()
        self.new = True
        self.run_time = 0
        self.running = False
        self.font = pygame.font.Font(None, 15)
        Board.treasures_font = pygame.font.Font(None, 25)
        Board.agents_font = pygame.font.Font(None, 15)
        Board.button_font = pygame.font.Font(None, 25)  # Default font and size

    def update_scene_params(self):
        if self.new:
            from PlanManager import PlanManager
            self.plan_manager = PlanManager.get_instance()
            
            self.new = False
            
            # Default screen dimensions and title
            self.screen_width = 730
            self.screen_height = 730
            pygame.display.set_caption('Treasure Hunting in ' + self.plan_manager.env_file)

            self.grid_width = self.plan_manager.env.tailleY
            self.grid_height = self.plan_manager.env.tailleX

            # Grid dimensions
            if self.screen_width/self.grid_width < self.screen_height/self.grid_height:
                cell_size = int(self.screen_width/self.grid_width)
            else:
                cell_size = int(self.screen_height/self.grid_height)

            # Adjust screen size
            if self.grid_width >= self.grid_height:
                self.screen_width = self.grid_width * cell_size
            if self.grid_width <= self.grid_height:
                self.screen_height = self.grid_height * cell_size + 50
            cell_size = 5 if cell_size <= 0 else cell_size
            
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.cell_size = cell_size
        
    def go(self):

        clock = pygame.time.Clock()

        while self.running:
            # if need be...
            self.update_scene_params()

            # Draw the scene
            self.draw_scene()

            # Let each agent do their thing
            agents_are_still_acting = False
            for agent in self.plan_manager.agents.values():
                # if at least one agent has a non empty local plan
                # then we are not over yet
                agents_are_still_acting = agent.act() or agents_are_still_acting

            if not agents_are_still_acting:
                score = str(self.plan_manager.env.score)
                Board.MESSAGE_BOARD_TEXT = "Terminé! Score final: " + score + "."# in " + str(self.run_time) + " frames."
            else: 
                self.run_time += 1

            # Draw the new state of agents and chests
            self.draw_agents_and_treasures()

            self.buttons()  # Draw the buttons

            # Update display
            pygame.display.flip()

            # 
            clock.tick(self.fps) 

        # quand le jeu est mis en pause 
        # les agents n'executent pas leurs plans 
        while not self.running:
            # if need be...
            self.update_scene_params()
            # Draw the scene
            self.draw_scene()

            # Draw the new state of agents and chests
            self.draw_agents_and_treasures()

            self.buttons()  # Draw the buttons

            # Update display
            pygame.display.flip()

            # 
            clock.tick(self.fps) 

        if self.running:
            self.go()

        pygame.quit()
        sys.exit()

    def draw_agents_and_treasures(self):
        # Draw agents and treasures
        for treasure in self.plan_manager.treasures:
            treasure.draw(self.screen, self.cell_size)
        for agent in self.plan_manager.agents.values():
            agent.draw(self.screen, self.cell_size)

    def draw_scene(self):
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_button_click(event.pos)

        self.screen.fill(Color.WHITE)
        
        # Draw grid
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, Color.BLACK, rect, 1)
        
        # Draw zone de depot
        self.draw_depot_zone()

    def draw_depot_zone(self):
        text = str(self.plan_manager.env.score)
        text_surface = self.font.render(text, True, Color.WHITE)
        text_rect = text_surface.get_rect()
        rect = pygame.draw.rect(self.screen, Color.BLACK, (self.plan_manager.env.posUnload[1] * self.cell_size, \
                                                            self.plan_manager.env.posUnload[0] * self.cell_size, \
                                                            self.cell_size, self.cell_size))
        text_rect.center = rect.center
        self.screen.blit(text_surface, text_rect)
    
    def buttons(self):
        # Button properties
        
        self.button_width, self.button_height = 100, 40
        self.button_positions = {
            Board.PAUSE_BUTTON_TEXT: (10, self.screen_height - 45, self.button_width),
            Board.RESTART_BUTTON_TEXT: (10+5+self.button_width, self.screen_height - 45, self.button_width),
            Board.NEW_BUTTON_TEXT: (10+10+2*self.button_width, self.screen_height - 45, self.button_width),
            Board.SPEED_PLUS_BUTTON_TEXT: (10+15+3*self.button_width, self.screen_height - 45, 20),
            Board.SPEED_MINUS_BUTTON_TEXT: (10+20+3*self.button_width+20, self.screen_height - 45, 20),
            Board.MESSAGE_BOARD_TEXT: (10+25+3*self.button_width+40, self.screen_height - 45, 330),
        }

        button_text = Board.PAUSE_BUTTON_TEXT
        x, y, w = self.button_positions[button_text]
        pygame.draw.rect(self.screen, Color.LIGHT_YELLOW, (x, y, w, self.button_height))
        text_surf = Board.button_font.render(button_text, True, Color.BLACK)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + self.button_height / 2))
        self.screen.blit(text_surf, text_rect)

        button_text = Board.RESTART_BUTTON_TEXT
        x, y, w = self.button_positions[button_text]
        pygame.draw.rect(self.screen, Color.BLUE, (x, y, w, self.button_height))
        text_surf = Board.button_font.render(button_text, True, Color.WHITE)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + self.button_height / 2))
        self.screen.blit(text_surf, text_rect)

        button_text = Board.NEW_BUTTON_TEXT
        x, y, w = self.button_positions[button_text]
        pygame.draw.rect(self.screen, Color.GREEN, (x, y, w, self.button_height))
        text_surf = Board.button_font.render(button_text, True, Color.WHITE)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + self.button_height / 2))
        self.screen.blit(text_surf, text_rect)

        button_text = Board.SPEED_PLUS_BUTTON_TEXT
        x, y, w = self.button_positions[button_text]
        pygame.draw.rect(self.screen, Color.BLACK, (x, y, w, self.button_height))
        text_surf = Board.button_font.render(button_text, True, Color.WHITE)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + self.button_height / 2))
        self.screen.blit(text_surf, text_rect)

        button_text = Board.SPEED_MINUS_BUTTON_TEXT
        x, y, w = self.button_positions[button_text]
        pygame.draw.rect(self.screen, Color.GRAY, (x, y, w, self.button_height))
        text_surf = Board.button_font.render(button_text, True, Color.BLACK)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + self.button_height / 2))
        self.screen.blit(text_surf, text_rect)

        button_text = Board.MESSAGE_BOARD_TEXT
        x, y, w = self.button_positions[button_text]
        pygame.draw.rect(self.screen, Color.LIGHT_GRAY, (x, y, w, self.button_height))
        text_surf = Board.button_font.render(button_text, True, Color.BLACK)
        text_rect = text_surf.get_rect(center=(x + w/2, y + self.button_height / 2))
        self.screen.blit(text_surf, text_rect)

    # Function to handle button clicks
    def handle_button_click(self, pos):
        x, y = pos
        for button_text, (bx, by, bw) in self.button_positions.items():
            if bx <= x <= bx + bw and by <= y <= by + self.button_height:
                if button_text == Board.PAUSE_BUTTON_TEXT:
                    self.running = not self.running
                    if self.running:
                        Board.PAUSE_BUTTON_TEXT = "pause"
                        Board.MESSAGE_BOARD_TEXT = "Game running at " + str(self.fps) + " fps."
                    else:
                        Board.PAUSE_BUTTON_TEXT = "go"
                        Board.MESSAGE_BOARD_TEXT = "Game is paused! Press 'go' to resume."
                elif button_text == Board.RESTART_BUTTON_TEXT:
                    self.plan_manager.rewind()
                    self.run_time = 0
                    Board.MESSAGE_BOARD_TEXT = "Game has restarted from scratch!"
                elif button_text == Board.NEW_BUTTON_TEXT:
                    self.plan_manager = self.plan_manager.__class__.get_new_instance()
                    self.run_time = 0
                    self.new = True
                    Board.MESSAGE_BOARD_TEXT = "New game instance generated!"
                elif button_text == Board.SPEED_PLUS_BUTTON_TEXT:
                    self.fps += 2
                    self.fps = min(60, self.fps)
                    Board.MESSAGE_BOARD_TEXT = "Game running at " + str(self.fps) + " fps."
                elif button_text == Board.SPEED_MINUS_BUTTON_TEXT:
                    self.fps -= 2
                    self.fps = max(1, self.fps)
                    Board.MESSAGE_BOARD_TEXT = "Game running at " + str(self.fps) + " fps."
    
    def get_instance():
        if not Board.instance:
            Board.instance = Board()
        return Board.instance


class Color:
    BLUE = (0, 0, 255)
    GOLD = (255, 215, 0)
    LIGHT_YELLOW =  (255, 239, 128)
    STONE = (155, 17, 30)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (230, 230, 230)
    RED = (255, 0, 0)
    LIGHT_RED =  (255, 204, 203)
    GREEN = (0, 128, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

if __name__ == "__main__":
    Board({"grid_width": 40, "grid_height": 40}).go()
