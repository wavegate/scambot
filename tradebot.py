import pyautogui
from tkinter import Tk
import pyperclip
import re

#pyautogui.PAUSE = .5
pyautogui.FAILSAFE = True
#pyautogui.MINIMUM_DURATION = 0.001
pyautogui.PAUSE = 0.05
#pyautogui.MINIMUM_SLEEP = 0.001

def copyMessage():
	text = pyperclip.paste()
	match = re.search("@(\w+).+for (\w+) (\w+)", text)
	charName = match.group(1)
	amount = int(match.group(2))
	currency = match.group(3)

def clickIn():
	pyautogui.moveTo(960,480)
	pyautogui.click()

def waitFor(image):
	loc = pyautogui.locateOnScreen(image)
	while loc == None:
		print("waiting...")
		loc = pyautogui.locateOnScreen(image)
		if loc != None:
			return loc
	
def click(image):
	loc = pyautogui.locateOnScreen(image)
	pyautogui.moveTo(loc[0], loc[1])
	pyautogui.click()

def message(text):
	pyperclip.copy(text)
	pyautogui.press('enter')
	pyautogui.hotkey('ctrl', 'a')
	pyautogui.hotkey('ctrl', 'v')
	pyautogui.press('enter')

def withdraw(amount, currency):
	pyautogui.moveTo(960, 480)
	pyautogui.click()
	#click('images/moneysymbol.png')
	loc = pyautogui.locateOnScreen('images/chaos.png')
	while loc == None:
		print("waiting...")
		loc = pyautogui.locateOnScreen('images/chaos.png')
		if loc != None:
			break
	pyautogui.moveTo(loc[0], loc[1])
	withdrawChaos(amount)
	pyautogui.press('escape')

def withdrawChaos(amount):
	pyautogui.keyDown('ctrl')
	if amount >= 10:
		pyautogui.click()
		withdrawChaos(amount-10)
	pyautogui.keyUp('ctrl')
	if amount < 10:
		pyautogui.keyDown('shift')
		pyautogui.click()
		pyautogui.keyUp('shift')
		if amount > 1:
			loc = pyautogui.locateOnScreen('images/amtright.png')
			pyautogui.moveTo(loc[0], loc[1])
			pyautogui.click(clicks=amount-1)
		click('images/amtaccept.png')
		pyautogui.moveTo(1890, 820)
		pyautogui.click()

def putInTrade():
	for i in range(1290, 1890, 54):
		pyautogui.moveTo(i, 610)
		pyautogui.keyDown('ctrl')
		pyautogui.click()
		for i in range(4):
			pyautogui.moveRel(0, 54)
			pyautogui.click()
		pyautogui.keyUp('ctrl')

def acceptTrade():
	loc = pyautogui.locateOnScreen('images/tradeaccept.png')
	print(loc)
	while (loc == None):
		for i in range(330, 930, 54):
			pyautogui.moveTo(i, 230)
			for i in range(4):
				pyautogui.moveRel(0, 54)
		loc = pyautogui.locateOnScreen('images/tradeaccept.png')
	pyautogui.moveTo(loc[0], loc[1])
	pyautogui.click()

def makeTrade():
	copyMessage()
	clickIn()
	#withdraw(amount, 'blue')
	message(text)
	waitFor('images/accept.png')
	click('images/accept.png')
	message('/hideout ' + charName)
	waitFor('images/accept.png')
	click('images/accept.png')
	putInTrade()

makeTrade()
#acceptTrade()

#message('/hideout ' + charName)
#message('/tradewith ' + charName)
#add currency
#hitaccept
#message('/hideout')


"""
clipboard
click into game
enter
ctrl-A
ctrl-V
enter
accept party invite
hideout
accept trade
offer trade
accept
return to hideout

######## Main #########
"""