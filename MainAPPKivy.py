# -*- coding: utf-8 -*-
"""
Created on Sun May 15 22:24:29 2022

@author: oussa
"""

#Communication between the App and the Host imports
import os
import socket
import tqdm

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.filemanager import MDFileManager 
from kivy.core.window import Window 

Window.size = (300, 570)

TakePhoto = """ 
ScreenManager : 
        TakePhotoScreen:
            
<MenuScreen>:
    
    ...
    
    MDRectangleFlatButton:
        text: 'Take a Photo'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_press: root.manager.current = 'TakePhoto'

<TakePhotoScreen>:
    name: 'TakePhoto'
    
    MDRectangleFlatButton:
        text: 'Use my camera'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        on_press: root.manager.current = 'menu'
        
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'menu'
        
"""

screen_helper = """

ScreenManager:
    MenuScreen:
    UploadFileScreen:
    ProcessingScreen:
    DownloadPDFScreen:
        
<MenuScreen>:
    name: 'menu'
    
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 50
        MDLabel:
            text : 'Please before using our APP make sure : '

        MDLabel: 
            text: '- That you have all your files in your galery '
        
        MDLabel:
            text: '- That u have a stable internet connexion' 
        
        MDLabel:
            text: '- That all your files respect the conditions mentioned before '
        
        MDLabel:
            text:'Thaks for using our application'
            
        MDRectangleFlatButton:
            text: 'Start'
            pos_hint : {'center_x': .5, 'center_y': .5}
            on_press: root.manager.current = 'Upload'
        
<UploadFileScreen>:
    name: 'Upload'
    
    MDRectangleFlatButton : 
        text : "Please select your File"
        pos_hint : {'center_x': .5, 'center_y': .5}
        on_release : app.open_file_manager()
            
        
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.33,'center_y':0.1}
        on_press: root.manager.current = 'menu'
    
    MDRectangleFlatButton:
        text: 'Next'
        pos_hint: {'center_x':0.66,'center_y':0.1}
        on_press: root.manager.current = 'processing'

<ProcessingScreen>:
    name : 'processing'
    
    MDTextField:
        id: IPadress
        hint_text: "Enter IP adress"
        helper_text_mode: "on_focus"
        icon_right: "android"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:250
    
    MDRectangleFlatButton:
        text: 'Use IP adress'
        pos_hint: {'center_x':0.33,'center_y':0.5}
        on_press: app.get_ip_host()
        
    MDRectangleFlatButton:
        text: 'Connect'
        pos_hint: {'center_x':0.66,'center_y':0.5}
        on_press: app.sending_file()
        
    MDRectangleFlatButton:
        text: 'Get My PDF'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'download_pdf'
        
<DownloadPDFScreen>:
    name: 'download_pdf'
    
    MDRectangleFlatButton:
        text: 'Download PDF'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        on_press: app.receiving_file()
    
    MDRectangleFlatButton:
        text: 'return to menu'
        pos_hint: {'center_x':0.5,'center_y':0.4}
        on_press:  root.manager.current = 'menu'
        
    MDRectangleFlatButton:
        id: btnExit
        text: "Exit"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: app.stop() 
"""

class MenuScreen(Screen):
    pass

class TakePhotoScreen(Screen):
    pass

class UploadFileScreen(Screen):
    pass

class ProcessingScreen(Screen):
    pass

class DownloadPDFScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name = 'menu'))
sm.add_widget(TakePhotoScreen(name = 'TakePhoto'))
sm.add_widget(UploadFileScreen(name = 'Upload'))
sm.add_widget(ProcessingScreen(name = 'processing'))
sm.add_widget(DownloadPDFScreen(name = 'download_pdf'))

class DemoApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager_obj = MDFileManager(
            select_path = self.select_path,
            exit_manager = self.exit_manager,
            preview = True
            )
        self.path = None
        
    def select_path(self, path):
        self.path = path
        self.exit_manager()
   
    def open_file_manager(self):
        self.file_manager_obj.show('/')
        
    def exit_manager(self):
        self.file_manager_obj.close()
    
    def sending_file(self):
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step
        
        # the ip address or hostname of the server, the receiver
        host = self.get_ip_host()
        # the port, let's use 5001
        port = 5001
        # the name of file we want to send, make sure it exists
        filename = self.path
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
        
    def receiving_file(self):
        
        SERVER_PORT = 5001
        # receive 4096 bytes each time
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"
        
        # create the server socket
        # TCP socket
        s = socket.socket()
        s.bind((socket.gethostname(), SERVER_PORT))
        
        # enabling our server to accept connections
        # 5 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        s.listen(5)
        print(f"[*] Listening as {socket.gethostname()}:{SERVER_PORT}")
        
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
            
    def get_host_name(self):
        return socket.gethostbyname(socket.gethostname())
    
    def build(self):
        self.screen = Builder.load_string(screen_helper)
        return self.screen
    
    def get_ip_host(self):
        return self.screen.get_screen('processing').ids.IPadress.text

mainApp = DemoApp()
mainApp.run()