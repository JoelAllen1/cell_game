import pygame as py
import random
import copy

py.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = py.display.set_mode((WIDTH, HEIGHT))

clock = py.time.Clock()


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



grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
grid[20][20] = 3
grid[30][20] = 5
grid[19][36] = 7
grid[19][35] = 4
grid[19][34] = 9


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid():
    global grid
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            cell_id = grid[row][col]

            colour = None

            if cell_id == 0:
                continue
            elif cell_id == 1:
                colour = GREY
            elif cell_id == 2:
                colour = YELLOW
            elif cell_id == 3 or cell_id == 4:
                colour = ORANGE
            elif cell_id == 5 or cell_id == 6 or cell_id == 7 or cell_id == 8:
                colour = BLUE
            elif cell_id == 9 or cell_id == 10:
                colour = RED
            elif cell_id == 11 or cell_id == 12 or cell_id == 13 or cell_id == 14:
                colour = GREEN

            top_left = (col * TILE_SIZE, row * TILE_SIZE)
            py.draw.rect(screen, colour, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        py.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        py.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjust_grid():
    global grid

    for ID in range(5, 15):
        if ID <= 8 and ID >= 5:
            grid = pusher(ID)
        elif ID == 9 or ID == 10:
            grid = rotator(ID)
        elif ID >= 11 and ID <= 14:
            pass  # generator subroutine

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

    if ID not in directions:
        print("Unexpected value received: pusher subroutine")
        return grid

    sy, sx, opp_id, movable = directions[ID]
    
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            cell_id = grid[row][col]
            if cell_id == ID:  # Check against the specified ID
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
                    temp_grid[row + y*sy][col + y*sx] = list_cell[-1]
                    y -= 1
                    list_cell.pop()
                    temp_grid[row][col] = 0

    return temp_grid  # Return the modified grid

def rotator(ID):
    global grid
    temp_grid = [row[:] for row in grid]  # Create a new grid to avoid modifying the original during iteration

    rotation_mapping_clockwise = {
                    0:0, # Empty
                    1:1, # Wall
                    2:2, # Blank
                    9:9, # Rotator
                    10:10, # Rotator
                    
                    3: 4, # blank x to y
                    4: 3, # blank y to x
                    
                    5: 8, # pusher up to right
                    8: 6, # pusher right to down
                    6: 7, # pusher down to left
                    7: 5, # pusher left to up

                    11: 14, # generator up to right
                    14: 12, # generator right to down
                    12: 13, # generator down to left
                    13: 11  # generator left to up
                }

    rotation_mapping_anticlockwise = {
                    0:0, # Empty
                    1:1, # Wall
                    2:2, # Blank
                    9:9, # Rotator
                    10:10, # Rotator
                    
                    3: 4, # blank x to y
                    4: 3, # blank y to x
                    
                    5: 7, # pusher up to left
                    7: 6, # pusher left to down
                    6: 8, # pusher down to right
                    8: 5, # pusher left to up

                    11: 13, # generator up to left
                    13: 12, # generator left to down
                    12: 14, # generator down to right
                    14: 11  # generator right to up
                }
    
    if ID not in rotation_mapping_clockwise and rotation_mapping_anticlockwise:
        print("Unexpected value received: rotator subroutine")
        return grid

    if ID == 9:
        rotation_mapping = rotation_mapping_clockwise
    elif ID == 10:
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




def adjust_grid_deprecated():
    global grid
    temp_grid = copy.deepcopy(grid)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            cell_id = temp_grid[row][col]

            if cell_id == 5: #pusher up cell
                run = True
                y = 0
                list_cell = []

                while run:
                    check_id = temp_grid[row - y][col]
                    
                    if check_id == 0:
                        run = False
                    
                    elif (cell_properties(check_id)['movable_y'] == False) or (check_id == 6):
                        run = False
                        list_cell = []
                    else:
                        list_cell.append(check_id)
                        y += 1
                
                while list_cell:
                    grid[row - y][col] = list_cell[-1]
                    y -= 1
                    list_cell.pop()
                    grid[row][col] = 0
            
            elif cell_id == 6: #pusher down cell
                run = True
                y = 0
                list_cell = []

                while run:
                    check_id = temp_grid[row + y][col]
                    
                    if check_id == 0:
                        run = False
                    
                    elif (cell_properties(check_id)['movable_y'] == False) or (check_id == 5):
                        run = False
                        list_cell = []
                    else:
                        list_cell.append(check_id)
                        y += 1
                
                while list_cell:
                    grid[row + y][col] = list_cell[-1]
                    y -= 1
                    list_cell.pop()
                    grid[row][col] = 0         
            
            elif cell_id == 7: #pusher left cell
                run = True
                x = 0
                list_cell = []
                sy = 0
                while run:
                    check_id = temp_grid[row][col - x]
                    
                    if check_id == 0:
                        run = False
                    
                    elif (cell_properties(check_id)['movable_x'] == False) or (check_id == 8):
                        run = False
                        list_cell = []
                    else:
                        list_cell.append(check_id)
                        x += 1
                
                while list_cell:
                    grid[row][col - x] = list_cell[-1]
                    x -= 1
                    list_cell.pop()
                    grid[row][col] = 0

            elif cell_id == 8: #pusher right cell
                run = True
                x = 0
                list_cell = []

                while run:
                    check_id = temp_grid[row][col + x]
                    
                    if check_id == 0:
                        run = False
                    
                    elif (cell_properties(check_id)['movable_x'] == False) or (check_id == 9):
                        run = False
                        list_cell = []
                    else:
                        list_cell.append(check_id)
                        x += 1
                
                while list_cell:
                    grid[row][col + x] = list_cell[-1]
                    x -= 1
                    list_cell.pop()
                    grid[row][col] = 0      


            elif cell_id == 9: #rotator clockwise cell
                above_id = temp_grid[row - 1][col]
                below_id = temp_grid[row + 1][col]
                left_id = temp_grid[row][col - 1]
                right_id = temp_grid[row][col + 1]

                rotation_mapping = {
                    0:0, # Empty
                    1:1, # Wall
                    2:2, # Blank
                    9:9, # Rotator
                    10:10, # Rotator
                    
                    3: 4, # blank x to y
                    4: 3, # blank y to x
                    
                    5: 8, # pusher up to right
                    8: 6, # pusher right to down
                    6: 7, # pusher down to left
                    7: 5, # pusher left to up

                    11: 14, # generator up to right
                    14: 12, # generator right to down
                    12: 13, # generator down to left
                    13: 11  # generator left to up
                }

                # Rotate the neighboring cells
                temp_grid[row - 1][col] = rotation_mapping[above_id]
                temp_grid[row + 1][col] = rotation_mapping[below_id]
                temp_grid[row][col - 1] = rotation_mapping[left_id]
                temp_grid[row][col + 1] = rotation_mapping[right_id]
            
            elif cell_id == 10: #rotator anticlockwise cell
                above_id = temp_grid[row - 1][col]
                below_id = temp_grid[row + 1][col]
                left_id = temp_grid[row][col - 1]
                right_id = temp_grid[row][col + 1]

                rotation_mapping = {
                    0:0, # Empty
                    1:1, # Wall
                    2:2, # Blank
                    9:9, # Rotator
                    10:10, # Rotator
                    
                    3: 4, # blank x to y
                    4: 3, # blank y to x
                    
                    5: 7, # pusher up to left
                    7: 6, # pusher left to down
                    6: 8, # pusher down to right
                    8: 5, # pusher left to up

                    11: 13, # generator up to left
                    13: 12, # generator left to down
                    12: 14, # generator down to right
                    14: 11  # generator right to up
                }

                # Rotate the neighboring cells
                temp_grid[row - 1][col] = rotation_mapping[above_id]
                temp_grid[row + 1][col] = rotation_mapping[below_id]
                temp_grid[row][col - 1] = rotation_mapping[left_id]
                temp_grid[row][col + 1] = rotation_mapping[right_id]
    return (grid)


def main():
    global grid
    window_running = True
    sim_running = False
    count = 0
    update_freq = FPS * 0.5

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
                
    
        screen.fill(BLACK)
        draw_grid()
        py.display.update()   
   
    py.quit()

if __name__ == "__main__":
    main()