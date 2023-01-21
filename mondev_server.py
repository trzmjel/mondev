import socket

if __name__=="__main__":
    port = 40534

    s = socket.socket()

    s.bind(('127.0.0.1',port))
    s.listen(5)
    print("MonDev server is starting...")

    try:
        while True:
            c, addr = s.accept()
            print(f'Recived connection from {addr}')
            mess = str(c.recv(1024))
            print(mess)
            
    except KeyboardInterrupt:
        print("Detected keyboard interrupt, exiting.")

    finally:
        s.close()
