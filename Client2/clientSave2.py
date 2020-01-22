#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import messagebox #used for the alert of important messages

from Crypto.Cipher import AES
# import tkinter
from tkinter import *
import tkinter.messagebox
import datetime as date #used to get date and time for messages
from datetime import datetime

def testline(line): #checks whether message is older than six months and important
    sixmonths = (date.date.today() - date.timedelta(6 * 365 / 12)) #set what sixmonths is equal to, using date time  minus 6 months
    date_object = datetime.strptime(line[9:19], "%Y-%m-%d") #takes the time and date as a string and converts it into a date object that only contains the date(used to check whether to keep storing messages)
    if date_object.date() <= sixmonths and line[8] == '0': # if older than sixmonths and not important
        return False #delete the message
    else:
        return True #dont delete the message if dateobject is older than six months or important

def deleteLines(): #will delete the message from text file
    with open("chatHistory" + userID + ".txt", "r") as f:
        lines = f.readlines() #go through each line(msg)
    with open("chatHistory" + userID + ".txt", "w") as f: #chatistory is the txt file created storing the messages
        for line in lines:
            if testline(line.strip("\n")): #if testline true = message should still be stored
                f.write(line) #keep stroing the line(message)

unClicked = True #buttn for load messages
def printLines(): #ouputs previous messages to GUI
    global unClicked
    if unClicked: # if unclicked (load chat history) is true
        unClicked = False #so you dont keep loading previous messages
        deleteLines() #deletes unwanted stored messages
        msg_list.delete(1000,
                        tkinter.END)  # 100 is the amount of messages to be shown, deletes messages inchat so that history is shown chronologically
        msg_list.update()
        with open("chatHistory" + userID + ".txt", "r") as f:
            lines = f.readlines() #creating an array called lines that stores all the messages from chat histroy
        for line in lines: #iterates through each line
            msg = unscramble(5, line).strip("\n") #because they are encrypted, need to unscramble them first
            if msg[4:8] == userID or msg[0:4] == userID: #declares what info each part of the message contains
                nameSent = msg[0:4] #line of message shows the sender
                nameRecieved = msg[4:8] #next shows who should receive the message
                important = msg[8] # set 0 or 1 to show if important or not
                date = msg[9:19] # stores date
                strT = msg[19:27] #time
                messageText = msg[27:] #the text of message

                for x in people:#matches user Id to given name
                    if str(people[x]) == nameRecieved:
                        nameRecieved = x # therefore when message outputted t will show name instead of user ID

                for x in people:
                    if str(people[x]) == nameSent:
                        nameSent = x

                if important == "0": #if sender has not marked the tickbox as important (for meesage to be sent)
                    msg_list.insert(tkinter.END,
                                    "(Date: " + date + ", Time:" + strT + ") " + nameSent + " to " + nameRecieved + ": " + messageText) #output to GUI

                if important == "1": #if sender has  marked the tickbox as important (for meesage to be sent)
                    msg_list.insert(tkinter.END,
                                    "(Date: " + date + ", Time: " + strT + ") " + nameSent + " to " + nameRecieved + " : (Important) " + messageText)  # add alert

def scramble(n, plaintext): #re use of code from sololearn
    """Encrypt the string and return the ciphertext"""
    result = ''
    for l in plaintext:
        try:
            i = (key.index(l) + n) % 26
            result += key[i]
        except ValueError:
            result += l

    return result

def unscramble(n, ciphertext):
    """Decrypt the string and return the plaintext"""
    result = ''
    ciphertext.strip("\n")
    for l in ciphertext:
        try:
            i = (key.index(l) - n) % 26
            result += key[i]
        except ValueError:
            result += l

    return result
def append(line): #write line to end of text file
    with open("chatHistory" + userID + ".txt", "a") as f:
        f.write(scramble(5, line) +"\n") # scramble the message and add to end of text file

#encryption re use code
def encrypt(message): #re used some code from stackoverflow
    while len(message) % 16: #it gave an error unless the message length was a multiple of 16
        message += " "
    obj = AES.new('This is a key123'.encode("utf-8"), AES.MODE_CBC, 'This is an IV456'.encode("utf-8"))
    ciphertext = obj.encrypt(message.encode("utf-8"))
    return ciphertext

