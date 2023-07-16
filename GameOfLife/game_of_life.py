import pygame , sys , copy

CELL_ALIVE = 1
CELL_DEAD = 0

class GameOfLife:
    def __init__(self, 
                    window_width: int = 800,
                    window_height: int = 800,
                    fps: int = 30,
                    bg_color: pygame.Color = pygame.Color(255, 255, 255),
                    alive_color: pygame.Color = pygame.Color(0, 0, 0),
                    cell_width: int = 50,
                    cell_height: int = 50,
                    line_color: tuple = (1, 1, 1),
                    percent: int = 2
                 ) -> None:

        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps
        self.bg_color = bg_color
        self.alive_color = alive_color
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_size = self.window_width // self.cell_width
        self.line_color = line_color
        self.percent = percent


        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

    def draw_grid(self, currentCells):
        for x in range(0, self.window_width, self.cell_size):
            pygame.draw.line(self.screen, self.line_color, (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.cell_size):
            pygame.draw.line(self.screen, self.line_color, (0, y), (self.window_width, y))
        
            # Print currentCells on the screen:
        for j , j1 in zip(range(0 , self.window_height , self.cell_size) ,range(self.cell_height)):
            for i , i1 in zip(range(0 , self.window_width , self.cell_size) , range(self.cell_width)):
                if currentCells[i1][j1] == CELL_ALIVE:
                    pygame.draw.rect(self.screen , self.alive_color , (i , j , self.cell_size , self.cell_size))

    # Run a single step of the Game of Life simulation:
    def update(self, nextCells):
        currentCells = copy.deepcopy(nextCells)        
        self.draw_grid(currentCells)
        # Calculate the next step's cells based on current step's cells:
        for x in range(self.cell_width):
            for y in range(self.cell_height):
                # Get neighboring coordinates:
                leftCoord  = (x - 1) % self.cell_width
                rightCoord = (x + 1) % self.cell_width
                aboveCoord = (y - 1) % self.cell_height
                belowCoord = (y + 1) % self.cell_height

                # Count number of living neighbors:
                numNeighbors = 0
                if currentCells[leftCoord][aboveCoord] == CELL_ALIVE:
                    numNeighbors += 1
                if currentCells[x][aboveCoord] == CELL_ALIVE:
                    numNeighbors += 1
                if currentCells[rightCoord][aboveCoord] == CELL_ALIVE:
                    numNeighbors += 1
                if currentCells[leftCoord][y] == CELL_ALIVE:
                    numNeighbors += 1
                if currentCells[rightCoord][y] == CELL_ALIVE:
                    numNeighbors += 1
                if currentCells[leftCoord][belowCoord] == CELL_ALIVE:
                    numNeighbors += 1
                if currentCells[x][belowCoord] == CELL_ALIVE:
                    numNeighbors += 1
                if currentCells[rightCoord][belowCoord] == CELL_ALIVE:
                    numNeighbors += 1
                
                # Set cell based on Conway's Game of Life rules:
                if currentCells[x][y] == CELL_ALIVE and (numNeighbors == 2 or numNeighbors == 3):
                    # Living cells with 2 or 3 neighbors stay alive:
                    nextCells[x][y] = CELL_ALIVE
                elif currentCells[x][y] == CELL_ALIVE and numNeighbors < 2:
                    # Living cells with fewer than 2 neighbors die:
                    nextCells[x][y] = CELL_DEAD
                elif currentCells[x][y] == CELL_ALIVE and numNeighbors >3:
                    # Living cells with more than 3 neighbors die:
                    nextCells[x][y] = CELL_DEAD
                elif currentCells[x][y] == CELL_DEAD and numNeighbors == 3:
                    # Dead cells with 3 neighbors become alive:
                    nextCells[x][y] = CELL_ALIVE

        return nextCells

    def fillMat(self, nextCells):
        for x in range(self.cell_width):
            column = []
            for y in range(self.cell_height):
                column.append(CELL_DEAD)
            nextCells.append(column)
        return nextCells

    def check_button_click(self, button_rect):
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            return True
        return False

    def get_clicked_cell(self, pos):
        x, y = pos
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        return cell_x, cell_y


    def run(self):

        # Create a list of list for the cells:
        nextCells = []
        nextCells = self.fillMat(nextCells)

        # Flag to check if the simulation has started
        simulation_started = False

        # Flag to check if cells can be clicked
        can_click_cells = True
        # Main loop
        running = True
        while running:
            self.clock.tick(self.fps)

            # Process input (events)
            for event in pygame.event.get():
                # Check for closing window
                if event.type == pygame.QUIT:
                    running = False

                # Check for mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not simulation_started and can_click_cells:
                        cell_x, cell_y = self.get_clicked_cell(pygame.mouse.get_pos())
                        if nextCells[cell_x][cell_y] == CELL_ALIVE:
                            nextCells[cell_x][cell_y] = CELL_DEAD
                        else:
                            nextCells[cell_x][cell_y] = CELL_ALIVE

                # Check for keyboard input (Enter key press)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not simulation_started:
                        # Start the simulation when the Enter key is pressed
                        can_click_cells = False
                        simulation_started = True


            # Draw / render
            self.screen.fill(self.bg_color)
            # Update
            if simulation_started:
                nextCells = self.update(nextCells)
            self.draw_grid(nextCells)  # Redraw grid to show user-selected cells

            # *after* drawing everything, flip the display
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = GameOfLife()
    game.run()