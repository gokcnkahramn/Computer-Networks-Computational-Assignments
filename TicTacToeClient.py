import socket
import threading
import argparse

argparser = argparse.ArgumentParser(description="Proxy server")
argparser.add_argument("port", type=int, help="Port to listen on")
parsargs = argparser.parse_args()

hst = '127.0.0.1'
prt = parsargs.port

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.connect((hst, prt))
print("Connection of server is successful!")

tradeTerm = False  # To determine thread termination, it makes enable to control it
flagInt = False

def transmitData():
    global tradeTerm
    global flagInt
    while True:
        if tradeTerm:
            break
        if flagInt:
            cmd = input("")
            socketClient.sendall(cmd.encode())

def getData():
    global tradeTerm
    global flagInt
    while True:
        packagee = socketClient.recv(1024).decode().strip()
        if packagee:
            print(packagee)
            if "Game is beginning" in packagee:
                flagInt = True
            if "win" in packagee or "lose" in packagee or "draw" in packagee:
                tradeTerm = True  # Since we want to stop thread, it needs to be true
        else:
            break

def main():
    
    thr_rec = threading.Thread(target=getData)
    thr_rec.start()

    thr_send = threading.Thread(target=transmitData)
    thr_send.start()

    thr_rec.join()
    thr_send.join()

    socketClient.close()


if __name__ == '__main__':
    main()