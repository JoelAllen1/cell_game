import pygame as py
import pathlib
import button
import ast
import sys

py.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 0
GRID_WIDTH = 0
GRID_HEIGHT = 0
FPS = 60
grid = []

# Variables to track dragging
dragging = False
dragged_cell = None
original_pos = None

screen = py.display.set_mode((WIDTH, HEIGHT))

clock = py.time.Clock()


IMAGE_DIR = pathlib.Path(__file__).parent/'images'

cell_images = {
    1: py.image.load(IMAGE_DIR / 'Wall.png').convert_alpha(),
    2: py.image.load(IMAGE_DIR / 'Blank4.png').convert_alpha(),
    3: py.image.load(IMAGE_DIR / 'BlankX.png').convert_alpha(),
    4: py.image.load(IMAGE_DIR / 'BlankY.png').convert_alpha(),
    5: py.image.load(IMAGE_DIR / 'PusherUp.png').convert_alpha(),
    6: py.image.load(IMAGE_DIR / 'PusherDown.png').convert_alpha(),
    7: py.image.load(IMAGE_DIR / 'PusherLeft.png').convert_alpha(),
    8: py.image.load(IMAGE_DIR / 'PusherRight.png').convert_alpha(),
    9: py.image.load(IMAGE_DIR / 'GeneratorUp.png').convert_alpha(),
    10: py.image.load(IMAGE_DIR / 'GeneratorDown.png').convert_alpha(),
    11: py.image.load(IMAGE_DIR / 'GeneratorLeft.png').convert_alpha(),
    12: py.image.load(IMAGE_DIR / 'GeneratorRight.png').convert_alpha(),
    13: py.image.load(IMAGE_DIR / 'RotatorClockwise.png').convert_alpha(),
    14: py.image.load(IMAGE_DIR / 'RotatorAnticlockwise.png').convert_alpha(),
    15: py.image.load(IMAGE_DIR / 'Enemy.png').convert_alpha()
}


start_img = py.image.load(IMAGE_DIR / 'Start.png').convert_alpha()
stop_img = py.image.load(IMAGE_DIR / 'Stop.png').convert_alpha()
step_img = py.image.load(IMAGE_DIR / 'Step.png').convert_alpha()
restart_img = py.image.load(IMAGE_DIR / 'Restart.png').convert_alpha()
back_img = py.image.load(IMAGE_DIR / 'Back.png').convert_alpha()
next_img = py.image.load(IMAGE_DIR / 'Next.png').convert_alpha()
play_img = py.image.load(IMAGE_DIR / 'Play.png').convert_alpha()
quit_img = py.image.load(IMAGE_DIR / 'Quit.png').convert_alpha()
help_img = py.image.load(IMAGE_DIR / 'Help.png').convert_alpha()
level1_img = py.image.load(IMAGE_DIR / 'Level1.png').convert_alpha()
level2_img = py.image.load(IMAGE_DIR / 'Level2.png').convert_alpha()
level3_img = py.image.load(IMAGE_DIR / 'Level3.png').convert_alpha()
completedlevel1_img = py.image.load(IMAGE_DIR / 'completedlevel1.png').convert_alpha()
completedlevel2_img = py.image.load(IMAGE_DIR / 'completedlevel2.png').convert_alpha()
completedlevel3_img = py.image.load(IMAGE_DIR / 'completedlevel3.png').convert_alpha()
resetprogress_img = py.image.load(IMAGE_DIR / 'Resetprogress.png').convert_alpha()
title_img = py.transform.scale(py.image.load(IMAGE_DIR / 'Title.png').convert_alpha(), (536, 56))
levels_img = py.transform.scale(py.image.load(IMAGE_DIR / 'Levels.png').convert_alpha(), (280, 56))
lock_img = py.transform.scale(py.image.load(IMAGE_DIR / 'lock.png').convert_alpha(), (90, 90))
helptitle_img = py.transform.scale(py.image.load(IMAGE_DIR / 'Helptitle.png').convert_alpha(), (184, 56))

py.display.set_caption('Cell Machine')
py.display.set_icon(cell_images[5])


