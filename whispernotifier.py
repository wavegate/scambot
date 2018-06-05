import time
from fbchat import Client
from fbchat.models import *
from pushbullet import Pushbullet
import getpass
import winsound

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
	p = getpass.getpass()
	client = Client('dingospetleg@gmail.com', p)
	pb = Pushbullet("o.Lx81UVSxfaCu3EXRfrhi2U4HC7EuvVQK")
	logfile = open("C:\Program Files (x86)\Grinding Gear Games\Path of Exile\logs\Client.txt","r")
	loglines = follow(logfile)
	for line in loglines:
		if "From" in line:
			print(line)
			#winsound.Beep(1000, 500)
			pb.push_note("Title", line)
			user = client.searchForUsers("Frank Lee")[0]
			client.send(Message(text=line), thread_id=user.uid, thread_type=ThreadType.USER)
	client.logout()