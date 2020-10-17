import socket, time, json
import os.path
host = "127.0.0.1"
port = 9090
RUN = True
password = "Annelo123"
mass = 8192


if os.path.isfile("bots.list"):
	with open('bots.list', 'r') as fr:
		clients = json.load(fr)
else:
	with open("bots.list","w+") as list0:
		print("File created")
	clients = []
def key():
    return(int(time.strftime("%M", time.localtime()))^2)

def getInfo(info,data,key):
    return(decrypt(data.get(info),key))

def decrypt(data,key):
    decrypt = ""
    k = True
    for i in data.decode("utf-8"):
        if i == ":":
            k = True
            decrypt += i
        elif k == False or i == " ":
            decrypt += i
        else:
            decrypt += chr(ord(i)^key)
    return(decrypt)
'''
def crypt(data,key):
    crypt = ""
    for i in data:
        crypt += chr(ord(i)^key)
    data = crypt
    return(data)
'''
while RUN:
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))

    quit = False
    print("[ Server Started ]")

    while not quit:
	#	time.sleep(15)
        try:
            data, addr = s.recvfrom(mass)
            data_temp = json.loads(data.decode("utf-8"))

            if addr not in clients:
                clients.append(addr)
				
            if getInfo("mass",data_temp,key()) != mass and getInfo("mass",data_temp,key()) != None:
                mass = getInfo("mass",data_temp,key())

            itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

            print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="")
            print(data.decode("utf-8"))

            if getInfo("password",data_temp,key()) == password:
                for client in clients:
                    if addr != client:
                        s.sendto(data,client)
        except:	
            print("\n[ Server Stopped ]")
            quit = True
        with open('bots.list', 'w+') as fw:
                json.dump(clients, fw)
s.close()