from fbchat import log, Client
from fbchat.models import *
import getpass

# Subclass fbchat.Client and override required methods
class EchoBot(Client):

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(thread_id, message_object.uid)
		self.markAsRead(thread_id)

		#name = client.fetchUserInfo(author_id)[author_id].first_name + " " + 
		name = client.fetchUserInfo(author_id)[author_id].last_name
		print(name)

		if client.fetchUserInfo(client.uid)[client_uid].nickname is not name:
			self.changeNickname(name, client.uid, thread_id, thread_type)

		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
		return_message = message_object.text

		# If you're not the author, echo
		#if author_id != self.uid:
		self.send(Message(text = return_message), thread_id=thread_id, thread_type=thread_type)

p = getpass.getpass()
client = EchoBot('cc.frankee@gmail.com', p)
client.listen()