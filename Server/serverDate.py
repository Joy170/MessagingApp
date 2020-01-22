#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections(): #code reuse
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address) #prints the IP address of the last clien that connected
        print(client) #shows client information
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = "client"
    clients[client] = name

    while True: #always checking, therefore coninue the loop
        msg = client.recv(BUFSIZ) #always for checking whether a client is sending message
        broadcast(msg) # if this is the case, broadcast the message then continue loops

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(msg) #sends essage to all clients, but not only the clients the message is ment for can read it


clients = {}
addresses = {}

HOST = "127.0.0.1" #is declared in each client to be able to connect
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5) #listening for new clients to connect to the server
    print("Waiting for connection...")
    print(type(SERVER))
    ACCEPT_THREAD = Thread(target=accept_incoming_connections) #runs the thread that accept clients with input of oorrect address
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()