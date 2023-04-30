import pygame
import keyboard
import time
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Contra')
clock = pygame.time.Clock()
background_surface = pygame.Surface([1200, 600])
background_surface.fill((77, 75, 118))

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


def createTrunk(height):
    for i in range(height):
        trunk_img = pygame.image.load('Forest_tiles\Tree_dark\image0.png')
        y_cordinate = ground_levelY - i * 50
        trunk_rect = trunk_img.get_rect(bottomleft=(300, y_cordinate))
        screen.blit(trunk_img, trunk_rect)
    return trunk_rect.bottomleft


def populate(row, slotNo, startCord):
    if slotNo == 0:
        if row == 0:
            img = pygame.image.load("Forest_tiles\Tree_Light/bottom_left.png")
        if row == 1:
            img = pygame.image.load('Forest_tiles\Tree_Light\center.png')
        if row == 2:
            img = pygame.image.load('Forest_tiles\Tree_Light/top_left.png')
    else:
        img = pygame.image.load('Forest_tiles\Tree_Light\center.png')
    img_rect = img.get_rect(bottomleft=(startCord[0] - 50 * slotNo, startCord[1]))
    screen.blit(img, img_rect)
    if slotNo > 0:
        startCord = (img_rect.bottomleft[0] - 50, img_rect.bottomleft[1])
        populate(row, slotNo - 1, (img_rect.bottomleft[0] - 50, img_rect.bottomleft[1]))


def createLeaves(width, start_cordinates):
    for row in range(width+1):
        if row == width:
            img = pygame.image.load('Forest_tiles\Tree_Light\mid_top.png')
        else:
            img = pygame.image.load('Forest_tiles\Tree_Light\center.png')
        y_coord = start_cordinates[1] - 50 * row
        img_rect = img.get_rect(bottomleft=(start_cordinates[0], y_coord))
        if row < width:
            slotNo = (width-1)//2
            populate(row, slotNo, img_rect.bottomleft)
        screen.blit(img, img_rect)


# this still needs a lot of work
def createTree(treeHeight, leafWidth):
    createLeaves(leafWidth, createTrunk(treeHeight))

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
        enemy_rect.bottom = 100
    enemy_Gravity()


while True:
    screen.blit(background_surface, (0, 0))
    maxColumns = 50
    maxRows = 10
    createGround(maxRows, maxColumns)
    createTree(5, 3)
    player_img = player_Gravity(gravity, player_rect)
    moveEnemy()

    if keyboard.is_pressed('right'):
        if currentIndex == 8:
            currentIndex = 0
        player_img = playerRunForward()
    elif keyboard.is_pressed('left'):
        player_img = playerRunBack()
    elif keyboard.is_pressed('up'):
        player_rect.bottom -= 30
    else:
        player_img = pygame.image.load('player_character\Player_Stand\image0-rb.png')

    screen.blit(player_img, player_rect)
    screen.blit(enemy_img, enemy_rect)
    pygame.display.update()
    clock.tick(60)
