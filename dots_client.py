#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
from queue import Queue

HOST = "128.237.186.74" # put your IP address here if playing on multiple computers
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

def doodle():
  while (serverMsg.qsize() > 0):
    msg = serverMsg.get(False)
    try:
      print("received: ", msg, "\n")
    except:
      print("failed")
    serverMsg.task_done()

while(True):
  doodle()
  server.send("test 3 3 3\n".encode())