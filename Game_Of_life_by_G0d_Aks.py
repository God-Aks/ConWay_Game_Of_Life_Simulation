import pygame , sys , copy

# Global Variables
WIDTH = 800
HEIGHT = 800
FPS = 30

BG_COLOR = (255, 255, 255)

#variables for game of life
width = 50
height = 50
PERCENT = 2

#grid vars
CELL_SIZE = WIDTH // width
CELL_COLOR = (1, 1, 1)

#set aliveCol as green
aliveCol = (0, 0, 0)

#Give grid
def draw_grid(currentCells):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, CELL_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, CELL_COLOR, (0, y), (WIDTH, y))
    
        # # Print currentCells on the screen:
    for j , j1 in zip(range(0 , HEIGHT , CELL_SIZE) ,range(height)):
        for i , i1 in zip(range(0 , WIDTH , CELL_SIZE) , range(width)):
            if currentCells[i1][j1] == '#':
                pygame.draw.rect(screen , aliveCol , (i , j , CELL_SIZE , CELL_SIZE))
                # pass

# Run a single step of the Game of Life simulation:
def update(nextCells):
    currentCells = copy.deepcopy(nextCells)        
    draw_grid(currentCells)
    # Calculate the next step's cells based on current step's cells:
    for x in range(width):
        for y in range(height):
            # Get neighboring coordinates:
            leftCoord  = (x - 1) % width
            rightCoord = (x + 1) % width
            aboveCoord = (y - 1) % height
            belowCoord = (y + 1) % height

            # Count number of living neighbors:
            numNeighbors = 0
            if currentCells[leftCoord][aboveCoord] == '#':
                numNeighbors += 1
            if currentCells[x][aboveCoord] == '#':
                numNeighbors += 1
            if currentCells[rightCoord][aboveCoord] == '#':
                numNeighbors += 1
            if currentCells[leftCoord][y] == '#':
                numNeighbors += 1
            if currentCells[rightCoord][y] == '#':
                numNeighbors += 1
            if currentCells[leftCoord][belowCoord] == '#':
                numNeighbors += 1
            if currentCells[x][belowCoord] == '#':
                numNeighbors += 1
            if currentCells[rightCoord][belowCoord] == '#':
                numNeighbors += 1
            
            # Set cell based on Conway's Game of Life rules:
            if currentCells[x][y] == '#' and (numNeighbors == 2 or numNeighbors == 3):
                # Living cells with 2 or 3 neighbors stay alive:
                nextCells[x][y] = '#'
            elif currentCells[x][y] == '#' and numNeighbors < 2:
                # Living cells with fewer than 2 neighbors die:
                nextCells[x][y] = ' '
            elif currentCells[x][y] == '#' and numNeighbors >3:
                # Living cells with more than 3 neighbors die:
                nextCells[x][y] = ' '
            elif currentCells[x][y] == ' ' and numNeighbors == 3:
                # Dead cells with 3 neighbors become alive:
                nextCells[x][y] = '#'

    return nextCells

def fillMat(nextCells):
    for x in range(width):
        column = []
        for y in range(height):
            column.append(' ')
        nextCells.append(column)
    return nextCells

def check_button_click(button_rect):
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        return True
    return False

def get_clicked_cell(pos):
    x, y = pos
    cell_x = x // CELL_SIZE
    cell_y = y // CELL_SIZE
    return cell_x, cell_y


# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

# Create a list of list for the cells:
nextCells = []
nextCells = fillMat(nextCells)

# Flag to check if the simulation has started
simulation_started = False

# Flag to check if cells can be clicked
can_click_cells = True
# Main loop
running = True
while running:
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not simulation_started and can_click_cells:
                cell_x, cell_y = get_clicked_cell(pygame.mouse.get_pos())
                if nextCells[cell_x][cell_y] == '#':
                    nextCells[cell_x][cell_y] = ' '
                else:
                    nextCells[cell_x][cell_y] = '#'

        # Check for keyboard input (Enter key press)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not simulation_started:
                # Start the simulation when the Enter key is pressed
                can_click_cells = False
                simulation_started = True


    # Draw / render
    screen.fill(BG_COLOR)
    # Update
    if simulation_started:
        nextCells = update(nextCells)
    draw_grid(nextCells)  # Redraw grid to show user-selected cells

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()