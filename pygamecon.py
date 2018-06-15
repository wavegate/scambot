import pygame
import pyautogui
"""
pygame.init()
#screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
finished = False
isKeyPressed = False
while not finished:
    for event in pygame.event.get():
        print(event)
        if isKeyPressed:
            pyautogui.moveTo(620,540)
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                isKeyPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                isKeyPressed = False
                #Perform action (here) when 'w' is unpressed 
        #pygame.display.flip()
        clock.tick(60)
pygame.quit()
"""

import sys

pygame.display.init()
screen = pygame.display.set_mode((320,240))
pygame.event.set_grab(True)
index =0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print("{0}: You pressed {1:c}".format ( index , event.key ))
                pyautogui.moveTo(620,540)

        index+=1