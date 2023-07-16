import pygame , sys , copy, random

# Global Variables
WIDTH = 1500
HEIGHT = 1000
FPS = 5

BG_COLOR = (44, 36, 79)

#variables for game of life
width = 120
height = 80
PERCENT = 2

#grid vars
CELL_SIZE = WIDTH // width
CELL_COLOR = (170, 145, 205)

#set aliveCol as black
aliveCol = (211, 179, 251)

#Give grid
def draw_grid(currentCells):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, CELL_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, CELL_COLOR, (0, y), (WIDTH, y))
    
        # Print currentCells on the screen:
    for j , j1 in zip(range(0 , HEIGHT, CELL_SIZE) ,range(height)):
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

def random_fill(nextCells):
    center_width = width // 4  # Center half of the whole width
    center_height = height // 4  # Center half of the whole height

    for x in range(width):
        column = []
        for y in range(height):
            # Check if the cell is within the center region
            if center_width < x < width - center_width and center_height < y < height - center_height:
                # Higher probability of filling cells in the center region (70-80%)
                if random.randint(1, 100) <= 80:  # You can adjust the percentage as desired
                    column.append('#')
                else:
                    column.append(' ')
            else:
                # Lower probability of filling cells in the outer region (20-30%)
                if random.randint(1, 100) <= 30:  # You can adjust the percentage as desired
                    column.append('#')
                else:
                    column.append(' ')
        nextCells.append(column)
    return nextCells



# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

# Create a list of list for the cells and randomly fill the matrix:
nextCells = []
nextCells = random_fill(nextCells)

# Main loop
running = True
prev_matrix = copy.deepcopy(nextCells)
consecutive_stable_iterations = 0
max_stable_iterations = 10

while running:
    clock.tick(FPS)

    # Draw / render
    screen.fill(BG_COLOR)
    # Update
    nextCells = update(nextCells)
    draw_grid(nextCells)  # Redraw grid to show user-selected cells

    # Check if the matrix has stabilized
    if prev_matrix == nextCells:
        consecutive_stable_iterations += 1
    else:
        consecutive_stable_iterations = 0

    # If the matrix has not changed for too many consecutive iterations, refill with random cells
    if consecutive_stable_iterations >= max_stable_iterations:
        nextCells = []
        nextCells = random_fill(nextCells)
        consecutive_stable_iterations = 0

    # Store the current matrix for comparison in the next iteration
    prev_matrix = copy.deepcopy(nextCells)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()