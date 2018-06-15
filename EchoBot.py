from fbchat import log, Client
from fbchat.models import *
import getpass
import autogui
import pyautogui
import pyperclip
import re
import time
import random
import templatematch
import whispernotifier

# Subclass fbchat.Client and override required methods
class EchoBot(Client):

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(thread_id, message_object.uid)
		self.markAsRead(thread_id)

		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
		return_message = message_object.text
		print(return_message)
		# If you're not the author, echo
		if author_id != self.uid:
			autogui.switchtopoe()
			message(return_message)
		#self.send(Message(text = return_message), thread_id=thread_id, thread_type=thread_type)

		#name = re.search("@(\w+):(.+)", return_message).group(1)
		#message = re.search("@(\w+):(.+)", return_message).group(2)
		#return_message = "@{}: {}".format(name, message)

def makeTrade(input, output, tradename):
	message("/invite {}".format(tradename))
	whispernotifier.waitforhideout(tradename)
	message("/tradewith {}".format(tradename))
	#openstash()
	requestoraccepttrade()
	#input()
	#checkoutput()
	#accept()
	#leaveparty()

def requestoracceptrade():
	pyautogui.moveTo(templatematch.locImage("tradeaccept", 0.4))
	time.sleep(random.uniform(1, 2))
	pyautogui.click()

def message(message):
		pyperclip.copy(message)
		pyautogui.press('enter')
		time.sleep(random.uniform(0.3, 0.6))
		pyautogui.hotkey('ctrl', 'a')
		time.sleep(random.uniform(0.3, 0.6))
		pyautogui.hotkey('ctrl', 'v')
		time.sleep(random.uniform(0.3, 0.6))
		pyautogui.press('enter')

def openstash():
	#autogui.switchtopoe()
	pyautogui.moveTo(templatematch.locImage("stash", 0.4))
	time.sleep(random.uniform(1, 2))
	pyautogui.click()
	withdraw(78, "chaos")

def withdraw(amount, currency):
	#click('images/moneysymbol.png')
	pyautogui.moveTo(templatematch.locImage("chaos", 0.6))
	withdrawChaos(amount)
	pyautogui.press('escape')

def click(image):
	pyautogui.moveTo(templatematch.locImage(image, 0.95))
	pyautogui.click()

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
			pyautogui.moveTo(templatematch.locImage("amtright", 0.95))
			pyautogui.click(clicks=amount-1)
		click('amtaccept')
		pyautogui.moveTo(1890, 820)
		pyautogui.click()

autogui.switchtopoe()
makeTrade(1, "chaos", "Poos")
#openstash()

import whispernotifier
p = getpass.getpass()
client = EchoBot('dingospetleg@gmail.com', p)
client.listen()