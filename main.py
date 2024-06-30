import pygame as py
import pathlib

py.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 25
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = py.display.set_mode((WIDTH, HEIGHT))

clock = py.time.Clock()


IMAGE_DIR = pathlib.Path(__file__).parent/'images'

cell_images = {
    1: py.image.load(IMAGE_DIR / 'Wall.png'),
    2: py.image.load(IMAGE_DIR / 'Blank4.png'),
    3: py.image.load(IMAGE_DIR / 'BlankX.png'),
    4: py.image.load(IMAGE_DIR / 'BlankY.png'),
    5: py.image.load(IMAGE_DIR / 'PusherUp.png'),
    6: py.image.load(IMAGE_DIR / 'PusherDown.png'),
    7: py.image.load(IMAGE_DIR / 'PusherLeft.png'),
    8: py.image.load(IMAGE_DIR / 'PusherRight.png'),
    9: py.image.load(IMAGE_DIR / 'GeneratorUp.png'),
    10: py.image.load(IMAGE_DIR / 'GeneratorDown.png'),
    11: py.image.load(IMAGE_DIR / 'GeneratorLeft.png'),
    12: py.image.load(IMAGE_DIR / 'GeneratorRight.png'),
    13: py.image.load(IMAGE_DIR / 'RotatorClockwise.png'),
    14: py.image.load(IMAGE_DIR / 'RotatorAnticlockwise.png')
}


#Scale images to fit the size of the grid
for i in cell_images:
    cell_images[i] = py.transform.scale(cell_images[i], (TILE_SIZE, TILE_SIZE))

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Set the borders to wall cells
for col in range(GRID_WIDTH):
    grid[0][col] = 1
    grid[GRID_HEIGHT - 1][col] = 1

for row in range(GRID_HEIGHT):
    grid[row][0] = 1
    grid[row][GRID_WIDTH - 1] = 1


grid[5][5] = 8
grid[6][5] = 8
grid[5][6] = 6
grid[6][6] = 3
grid[5][7] = 12


