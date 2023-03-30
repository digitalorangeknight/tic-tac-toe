import pygame


# Grid groups: [A] Actual grid [B] LMB hold animation
class GridClass(pygame.sprite.Sprite):  # Grid group [A]
    def __init__(self):
        super().__init__()
        for x in range(0, background.get_width(), square_size):
            for y in range(0, background.get_height(), square_size):
                block_rect = pygame.Rect(x, y, square_size, square_size)
                pygame.draw.rect(background, "black", block_rect, 1)


class GridCoordinate(pygame.sprite.Sprite):  # Grid group [B]
    def __init__(self):
        (x, y) = pygame.mouse.get_pos()
        self.cx = (x // square_size) * square_size
        self.cy = (y // square_size) * square_size
        self.square = pygame.Rect(self.cx, self.cy, square_size, square_size)

    def draw(self, surface):  # Creates a grey square with mouse position and LMB hold/click
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(surface, "grey", self.square)


# Object groups: [A] Object loader and [B] Object creator/determiner
class ObjectClass(pygame.sprite.Sprite):  # Object group [A]
    def __init__(self, img):
        super().__init__()
        self.image = img


def createObject(pos_storage, possible_pos):  # Object group [B]: Unique mouse position -> X/O in array
    (x, y) = pygame.mouse.get_pos()
    cx = (x // square_size) * square_size
    cy = (y // square_size) * square_size

    if (cx, cy) not in pos_storage and gameEnd[0] is not True:  # Unique object coordinates + stops game after win

        if len(pos_storage) % 2 == 0:  # Converts coordinate into shapes based on even/odd index
            shape = 'x'
            object_img = x_img
        else:
            shape = 'o'
            object_img = o_img

        index_counter = 0
        for x in possible_pos:
            for y in x:
                if y == (cx, cy):
                    full_grid_list[possible_pos.index(x)][possible_pos[index_counter].index(y)] = shape
            index_counter += 1

        # print(full_grid_list)  # Debug purposes

        a = ObjectClass(object_img)
        a.rect = pygame.Rect(cx, cy, square_size, square_size)

        sprite_group.add(a)

        pos_storage.append((cx, cy))
        # print(pos_storage)  # Debug purposes - visual representation in array

        checkWin(shape, len(pos_storage))


# End-screen groups: [A] Win determiner [B] End-screen
def checkWin(shape, object_number):  # [A]
    game_end = False
    if full_grid_list.count('') < 8:  # Check only when three objects are inside the grid
        for x in range(3):
            if full_grid_list[x][0] == full_grid_list[x][1] == full_grid_list[x][2] != '':  # Row victory
                game_end = True
            if full_grid_list[0][x] == full_grid_list[1][x] == full_grid_list[2][x] != '':  # Column victory
                game_end = True
        if full_grid_list[0][0] == full_grid_list[1][1] == full_grid_list[2][2] != '':  # Forward diagonal victory
            game_end = True
        elif full_grid_list[2][0] == full_grid_list[1][1] == full_grid_list[0][2] != '':  # Backward diagonal victory
            game_end = True

    if game_end:
        msg = f'{shape.upper()} Wins!'
        endScreen(msg)

    elif object_number == 9:
        msg = 'Draw!'
        endScreen(msg)


def endScreen(msg):  # [B]
    print(msg)
    timer = 400  # Determines duration of endScreen
    delay = 1000
    while delay != 0:
        delay -= 1
    while timer > 0:
        text_surface = text_font.render(msg, True, 'black')

        text_rect = text_surface.get_rect()
        text_rect.center = (background.get_height() // 2, background.get_width() // 2)

        gameEnd[0] = True

        background.blit(text_surface, text_rect)
        pygame.display.update()

        timer -= 1


# Initialization
pygame.init()
pygame.display.set_caption('Tic Tac Toe')  # Game title
pygame.display.set_icon(pygame.image.load('assets/thumbnail.png'))  # Game icon
background = pygame.display.set_mode((400, 400))  # Game window size - change pos_data if it is changed

fps = 60
clock = pygame.time.Clock()
running = True

# Sprite variables
sprite_group = pygame.sprite.Group()
square_size = background.get_width() // 3

# Object variables
x_img = pygame.transform.scale(pygame.image.load('assets/x.png'), (square_size, square_size))
o_img = pygame.transform.scale(pygame.image.load('assets/o.png'), (square_size, square_size))
text_font = pygame.font.Font('freesansbold.ttf', 72)

gameEnd = [False]
pos_input = []  # Clear this if adding an option to restart game
pos_data = [[(0, 0), (133, 0), (266, 0)], [(0, 133), (133, 133), (266, 133)], [(0, 266), (133, 266), (266, 266)]]
full_grid_list = [['', '', ''], ['', '', ''], ['', '', '']]  # Clear this if adding an option to restart game

while running:
    background.fill("white")  # White background

    grid_animation = GridCoordinate()
    grid_animation.draw(background)

    GridClass()
    sprite_group.draw(background)
    sprite_group.update()

    for event in pygame.event.get():
        mouse = pygame.mouse.get_pressed(num_buttons=3)
        key = pygame

        if event.type == pygame.QUIT:  # Exit game
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and mouse[0]:  # Create object onclick where the cursor is
            createObject(pos_input, pos_data)

    pygame.display.flip()

    # Game set to 60 FPS
    clock.tick(fps)

pygame.quit()
