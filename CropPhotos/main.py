import cv2 as cv
from PIL import Image

image = cv.imread('OpenGunnerForestTiles.png')
player_folder = '\player_character'
cv.waitKey(1) & 0xFF
boxlist = []


def mouseClick(events, x, y, flags, params):
    global boxlist
    if events == cv.EVENT_LBUTTONDOWN:
        boxlist = [x, y, x+50, y+50]                                  #im.crop((left, top, right, bottom))

count = 0
img = Image.open('OpenGunnerForestTiles.png')

while True:
    cv.imshow('Big Image', image)
    cv.setMouseCallback('Big Image', mouseClick)
    cv.waitKey(10)

    if len(boxlist) == 4:
        croppedImage = img.crop(tuple(boxlist))
        croppedImage.save(f'image{count}.png')
        boxlist = []
        count += 1
