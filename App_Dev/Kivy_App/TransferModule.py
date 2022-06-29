# -*- coding: utf-8 -*-
"""
Created on Wed May 18 21:42:03 2022

@author: oussa
"""
import socket
import tqdm
import os

def trasfer_file_sender(host, file, port = 5001):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    
    # the ip address or hostname of the server, the receiver
    # host = "192.168.1.33"
    # the port, let's use 5001
    
    # the name of file we want to send, make sure it exists
    filename = "transferTest.txt"
    # get the file size
    filesize = os.path.getsize(filename)
    
    # create the client socket
    s = socket.socket()
    
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    
    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    
    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()

def transfer_file_HOST(SERVER_PORT = 5001):
    # device's IP address
    SERVER_HOST = socket.gethostname()
    
    print(socket.gethostbyname(socket.gethostname()))
    
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    
    # create the server socket
    # TCP socket
    s = socket.socket()
    
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    
    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    
    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    
    # remove absolute path if there is
    filename = os.path.basename(filename)
    
    # convert to integer
    filesize = int(filesize)
    
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open("./UploadsUsingAPP/" + filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    
    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()