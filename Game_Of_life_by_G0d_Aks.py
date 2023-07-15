import pygame , sys , random , time , copy

# Global Variables
WIDTH = 700
HEIGHT = 700
FPS = 60

BG_COLOR = (40, 0, 0)

#variables for game of life
width = 100
height = 100
PERCENT = 2

#grid vars
CELL_SIZE = WIDTH // width
CELL_COLOR = (0, 0, 0)

#set aliveCol as green
aliveCol = (50, 255, 0)

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
            # `% width` ensures leftCoord is always between 0 and width - 1
            # %height also for the same reason
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
            # elif currentCells[x][y] == '#' and numNeighbors < 2:
            #     # Living cells with fewer than 2 neighbors die:
            #     nextCells[x][y] = ' '
            elif currentCells[x][y] == '#' and numNeighbors >3:
                # Living cells with more than 3 neighbors die:
                nextCells[x][y] = ' '
            elif currentCells[x][y] == ' ' and numNeighbors == 3:
                # Dead cells with 3 neighbors become alive:
                nextCells[x][y] = '#'

    return nextCells

def fillMat(nextCells):
    for x in range(width):
        temp = []
        for i in range(PERCENT*(height//100)):
            var = random.choice(range(height))
            if var not in temp:
                temp.append(var)
            else:
                temp.append(var+1 if var!=height-1 and var+1 not in temp else var-1)
        column = []
        for y in range(height):
            if y in temp:
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

# Create a list of list for the cells:
nextCells = []
nextCells = fillMat(nextCells)

#main loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    time.sleep(0.5)  #Uncomment this line to make simulation slower

    # Draw / render
    screen.fill(BG_COLOR)

    # Update
    nextCells = update(nextCells)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()
