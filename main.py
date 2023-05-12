import pygame
import keyboard

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Contra')
clock = pygame.time.Clock()
background_surface = pygame.Surface([1200, 600])
background_surface.fill((77, 75, 118))

class bulletRight(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('player_character/bullet.png')
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    def update(self):
        self.rect.x += 15
        if self.rect.x > screen.get_width():
            del self
class bulletLeft(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('player_character/bullet.png')
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    def update(self):
        self.rect.x -= 15
        if self.rect.x < 0:
            del self
bullet_group = pygame.sprite.Group()

global player_img
player_img = pygame.image.load('player_character\Player_Stand\image0-rb.png')
global player_rect
player_rect = player_img.get_rect(bottomleft=(1, 455))
ground_surface = pygame.image.load('DJ_Art\Grass0.png')
ground_levelY = 455
global enemy_img
enemy_img = pygame.image.load('Enemy_character\Enemy_Stand\image_backward.png')
global enemy_rect
enemy_rect = enemy_img.get_rect(bottomleft=(200, 455))
currentIndex = 0
def playerRunForward():
    global currentIndex
    player_img = pygame.image.load(f'player_character\Player_Run\Forward\image{currentIndex}.png')
    player_rect.right += 5
    currentIndex += 1
    if currentIndex == 8:
        currentIndex = 0
    return player_img
currentIndex_back = 0
def playerRunBack():
    global currentIndex_back
    player_img = pygame.image.load(f'player_character\Player_Run\Backward\image{currentIndex_back}.png')
    player_rect.left -= 5
    currentIndex_back += 1
    if currentIndex_back == 8:
        currentIndex_back = 0
    return player_img
global gravity
gravity = 5
forwardSpin_Index = 0
def player_Gravity(gravity, player_rect):
    global forwardSpin_Index
    global  player_img
    if (player_rect.bottom < ground_levelY):
        player_img = pygame.image.load(f'player_character\Player_Forward_Spin\image{forwardSpin_Index}.png')
        forwardSpin_Index += 1
        if forwardSpin_Index == 4:
            forwardSpin_Index = 0

        if player_rect.bottom + gravity >= ground_levelY:
            player_rect.bottom = ground_levelY
            gravity = 5
        player_rect.bottom += gravity
        gravity += 5
    return player_img
def createGround(maxRows, maxColumns):
    for row in range(maxRows):
        for col in range(maxColumns):
            if row == 0:
                if 0 < col < maxColumns - 1:
                    img = pygame.image.load(f"DJ_Art\Grass{1}.png")
                else:
                    if col == 0:
                        img = pygame.image.load(f"DJ_Art\Grass{0}.png")
                    if col == maxColumns - 1:
                        img = pygame.image.load(f"DJ_Art\Grass{2}.png")
            else:
                img = pygame.image.load(f"DJ_Art\Dirt_1.png")
            ground_origin = [0, 450]
            temp_list = [ground_origin[0] + 16 * col, ground_origin[1] + 16 * row]
            screen.blit(img, tuple(temp_list))
def createTrunk(height, x_cord):
    for i in range(height):
        trunk_img = pygame.image.load('Forest_tiles\Tree_Light\image0.png')
        y_cordinate = ground_levelY - i * trunk_img.get_height()
        trunk_rect = trunk_img.get_rect(bottomleft=(x_cord, y_cordinate))
        screen.blit(trunk_img, trunk_rect)
    return trunk_rect.topleft
def createLeaves(width, start_cordinates):
    slots_left = slots_right = (width-1)//2
    start_cordinates = list(start_cordinates)
    start_cordinates[0] = start_cordinates[0] - slots_left*50
    for col in range(slots_left):
        for row in range(width):
            if col == 0:
                if row == 0:
                    img = pygame.image.load('Forest_tiles\Tree_Light/bottom_left.png')
                if row == width-1:
                    img = pygame.image.load('Forest_tiles\Tree_Light/top_left.png')
                else:
                    img = pygame.image.load('Forest_tiles\Tree_Light\center.png')
            else:
                img = pygame.image.load('Forest_tiles\Tree_Light\center.png')

            img_rect = img.get_rect(bottomleft = (start_cordinates))
            screen.blit(img, img_rect)
            start_cordinates[1] -= 50
        start_cordinates[0] += 50
        start_cordinates[1] += width*50

    for i in range(width):
        img = pygame.image.load('Forest_tiles\Tree_Light\center.png')
        img_rect = img.get_rect(bottomleft = (start_cordinates))
        screen.blit(img, img_rect)
        start_cordinates[1] -= 50

    start_cordinates[1] += width*50
    start_cordinates[0] += 50

    for col in range(slots_right):
        for row in range(width):
            if row == 0 and col == slots_right-1:
                img = pygame.image.load('Forest_tiles\Tree_Light/bottom_right.png')
            if row == width-1 and col == slots_right-1:
                img = pygame.image.load('Forest_tiles\Tree_Light/top_right.png')
            else:
                img = pygame.image.load('Forest_tiles\Tree_Light\center.png')
            img_rect = img.get_rect(bottomleft =(start_cordinates))
            screen.blit(img, img_rect)
            start_cordinates[1] -= 50
        start_cordinates[0] += 50
        start_cordinates[1] += 50*width
def createTree(treeHeight, leafWidth, x_cord):
    createLeaves(leafWidth, createTrunk(treeHeight, x_cord))
def addForestSprites(x_cord, clusters):
    img1 =pygame.image.load('Playground_Objects/image0.png')
    img1_rect = img1.get_rect(bottomleft = (x_cord, ground_levelY))
    img2 = pygame.image.load('Playground_Objects/image1.png')
    img2_rect = img2.get_rect(bottomleft = (x_cord + 25, ground_levelY))
    img3 = pygame.image.load('Playground_Objects/image2.png')
    img3_rect = img3.get_rect(bottomleft = (x_cord +50, ground_levelY))

    screen.blit(img1, img1_rect)
    screen.blit(img2, img2_rect)
    screen.blit(img3, img3_rect)
    if clusters - 1 > 0:
        addForestSprites(x_cord + 200, clusters -1)
def addOcean():
    start = [0, screen.get_height()]
    while start[0] < screen.get_width():
        img = pygame.image.load('Forest_tiles/Stagnant_Water/image_dark.png')
        img_rect = img.get_rect(bottomleft =(start))
        screen.blit(img, img_rect)
        start[0] += img.get_width()
def addWaterFall(groundColummns, waterFall_height):
    available_Slots = (screen.get_width() - 16*groundColummns)//50 + 1
    start = [16*groundColummns, screen.get_height()-50]
    for col in range(available_Slots):
        for row in range(waterFall_height):
            if col % 3 == 1:
                img = pygame.image.load('Forest_tiles/Waterfall_light/image0.png')
            if col % 3 == 2:
                img = pygame.image.load('Forest_tiles/Waterfall_light/image1.png')
            if col%3 == 0:
                img = pygame.image.load('Forest_tiles/Waterfall_light/image2.png')
            img_rect = img.get_rect(bottomleft = (start))
            screen.blit(img, img_rect)
            if(row == 0):
                cloudy_img = pygame.image.load('Forest_tiles/Waterfall_light/frothDown.png')
                cloudy_img_rect = cloudy_img.get_rect(bottomleft = (start))
                screen.blit(cloudy_img, cloudy_img_rect)
            if(row == waterFall_height-1):
                log_img = pygame.image.load('Forest_tiles/Tree_dark/image14.png')
                log_img_rect = log_img.get_rect(bottomleft = (start[0],start[1]-50))
                screen.blit(log_img, log_img_rect)
            start[1] -= img.get_height()
        start[0] += 49
        start[1] += 50*waterFall_height
def enemy_Gravity():
    global gravity
    if enemy_rect.bottom < ground_levelY:
        if enemy_rect.bottom + gravity >= ground_levelY:
            enemy_rect.bottom = ground_levelY
            gravity = 5
        enemy_rect.bottom += gravity
        gravity += 5
enemyIMG_index = 0
def moveEnemy():
    global enemyIMG_index
    global  enemy_rect
    global enemy_img
    if enemyIMG_index == 8:
        enemyIMG_index = 0
    enemy_img = pygame.image.load(f'Enemy_character\Enemy_Run\image{enemyIMG_index}.png')
    enemyIMG_index += 1
    enemy_rect.right -= 5
    if enemy_rect.right < 0:
        enemy_rect.left = 1200
        enemy_rect.bottom = 275
    if enemy_rect.right<960:
        enemy_Gravity()
def playerShoot(start_coordinates, button):
    img = pygame.image.load('player_character/bullet.png')
    img_rect = img.get_rect(center = (start_coordinates))
    screen.blit(img, img_rect)
    if button == 'left':
        while img_rect.left > 0:
            img_rect.left -= 10
    if button == 'right':
        img_rect.right += 20
while True:
    screen.blit(background_surface, (0, 0))
    maxColumns = 60
    maxRows = 10
    createGround(maxRows, maxColumns)
    addWaterFall(maxColumns,5)
    addOcean()
    createTree(5, 3, 200)
    createTree(5,3, 400)
    createTree(5, 3, 600)
    addForestSprites(75,4)
    player_img = player_Gravity(gravity, player_rect)
    moveEnemy()

    if keyboard.is_pressed('right'):
        if currentIndex == 8:
            currentIndex = 0
        player_img = playerRunForward()
        if keyboard.is_pressed('s'):
            bullet_group.add(bulletRight(player_rect.midright[0], player_rect.midright[1]))
    elif keyboard.is_pressed('left'):
        player_img = playerRunBack()
        if keyboard.is_pressed('s'):
            bullet_group.add(bulletLeft(player_rect.midleft[0], player_rect.midleft[1]))
    elif keyboard.is_pressed('up'):
        player_rect.bottom -= 30
    else:
        player_img = pygame.image.load('player_character\Player_Stand\image0-rb.png')
        if keyboard.is_pressed('s'):
            bullet_group.add(bulletRight(player_rect.midright[0], player_rect.midright[1]))

    screen.blit(player_img, player_rect)
    screen.blit(enemy_img, enemy_rect)
    bullet_group.draw(screen)
    bullet_group.update()
    pygame.display.update()
    clock.tick(60)
