import socket
import pyautogui 
import threading
SERVER = "irc.twitch.tv"
PORT = 6667
PASS = "" # You oauth key https://twitchapps.com/tmi/
BOT = " Bot"
CHANNEL = "" # Your channel name
OWNER = "" # Your channel name again
message = ""

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" +
            "NICK" + BOT + "\n" +
            "JOIN #" + CHANNEL + "\n").encode())

def gamecontrol():
    global message
    while True:

        if "up" in message.lower():
            pyautogui.keyDown('w')
            message = ""
            pyautogui.keyUp('w')

        elif "down" in message.lower():
            pyautogui.keyDown('s')
            message = ""
            pyautogui.keyUp('s')

        elif "right" in message.lower():
            pyautogui.keyDown('d')
            message = ""
            pyautogui.keyUp('d')

        elif "left" in message.lower():
            pyautogui.keyDown('a')
            message = ""
            pyautogui.keyUp('a')

        # A button
        elif "abut" in message.lower():
            pyautogui.keyDown('a')
            message = ""
            pyautogui.keyUp('a')

        # B button
        elif "bbut" in message.lower():
            pyautogui.keyDown('b')
            message = ""
            pyautogui.keyUp('b')

        # Start button
        elif "start" in message.lower():
            pyautogui.keyDown('enter')
            message = ""
            pyautogui.keyUp('enter')
        else:
            pass

def twitch():
    def joinchat():
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = loadingComplete(line)

    def loadingComplete(line):
        if ("End of /NAMES list" in line):
            print("Bot has joined " + CHANNEL + "'s Channel!")
            sendMessage(irc, "Chat Room Joined")
            return False
        else:
            print("test")
            return True
    def sendMessage(irc, message):
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        irc.send((messageTemp + "\n").encode())

    def getUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!" ,1)[0]
        return user

    def getMessage(line):
        global message
        try:
            message = (line.split(":",2))[2]
        except:
            message = ""
        return message
    def Console (line):
        if "PRIVMSG" in line:
            return False
        else:
            return True

    joinchat()

    while True: 
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue 

            elif "PING" in line and Console(line):
                msgg = "PONG rmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                print(msgg)
                continue

            else:
                print(line)
                user = getUser(line)
                message = getMessage(line)
                print(user + " : " + message)
if __name__ =='__main__':
    t1 = threading.Thread(target = twitch)
    t1. start()
    t2 = threading.Thread(target = gamecontrol)
    t2. start()