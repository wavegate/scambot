from fbchat import log, Client
from fbchat.models import *
import getpass
import autogui
import pyautogui
import pyperclip
import re
import time
import random

# Subclass fbchat.Client and override required methods
class EchoBot(Client):

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(thread_id, message_object.uid)
		self.markAsRead(thread_id)

		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
		return_message = message_object.text

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
		waitForHideout()
		message("/tradewith {}".format(tradename))
		whispernotifier.waitforhideout(tradename)
		#input()
		#checkoutput()
		#accept()
		#leaveparty()

	def message(message):
		pyperclip.copy(message)
		pyautogui.press('enter')
		time.sleep(random.uniform(0.3, 0.6))
		pyautogui.hotkey('ctrl', 'a')
		time.sleep(random.uniform(0.3, 0.6))
		pyautogui.hotkey('ctrl', 'v')
		time.sleep(random.uniform(0.3, 0.6))
		pyautogui.press('enter')

import whispernotifier
p = getpass.getpass()
client = EchoBot('dingospetleg@gmail.com', p)
client.listen()