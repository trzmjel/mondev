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
            cur.execute(f'DROP TABLE {mess["device_name"]}')
            conn.commit()
            cur.execute(f'CREATE TABLE IF NOT EXISTS {mess["device_name"]} (\'KEY\' TEXT, \'VALUE\' TEXT);')
            conn.commit()
            for x in mess:
                cur.execute(f'INSERT INTO {mess["device_name"]} VALUES (\'{x}\',\'{mess[x]}\');')
                conn.commit()
    except KeyboardInterrupt:
        print("Detected keyboard interrupt, exiting.")

    finally:
        s.close()
