import pygame, sys, copy

CELL_ALIVE = 1
CELL_DEAD = 0


class GameOfLife:
    def __init__(
        self,
        window_width: int = 800,
        window_height: int = 800,
        fps: int = 30,
        bg_color: pygame.Color = pygame.Color(255, 255, 255),
        alive_color: pygame.Color = pygame.Color(0, 0, 0),
        cell_rows: int = 50,
        cell_cols: int = 50,
        line_color: tuple = (1, 1, 1),
        percent: int = 2,
    ) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps
        self.bg_color = bg_color
        self.alive_color = alive_color
        self.cell_rows = cell_rows
        self.cell_cols = cell_cols
        self.cell_size = self.window_width // self.cell_cols
        self.line_color = line_color
        self.percent = percent
        self.simulation_started = False

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

    def draw_grid(self, currentCells):
        for x in range(0, self.window_width, self.cell_size):
            pygame.draw.line(
                self.screen, self.line_color, (x, 0), (x, self.window_height)
            )
        for y in range(0, self.window_height, self.cell_size):
            pygame.draw.line(
                self.screen, self.line_color, (0, y), (self.window_width, y)
            )

            # Print currentCells on the screen:
        for j, j1 in zip(
            range(0, self.window_height, self.cell_size), range(self.cell_rows)
        ):
            for i, i1 in zip(
                range(0, self.window_width, self.cell_size), range(self.cell_cols)
            ):
                if currentCells[i1][j1] == CELL_ALIVE:
                    pygame.draw.rect(
                        self.screen,
                        self.alive_color,
                        (i, j, self.cell_size, self.cell_size),
                    )

    # Run a single step of the Game of Life simulation:
    def update(self, cell_grid):
        new_grid = copy.deepcopy(cell_grid)

        # Calculate the next step's cells based on current step's cells:
        for x in range(self.cell_cols):
            for y in range(self.cell_rows):
                numNeighbors = self.get_neighbour_count(cell_grid, x, y)

                # Set cell based on Conway's Game of Life rules:
                if cell_grid[x][y] == CELL_ALIVE and (
                    numNeighbors == 2 or numNeighbors == 3
                ):
                    # Living cells with 2 or 3 neighbors stay alive:
                    new_grid[x][y] = CELL_ALIVE
                elif cell_grid[x][y] == CELL_ALIVE and numNeighbors < 2:
                    # Living cells with fewer than 2 neighbors die:
                    new_grid[x][y] = CELL_DEAD
                elif cell_grid[x][y] == CELL_ALIVE and numNeighbors > 3:
                    # Living cells with more than 3 neighbors die:
                    new_grid[x][y] = CELL_DEAD
                elif cell_grid[x][y] == CELL_DEAD and numNeighbors == 3:
                    # Dead cells with 3 neighbors become alive:
                    new_grid[x][y] = CELL_ALIVE

        return new_grid

    def get_neighbour_count(self, cell_grid, x, y):
        num_neighbors = 0

        left_coord = (x - 1) % self.cell_cols
        right_coord = (x + 1) % self.cell_cols
        above_coord = (y - 1) % self.cell_rows
        below_coord = (y + 1) % self.cell_rows

        # Count number of living neighbors:
        if cell_grid[left_coord][above_coord] == CELL_ALIVE:
            num_neighbors += 1
        if cell_grid[x][above_coord] == CELL_ALIVE:
            num_neighbors += 1
        if cell_grid[right_coord][above_coord] == CELL_ALIVE:
            num_neighbors += 1
        if cell_grid[left_coord][y] == CELL_ALIVE:
            num_neighbors += 1
        if cell_grid[right_coord][y] == CELL_ALIVE:
            num_neighbors += 1
        if cell_grid[left_coord][below_coord] == CELL_ALIVE:
            num_neighbors += 1
        if cell_grid[x][below_coord] == CELL_ALIVE:
            num_neighbors += 1
        if cell_grid[right_coord][below_coord] == CELL_ALIVE:
            num_neighbors += 1
        return num_neighbors

    def fill_grid(self, cell_grid, cell_state=CELL_DEAD):
        for x in range(self.cell_cols):
            row = [cell_state] * self.cell_rows
            cell_grid.append(row)
        return cell_grid

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
        cell_grid = []
        cell_grid = self.fill_grid(cell_grid, CELL_DEAD)

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
                    if not self.simulation_started and can_click_cells:
                        cell_x, cell_y = self.get_clicked_cell(pygame.mouse.get_pos())
                        if cell_grid[cell_x][cell_y] == CELL_ALIVE:
                            cell_grid[cell_x][cell_y] = CELL_DEAD
                        else:
                            cell_grid[cell_x][cell_y] = CELL_ALIVE

                # Check for keyboard input (Enter key press)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not self.simulation_started:
                        # Start the simulation when the Enter key is pressed
                        can_click_cells = False
                        self.simulation_started = True

            # Draw / render
            # self.screen.fill(self.bg_color)
            # Update
            if self.simulation_started:
                cell_grid = self.update(cell_grid)
            # self.draw_grid(cell_grid)  # Redraw grid to show user-selected cells

            # # *after* drawing everything, flip the display
            # pygame.display.flip()

            self.render(cell_grid)

        pygame.quit()
        sys.exit()

    def render(self, cell_grid):
        self.screen.fill(self.bg_color)
        self.draw_grid(cell_grid)
        pygame.display.flip()