def draw_grid():
    global grid
    screen.fill(BLACK)

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            cell_id = grid[row][col]

            if cell_id in cell_images:
                screen.blit(cell_images[cell_id], (col * TILE_SIZE, row * TILE_SIZE))
            else:
                # Handle the case where the cell_id does not have an associated image
                py.draw.rect(screen, (0, 0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        py.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        py.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    
    py.display.update()   


def cell_properties(cell_id):
    if cell_id == 0:  # Empty Cell
        return {'movable_x': True, 'movable_y': True}
    elif cell_id == 1:  # Wall Cell
        return {'movable_x': False, 'movable_y': False}
    elif cell_id == 2:  # Blank Cell
        return {'movable_x': True, 'movable_y': True}
    elif cell_id == 3:  # Blank X Cell
        return {'movable_x': True, 'movable_y': False}
    elif cell_id == 4:  # Blank Y Cell
        return {'movable_x': False, 'movable_y': True}
    elif cell_id in (5, 6, 7, 8, 9, 10, 11, 12, 13, 14):  # Every Other Cell
        return {'movable_x': True, 'movable_y': True}
    else:  # Default case for undefined cell_ids
        return {}


def adjust_grid():
    global grid

    for ID in range(5, 15):
        if ID >= 5 and ID <= 8:
            grid = pusher(ID)
        elif ID >= 9 and ID <= 12:
            grid = generator(ID)
        elif ID == 13 or ID == 14:
            grid = rotator(ID)
        

    return grid

def pusher(ID): 
    global grid
    temp_grid = [row[:] for row in grid]  # Create a new grid to avoid modifying the original during iteration

    directions = {
        5: (-1, 0, 6, 'movable_y'),  # pusher up cell
        6: (1, 0, 5, 'movable_y'),   # pusher down cell
        7: (0, -1, 8, 'movable_x'),  # pusher left cell
        8: (0, 1, 7, 'movable_x'),   # pusher right cell
    }

    sy, sx, opp_id, movable = directions[ID]
    
    # Determine the direction of iteration based on direction of pusher cell
    if sy == -1 or sx == -1:  # pusher up/left
        row_range = range(GRID_HEIGHT)
        col_range = range(GRID_WIDTH)
    elif sy == 1:  # pusher down
        row_range = range(GRID_HEIGHT - 1, -1, -1)
        col_range = range(GRID_WIDTH)
    elif sx == 1:  # pusher right
        row_range = range(GRID_HEIGHT)
        col_range = range(GRID_WIDTH - 1, -1, -1)

    for row in row_range:
        for col in col_range:
            cell_id = grid[row][col]
            if cell_id == ID:  # Check the grid for the specified ID
                run = True
                y = 0
                list_cell = []

                while run:
                    check_id = grid[row + y*sy][col + y*sx]

                    if check_id == 0:
                        run = False
                    elif (cell_properties(check_id)[movable] == False) or (check_id == opp_id):
                        run = False
                        list_cell = []
                    else:
                        list_cell.append(check_id)
                        y += 1

                while list_cell:
                    temp_grid[row + y*sy][col + y*sx] = list_cell.pop()
                    y -= 1
                    temp_grid[row][col] = 0

    return temp_grid  # Return the modified grid

def generator(ID):
    global grid
    temp_grid = [row[:] for row in grid]  # Create a new grid to avoid modifying the original during iteration

    directions = {
        9: (-1, 0, 10, 'movable_y'),  # generator up cell
        10: (1, 0, 9, 'movable_y'),   # generator down cell
        11: (0, -1, 12, 'movable_x'),  # generator left cell
        12: (0, 1, 11, 'movable_x')   # generator right cell
    }

    if ID not in directions:
        print("Unexpected value received: generator subroutine")
        return grid

    sy, sx, opp_id, movable = directions[ID]

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] == ID and grid[row - sy][col - sx] != 0:  # Check against the specified ID
                run = True
                generate = True
                y = 1
                list_cell = []

                while run:
                    check_id = grid[row + y*sy][col + y*sx]

                    if check_id == 0:
                        run = False
                    elif (cell_properties(check_id)[movable] == False) or (check_id == opp_id and grid[row + sy * (y +1)][col + sx * (y + 1)] != 0):
                        run = False
                        list_cell = []
                        generate = False
                    else:
                        list_cell.append(check_id)
                        y += 1

                while list_cell:
                    temp_grid[row + y * sy][col + y * sx] = list_cell.pop()
                    y -= 1

                if generate:  # Set the cell right in front of the generator to the cell behind
                    temp_grid[row + sy][col + sx] = grid[row - sy][col - sx]

    return temp_grid  # Return the modified grid

def rotator(ID):
    global grid
    temp_grid = [row[:] for row in grid]  # Create a new grid to avoid modifying the original during iteration

    rotation_mapping_clockwise = {
                    0:0, # Empty
                    1:1, # Wall
                    2:2, # Blank
                    13:13, # Rotator
                    14:14, # Rotator
                    
                    3: 4, # blank x to y
                    4: 3, # blank y to x
                    
                    5: 8, # pusher up to right
                    8: 6, # pusher right to down
                    6: 7, # pusher down to left
                    7: 5, # pusher left to up

                    9: 12, # generator up to right
                    12: 10, # generator right to down
                    10: 11, # generator down to left
                    11: 9  # generator left to up
                }

    rotation_mapping_anticlockwise = {
                    0:0, # Empty
                    1:1, # Wall
                    2:2, # Blank
                    13:13, # Rotator
                    14:14, # Rotator
                    
                    3: 4, # blank x to y
                    4: 3, # blank y to x
                    
                    5: 7, # pusher up to left
                    7: 6, # pusher left to down
                    6: 8, # pusher down to right
                    8: 5, # pusher left to up

                    9: 11, # generator up to left
                    11: 10, # generator left to down
                    10: 12, # generator down to right
                    12: 9  # generator right to up
                }

    if ID == 13:
        rotation_mapping = rotation_mapping_clockwise
    elif ID == 14:
        rotation_mapping = rotation_mapping_anticlockwise

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            cell_id = grid[row][col]
            if cell_id == ID:  # Check against the specified ID
                temp_grid[row - 1][col] = rotation_mapping[temp_grid[row - 1][col]]
                temp_grid[row + 1][col] = rotation_mapping[temp_grid[row + 1][col]]
                temp_grid[row][col - 1] = rotation_mapping[temp_grid[row][col - 1]]
                temp_grid[row][col + 1] = rotation_mapping[temp_grid[row][col + 1]]
    return temp_grid


def main():
    global grid
    window_running = True
    sim_running = False
    count = 0
    update_freq = FPS * 0.4

    while window_running:
        clock.tick(FPS)

        if sim_running:
            count += 1

        if count >= update_freq:
            count = 0
            grid = adjust_grid()

        py.display.set_caption("Playing" if sim_running else "Paused")

        for event in py.event.get():
            if event.type == py.QUIT:
                window_running = False
            
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    sim_running = not sim_running
                
                if event.key == py.K_c:
                    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                    sim_running = False
                    count = 0
        
        draw_grid()
   
    py.quit()

if __name__ == "__main__":
    main()