import socket, time, json
import os.path
host = "51.83.203.114"
port = 9090
RUN = True
password = "ALlolIK123"
mass = 8192

if password == "" or password == None:
    password = input("Input password: ")

if os.path.isfile("bots.list"):
	with open('bots.list', 'r') as fr:
		clients = json.load(fr)
else:
	with open("bots.list","w+") as list0:
		print("File created")
	clients = []
def key():
    return(int(time.strftime("%M", time.localtime()))^2)

def getInfo(info,data):
    if data.get(info) == None:
        return("error")
    else:
        return(data.get(info))

def decrypt(data,key):
    if data == None: return("error")
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
    print(0)
    quit = False
    print("[ Server Started ]")

    while not quit:
	#	time.sleep(15)
        try:
            data, addr = s.recvfrom(mass)
            data_temp = json.loads(data.decode("utf-8"))
            print(0)
            if addr not in clients:
                clients.append(addr)
            print(0)
            if getInfo("mass",data_temp) != "error" and getInfo("mass",data_temp) != mass: # Not Crypted 
                mass = int(getInfo("mass",data_temp))                                      # Not Crypted 
            #print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="")
            #print(data.decode("utf-8"))
            time.sleep(5)
            if decrypt(data_temp.get("password"),key()) == password:                       # Crypted
                #s.sendto(data,addr)                                                       # Crypted
                for client in clients:                                                     # Crypted
                    if addr != client:                                                     # Crypted
                        s.sendto(data,client)                                              # Crypted
            else:
                text = {"password": "Incorrect password"}
                text = json.dumps(text)
                s.sendto(text.encode("utf-8"),addr)
                print("Sended")
        except:	
            print("\n[ Server Stopped ]")
            quit = True
    with open('bots.list', 'w+') as fw:
            json.dump(clients, fw)
s.close()