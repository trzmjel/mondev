import socket
import json
import sqlite3

conn = sqlite3.connect("devices.db")
cur = conn.cursor()

if __name__=="__main__":
    port = 40534

    s = socket.socket()

    s.bind(('127.0.0.1',port))
    s.listen(5)
    print("MonDev server is starting...")


    #zrobic tak ze ten identyfikator lepszy niz to
    try:
        while True:
            c, addr = s.accept()
            print(f'Recived connection from {addr}')
            mess = json.loads(c.recv(1024*100).decode())
            # Najlepiej było by zrobić tak, że tworzę tabele ze wszystkimi sprzętami która ma id, które jest nazwą tabeli z programami.

            cur.executescript(f"""CREATE TABLE IF NOT EXISTS devices (
                        uuid TEXT UNIQUE, 
                        system TEXT,
                        architecture TEXT,
                        bios_ver TEXT,
                        device_name TEXT,
                        release TEXT,
                        cpu_model TEXT,
                        cpu_cores NUMBER,
                        cpu_threads NUMBER,
                        cpu_freq REAL,
                        ram_total INTEGER,
                        swap_total INTEGER
                        );""")
            conn.commit()
            cur.executescript(f'REPLACE INTO devices VALUES ("{mess["uuid"]}","{mess["system"]}","{mess["architecture"]}","{mess["bios_ver"]}","{mess["device_name"]}","{mess["release"]}","{mess["cpu_model"]}",{mess["cpu_cores"]},{mess["cpu_threads"]},{mess["cpu_freq"]},{mess["ram_total"]},{mess["swap_total"]});')
            conn.commit();
            cur.execute(f'DROP TABLE IF EXISTS programs_{mess["uuid"]};')
            conn.commit();
            cur.execute(f'CREATE TABLE IF NOT EXISTS programs_{mess["uuid"]} (program TEXT UNIQUE,version TEXT)')
            command = f'INSERT INTO programs_{mess["uuid"]} VALUES '
            keys_to_exclude=set(('uuid','system','architecture','bios_ver','device_name','release','cpu_model','cpu_cores','cpu_threads','cpu_freq','ram_total','swap_total'))
            programs ={k:v for k,v in mess.items() if k not in keys_to_exclude}
            for p in programs:
                command+=f'("{p}","{programs[p]}"),'
            command=command[:-1]+";"
            cur.execute(command)
            conn.commit();
    except KeyboardInterrupt:
        print("Detected keyboard interrupt, exiting.")

    finally:
        s.close()
