import platform
import socket

#-----some variables----

port=40534 #right now gonna leave it like that, may be changed
sep = ', '

def collect_sysinf():
    uname = platform.uname()
    result = uname.system + sep + uname.version + sep + uname.machine + sep + uname.node + sep + uname.release

    return result

print("Put ip address of server you want to send data:")
addr=input()

s=socket.socket()

s.connect((addr,port))
lol=["elo","benc"]
s.send(collect_sysinf().encode()) 
print(collect_sysinf())
s.close