#Game screen buttons
start_button = button.Button(50, 701, start_img, 5)
stop_button = button.Button(50, 701, stop_img, 5)
step_button = button.Button(150, 701, step_img, 5)
restart_button = button.Button(250, 701, restart_img, 5)
back_button = button.Button(50, 25, back_img, 3)
next_button = button.Button(600, 701, next_img, 5)

#Level screen buttons
level1_button = button.Button(155, 355, level1_img, 6)
level2_button = button.Button(355, 355, level2_img, 6)
level3_button = button.Button(555, 355, level3_img, 6)
completedlevel1_button = button.Button(155, 355, completedlevel1_img, 6)
completedlevel2_button = button.Button(355, 355, completedlevel2_img, 6)
completedlevel3_button = button.Button(555, 355, completedlevel3_img, 6)
resetprogress_button = button.Button(347, 700, resetprogress_img, 2)

#Menu screen buttons
play_button = button.Button(284, 250, play_img, 8)
quit_button = button.Button(342, 375, quit_img, 4)
help_button = button.Button(663, 736, help_img, 3)


def is_within_valid_area(col, row, level): # Used in functionality of editing the grid to determine the area that can be edited
    valid_area_top_left = load_value('levels.txt', level)[0]
    valid_area_bottom_right = load_value('levels.txt', level)[1]
    return (
        valid_area_top_left[0] <= col <= valid_area_bottom_right[0] and
        valid_area_top_left[1] <= row <= valid_area_bottom_right[1]
    )