def decrypt(ciphertext): #resused code from stackoverflow
    obj2 = AES.new('This is a key123'.encode("utf-8"), AES.MODE_CBC, 'This is an IV456'.encode("utf-8")) #object created for decrpyption
    return obj2.decrypt(ciphertext).decode("utf-8").strip()


def receive(): #function for getting a message
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ) #waits to receive a message from the server
            msg = decrypt(msg) #decrypt the message thats being sent so receiver can read it
            if msg[4:8] == userID:
                nameSent = msg[0:4]
                nameRecieved = msg[4:8]
                important = msg[8]
                date = msg[9:19]
                strT = msg[19:27]
                messageText = msg[27:]
                append(msg)

                for x in people:
                    if str(people[x]) == nameRecieved:
                        nameRecieved = x

                for x in people:
                    if str(people[x]) == nameSent:
                        nameSent = x

                if important == "0":
                    msg_list.insert(tkinter.END,
                                    "(Date: " + date + ", Time:" + strT + ") " + nameSent + " to " + nameRecieved + ": " + messageText)

                if important == "1":
                    messagebox.showinfo("Information", "Important message from: " + nameSent) #alert box pop up if receiver gets new a message marked important
                    msg_list.insert(tkinter.END,
                                    "(Date: " + date + ", Time: " + strT + ") " + nameSent + " to " + nameRecieved + " : (Important) " + messageText)  # add alert

        except OSError:  # Possibly client has left the chat.
            break #from original program


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    if chkValue.get() == True: #checks if he sender ticked the important box
        important = '1'
    else:
        important = '0'

    msg = userID + my_msg_rec.get() + important + datetime.now().strftime('%Y-%m-%d%H:%M:%S') + my_msg.get() # included info into the message, userID my_message recived get and important

    if msg[0:4] == userID:
        nameSent = msg[0:4]
        nameRecieved = msg[4:8]
        important = msg[8]
        date = msg[9:19]
        strT = msg[19:27]
        messageText = msg[27:]
        append(msg)

        for x in people:
            if str(people[x]) == nameRecieved:
                nameRecieved = x

        for x in people:
            if str(people[x]) == nameSent:
                nameSent = x

        if important == "0":
            msg_list.insert(tkinter.END,
                            "(Date: " + date + ", Time:" + strT + ") " + nameSent + " to " + nameRecieved + ": " + messageText)

        if important == "1":
            msg_list.insert(tkinter.END,
                            "(Date: " + date + ", Time: " + strT + ") " + nameSent + " to " + nameRecieved + " : (Important) " + messageText)  # add alert

    msg = encrypt(msg)  #once msg is written, make sure it is encrypted

    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg)) #sned encypted message to server to then be passed through to user it should be sent to

    if msg == "{quit}": #if user types in quit, the chat should close
        client_socket.close()
        top.quit() #close GUI


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    top.destroy() #closes the GUI

key = 'zyxwvutsrqponmlkjihgfedcba'
userID = str(input('Please enter your given ID (4 digit number): ')) #written in python console, verifies id
top = tkinter.Tk()
top.title(userID) #shown on GUI

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.") #input box where message should be displayed

my_msg_rec = tkinter.StringVar()  # type in who the message is for
my_msg_rec.set("Type your recipient here.")  #recipient have to match the host pc for message to be displayed

scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=20, width=150, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg_rec)
entry_field.pack()

chkValue = tkinter.BooleanVar()
chkValue.set(True)

chkExample = tkinter.Checkbutton(messages_frame, text='Important', var=chkValue).pack()

send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

send_button = tkinter.Button(messages_frame, text="Load Chat History", command=printLines) #button to load chat history
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# ----Now comes the sockets part---- code reuse referenced in portfolio
HOST = "127.0.0.1" #IP address of the server
PORT = 33000 #Port of server
people = {"John": 1111, "Ethan": 2222, "Bradly": 3333, "Charlie": 4444} #the saved users

BUFSIZ = 1024
ADDR = (HOST, PORT) #contains the information needed to connect to the server

client_socket = socket(AF_INET, SOCK_STREAM) #declaring a connection unique to this client running this program
client_socket.connect(ADDR)  #links the connection to the addess; which holds information of the server

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
