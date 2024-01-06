### planning ###
# all cells will be movable before play starts including walls but the editing area will not include walls i dont want the player to move




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
    if cell_id == 0: #Empty Cell
        return None
    elif cell_id == 1: # Wall Cell
        return {'movable_x': False, 'movable_y': False, 'rotatable': False}
    elif cell_id == 2: # Blank Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': False}
    elif cell_id == 3: # Blank X Cell
        return {'movable_x': True, 'movable_y': False, 'rotatable': True}
    elif cell_id == 4: # Blank Y Cell
        return {'movable_x': False, 'movable_y': True, 'rotatable': True}
    elif cell_id == 5: # Pusher Up Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}
    elif cell_id == 6: # Pusher Down Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}
    elif cell_id == 7: # Pusher Left Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}
    elif cell_id == 8: # Pusher Right Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}
    elif cell_id == 9: # Rotator Clockwise Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': False}
    elif cell_id == 10: # Rotator Anticlockwise Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': False}
    elif cell_id == 11: # Generator Up Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}
    elif cell_id == 12: # Generator Down Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}
    elif cell_id == 13: # Generator Left Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}
    elif cell_id == 14: # Generator Right Cell
        return {'movable_x': True, 'movable_y': True, 'rotatable': True}

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
grid[20][20] = 4
grid[20][19] = 8
grid[21][30] = 2
grid[21][31] = 7
grid[21][29] = 9

def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(grid):
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
                    
                    elif cell_properties(check_id)['movable_y'] == False:
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
                    
                    elif cell_properties(check_id)['movable_y'] == False:
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

                while run:
                    check_id = temp_grid[row][col - x]
                    
                    if check_id == 0:
                        run = False
                    
                    elif cell_properties(check_id)['movable_x'] == False:
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
                    
                    elif cell_properties(check_id)['movable_x'] == False:
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
                temp_grid[row - 1][col] = rotation_mapping.get(above_id, above_id)
                temp_grid[row + 1][col] = rotation_mapping.get(below_id, below_id)
                temp_grid[row][col - 1] = rotation_mapping.get(left_id, left_id)
                temp_grid[row][col + 1] = rotation_mapping.get(right_id, right_id)
            
            elif cell_id == 10: #rotator anticlockwise cell
                above_id = temp_grid[row - 1][col]
                below_id = temp_grid[row + 1][col]
                left_id = temp_grid[row][col - 1]
                right_id = temp_grid[row][col + 1]

                rotation_mapping = {
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
        draw_grid(grid)
        py.display.update()   
   
    py.quit()

if __name__ == "__main__":
    main()