def draw_grid(level, dragging=False, dragged_cell=None, mouse_pos=None): #Draws the entire game screen except for the buttons
    global grid, TILE_SIZE, GRID_HEIGHT, GRID_WIDTH
    valid_area_top_left = load_value('levels.txt', level)[0]
    valid_area_bottom_right = load_value('levels.txt', level)[1]
    #Scale images to fit the size of the grid
    for i in cell_images:
        cell_images[i] = py.transform.scale(cell_images[i], (TILE_SIZE, TILE_SIZE))


    py.draw.rect(screen, (48, 48, 48), (valid_area_top_left[0] * TILE_SIZE, valid_area_top_left[1] * TILE_SIZE, 
    (valid_area_bottom_right[0] - valid_area_top_left[0] + 1) * TILE_SIZE, (valid_area_bottom_right[1] - valid_area_top_left[1] + 1) * TILE_SIZE))
    
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            cell_id = grid[row][col]

            if cell_id in cell_images:
                screen.blit(cell_images[cell_id], (col * TILE_SIZE, row * TILE_SIZE))

    for row in range(GRID_HEIGHT):
        py.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        py.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    
    if dragging and dragged_cell is not None:
        screen.blit(dragged_cell, (mouse_pos[0] - TILE_SIZE // 2, mouse_pos[1] - TILE_SIZE // 2))
    

def cell_properties(cell_id): #Stores the properties of the different cell types
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
    elif cell_id in (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):  # Every Other Cell
        return {'movable_x': True, 'movable_y': True}
    else:  # Default case for undefined cell_ids
        return {}


def adjust_grid(): #Handles the execution of the functionality to update the grid
    global grid
    new_grid = [row[:] for row in grid]  #to store the locations of the enemy cells

    for ID in range(5, 15):
        if ID >= 5 and ID <= 8:
            grid = pusher(ID)
        elif ID >= 9 and ID <= 12:
            grid = generator(ID)
        elif ID == 13 or ID == 14:
            grid = rotator(ID)
    
    grid = enemy(new_grid)
        

    return grid

def pusher(ID): #Functionality for pusher cells
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
    if sy == -1 or sx == -1:
        row_range = range(GRID_HEIGHT)
        col_range = range(GRID_WIDTH)
    elif sy == 1:
        row_range = range(GRID_HEIGHT - 1, -1, -1)
        col_range = range(GRID_WIDTH)
    elif sx == 1:
        row_range = range(GRID_HEIGHT)
        col_range = range(GRID_WIDTH - 1, -1, -1)

    for row in row_range:
        for col in col_range:
            cell_id = grid[row][col]
            if cell_id == ID:
                run = True
                y = 0
                list_cell = []

                while run:
                    check_id = grid[row + y*sy][col + y*sx]

                    if check_id == 0 or check_id == 15:
                        run = False
                        grid[row + y*sy][col + y*sx] = 0
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

    return temp_grid

def generator(ID): #Functionality for generator cells
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
            if grid[row][col] == ID and (grid[row - sy][col - sx] > 1):
                run = True
                generate = True
                y = 1
                list_cell = []

                while run:
                    check_id = grid[row + y*sy][col + y*sx]

                    if check_id == 0 or check_id == 15:
                        run = False
                        grid[row + y*sy][col + y*sx] = 0
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

    return temp_grid  

def rotator(ID): #Functionality for rotator cells
    global grid
    temp_grid = [row[:] for row in grid]  # Create a new grid to avoid modifying the original during iteration

    rotation_mapping_clockwise = {
                    0:0, # Empty
                    1:1, # Wall
                    2:2, # Blank
                    13:13, # Rotator
                    14:14, # Rotator
                    15:15, # Enemy
                    
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
                    15:15, # Enemy
                    
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
            if cell_id == ID:
                temp_grid[row - 1][col] = rotation_mapping[temp_grid[row - 1][col]]
                temp_grid[row + 1][col] = rotation_mapping[temp_grid[row + 1][col]]
                temp_grid[row][col - 1] = rotation_mapping[temp_grid[row][col - 1]]
                temp_grid[row][col + 1] = rotation_mapping[temp_grid[row][col + 1]]
    return temp_grid

def enemy(new_grid): #Functionality for enemy cells

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if new_grid[row][col] == 15:
                if grid[row][col] != 0 and grid[row][col] != 15:
                    grid[row][col] = 0

    return grid


def save_value(input_value): #Handles storeing player progress
    with open('progress.txt', 'w') as f:
        f.write(input_value)

def load_value(file_name, index): #Handles retrieveing player progress and the levels
    with open(file_name, 'r') as f:
        read = ast.literal_eval(f.read())
        if index != None:
            read = read[index]
    return read

def draw_text(text, y): #Handles the display of text on the help screen
    font = py.font.SysFont('Pixeloid Sans', 20)
    img = font.render(text, True, (255, 255, 255))
    text_rect = img.get_rect(center=(400, y))
    screen.blit(img, text_rect)


def game(level): #The game window where all the gameplay happens
    global grid, dragging, dragged_cell, original_pos, TILE_SIZE, GRID_HEIGHT, GRID_WIDTH, WIDTH, HEIGHT
    window_running = True
    sim_running = False
    editing = True
    TILE_SIZE = load_value('levels.txt', level)[2]
    GRID_WIDTH = WIDTH // TILE_SIZE
    GRID_HEIGHT = HEIGHT // TILE_SIZE
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    grid = load_value('levels.txt', level)[3]
    count = 0
    update_freq = FPS * 0.4

    while window_running:
        clock.tick(FPS)

        if sim_running:
            count += 1

        if count >= update_freq:
            count = 0
            grid = adjust_grid()

        screen.fill(BLACK)
        draw_grid(level, dragging, dragged_cell, py.mouse.get_pos())
        #Drawing the buttons to the screen and handling their functionality
        if sim_running:
            if stop_button.draw(screen):
                sim_running = False
        else:
            if start_button.draw(screen):
                sim_running = True
                if editing:
                    edited_grid = [row[:] for row in grid]
                    editing = False
        
        
        if step_button.draw(screen):
            sim_running = False
            if editing:
                edited_grid = [row[:] for row in grid]
                editing = False
            grid = adjust_grid()
        if not editing:
            if restart_button.draw(screen):
                sim_running = False
                grid = [row[:] for row in edited_grid]
                editing = True
        if help_button.draw(screen):
            sim_running = False
            help()
        if back_button.draw(screen):
            return

        if not any(15 in row for row in grid):
            progress = load_value('progress.txt', None)
            progress[level] = 2
            if level + 1 in progress and progress[level + 1] == 0:
                progress[level + 1] = 1
            save_value(str(progress))
            if next_button.draw(screen):
                return level + 1

        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                window_running = False
                py.quit()
                sys.exit()
            #Functionality for editing the grid
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                col = mouse_x // TILE_SIZE
                row = mouse_y // TILE_SIZE
                
                if 0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT and is_within_valid_area(col, row, level) and editing:
                    cell_id = grid[row][col]
                    if cell_id != 0:
                        dragging = True
                        dragged_cell = cell_images[cell_id]
                        original_pos = (col, row)
                        grid[row][col] = 0 

            if event.type == py.MOUSEBUTTONUP and event.button == 1:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // TILE_SIZE
                    row = mouse_y // TILE_SIZE
                    
                    if 0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT and is_within_valid_area(col, row, level) and editing:
                        grid[original_pos[1]][original_pos[0]], grid[row][col] = grid[row][col], cell_id
                    else:
                        grid[original_pos[1]][original_pos[0]] = cell_id

                    dragging = False
                    dragged_cell = None
                    original_pos = None

            if event.type == py.MOUSEMOTION and dragging:
                mouse_x, mouse_y = event.pos
                col = mouse_x // TILE_SIZE
                row = mouse_y // TILE_SIZE

                if not (0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT and is_within_valid_area(col, row, level)):
                    grid[original_pos[1]][original_pos[0]] = cell_id
                    dragging = False
                    dragged_cell = None
                    original_pos = None



def level_select(): #The level select screen
    window_running = True
    next = 0
    
    while window_running:
        clock.tick(FPS)
        levels = load_value('progress.txt', None) #Retrieves which levels are locked, unlocked or completed
        
        screen.fill(BLACK)
        screen.blit(levels_img, (260, 25))
        #Drawing the buttons to the screen and handling their functionality
        if back_button.draw(screen):
            return
        if levels[1] == 1:
            if level1_button.draw(screen):
                next = 0
                next = game(1)
        else:
            if completedlevel1_button.draw(screen):
                next = 0
                next = game(1)
        if levels[2] == 0:
            screen.blit(lock_img, (355, 355))
        elif levels[2] == 1:
            if level2_button.draw(screen) or next == 2:
                next = 0
                next = game(2)
        else:
            if completedlevel2_button.draw(screen) or next == 2:
                next = 0
                next = game(2)
        if levels[3] == 0:
            screen.blit(lock_img, (555, 355))
        elif levels[3] == 1:
            if level3_button.draw(screen) or next == 3:
                next = 0
                game(3)
        else:
            if completedlevel3_button.draw(screen) or next == 3:
                next = 0
                game(3)
        if resetprogress_button.draw(screen):
            save_value("{1: 1, 2: 0, 3: 0}")
        py.display.update()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                window_running = False
                py.quit()
                sys.exit()

def help(): #The help screen
    window_running = True
    while window_running:
        clock.tick(FPS)

        screen.fill(BLACK)
        screen.blit(helptitle_img, (308, 25))
        draw_text('Move cells within the highlighted area and then click the play button.', 150)
        draw_text('Once the play button is clicked you cannot move cells yourself.', 175)
        draw_text('The goal is to remove all enemy cells. This is done by moving another', 200)
        draw_text("cell into the same space as an enemy cell. If you don't manage to", 225)
        draw_text('remove all of the enemy cells, you can click the reset button to try', 250)
        draw_text('again. The step button steps through the simulation one step at a time.', 275)
        draw_text('Blue cells push things in front of them in the direction of their arrow.', 350)
        draw_text('Green cells duplicate the cell behind it and place it in front.', 400)
        draw_text('Red cells rotate cells surrounding them in the direction of the arrow.', 450)
        draw_text('Yellow cells can only be moved in the direction of their arrow.', 500)
        if back_button.draw(screen): #Draws the back button and handles its functionality
            return
        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                window_running = False
                py.quit()
                sys.exit()


def menu(): #The menu screen
    window_running = True
    while window_running:
        clock.tick(FPS)
        
        screen.fill(BLACK)
        screen.blit(title_img, (132, 100))
        #Drawing the buttons to the screen and handling their functionality
        if play_button.draw(screen):
            level_select()
        if quit_button.draw(screen):
            window_running = False
        if help_button.draw(screen):
            help()
        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                window_running = False
                py.quit()
                sys.exit()
        



if __name__ == "__main__": #runs the menu subroutine on opening
    menu()