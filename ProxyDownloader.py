import socket
import urllib.parse
import os
import argparse

# This part helps us to make our port number directly.
parser = argparse.ArgumentParser(description="Proxy server")
parser.add_argument("port", type=int, help="Port to listen on")
args = parser.parse_args()

def proxyDownloader(host, port):
    # That part makes a new socket object.
    socProxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This part specifies host and port.
    socProxy.bind((host, port))
    # We listen our proxys' reaction.
    socProxy.listen()
    # This is printing of listening reaction.
    print(f"[*] {host}:{port} is listening...")
    # This part makes when our reaction happens
    while True:
        # We accept the incoming reaction.
        socClient, addClient = socProxy.accept()
        # This is printing of accepted reaction.
        print(f"[*] {addClient[0]}:{addClient[1]} connection number is accepted!")
        # We retrieve data from the client.
        request = socClient.recv(4096)
        # Our request is extracting in the URL.
        url = urlExtract(request.decode())
        # Specified URL is retrieving.
        contFile, messResponse = fileRetrieve(url)
        # Our file is saving.
        nameFile = fileSave(url, contFile)
        # Our response message to the client is sent.
        socClient.sendall(messResponse.encode())
        # These are our printing materials.
        print("[*] Our client which received request is:\n", request)
        print("[*] Our client which sent response is:\n", messResponse)
        print(f"[*] {url} inside the file downloaded and {nameFile} is saved.")
        # Connection is closed.
        socClient.close()

def urlExtract(request):
    # We will extract URL from an HTTP GET.
    beg = request.find('GET') + 4
    finnish = request.find('HTTP/1.1')
    url = request[beg:finnish].strip()
    return url

def fileRetrieve(url):
    # Retrieves a file's content from the given URL.
    # A tuple with the file content and an HTTP response message is returned.
    try:
        urlParsed = urllib.parse.urlparse(url)
        host = urlParsed.netloc
        path = urlParsed.path
        # We create a new socket object.
        socFile = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We connect a host.
        socFile.connect((host, 80))
        # Our host get our HTTP GET message.
        socFile.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
        # Its received.
        rsp = b""
        while True:
            data = socFile.recv(1024)
            if not data:
                break
            rsp += data
        # Our file is extracted at file content and HTTP response.
        contFile = rsp.split(b"\r\n\r\n")[1]
        messResponse = rsp.split(b"\r\n\r\n")[0].decode()
        # Socket is closed.
        socFile.close()
        return contFile, messResponse

    except Exception as e:
        print(f"[*] Our retrieving error file is: {str(e)}")
        return b"", "HTTP/1.1 404 Not Found\r\n\r\n"
    

def fileSave(url, conttFile):
    # That def makes our downloadable content saves.
    # We create our download path
    if not os.path.exists("Downloaded Files"):
        os.makedirs("Downloaded Files")
    # We create a file name based on URL
    nameFile = os.path.join("Downloaded Files", os.path.basename(url))
    # We write our file content
    with open(nameFile, "wb") as f:
        f.write(conttFile)

    return nameFile

if __name__ == '__main__':
    proxyDownloader('localhost', args.port)