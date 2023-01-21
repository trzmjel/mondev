import platform
from cpuinfo import get_cpu_info
import psutil
import socket
import json
import os
import subprocess
#-----some variables----
port=40534 #right now gonna leave it like that, may be changed
#-----------------------

def collect_sysinf():
    uname = platform.uname()
    programs=subprocess.check_output(['pacman','-Q']).decode()
    ram= psutil.virtual_memory()
    partitions = psutil.disk_partitions()
    swap = psutil.swap_memory()
    partitions = psutil.disk_partitions()
    if_addrs = psutil.net_if_addrs()
    i=0
    f=open("/sys/class/dmi/id/bios_version","r")
  
    result = {
            "system":uname.system,
            "architecture":uname.machine,
            "bios_ver":f.read(),
            "device_name":uname.node,
            "release":uname.release,
            "cpu_model": get_cpu_info()['brand_raw'],
            "cpu_cores":psutil.cpu_count(logical=False),
            "cpu_threads":psutil.cpu_count(logical=True),
            "cpu_freq":str(psutil.cpu_freq().max),
            "ram_total":ram.total,
            "swap_total":swap.total,
            }
   
    for part in partitions:
        result.update({f"disk{i}_model":part.device})
        result.update({f"disk{i}_fs":part.fstype})
        i=i+1
        
        for line in programs.split('\n')[:-1]:
            temp = line.split(" ")
            result.update({temp[0]:temp[1]})
    #chcemy sprawdzic programy poprzez pacman -Q
         
    return json.dumps(result)

addr=input("Put ip address of server you want to send data (press enter for 127.0.0.1):")
if addr=="":
    addr="127.0.0.1"
s=socket.socket()
s.connect((addr,port))
s.send(collect_sysinf().encode()) 
print(collect_sysinf())
s.close
# Zrobic to tak ze kazda jednostka jest zapisana w tabeli.
