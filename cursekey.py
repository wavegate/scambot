import keyboard #Using module keyboard
import pyautogui

while True:#making a loop
    try: #used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('w'):#if key 'q' is pressed 
          pyautogui.moveTo(960,200)
          keyboard.press("e")
          pass
        if keyboard.is_pressed('a'):#if key 'q' is pressed 
          pyautogui.moveTo(620,540)
          keyboard.press("e")
        if keyboard.is_pressed('s'):#if key 'q' is pressed 
          pyautogui.moveTo(960,750)
          keyboard.press("e")
        if keyboard.is_pressed('d'):#if key 'q' is pressed 
          pyautogui.moveTo(1300,540)
          keyboard.press("e")
            #break#finishing the loop
        else:
          pass
    except:
        break #if user pressed a key other than the given key the loop will break