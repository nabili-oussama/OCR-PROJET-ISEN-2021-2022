# -*- coding: utf-8 -*-
"""
Created on Sun May 15 20:43:28 2022

@author: oussa
"""

import os
import socket

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.filemanager import MDFileManager 
from kivy.core.window import Window 

Window.size = (300, 570)


screen_helper = """

ScreenManager:
    MenuScreen:
    TakePhotoScreen:
    UploadFileScreen:
    ProcessingScreen:
        
<MenuScreen>:
    name: 'menu'
    
    MDRectangleFlatButton:
        text: 'Take a Photo'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_press: root.manager.current = 'TakePhoto'
        
    MDRectangleFlatButton:
        text: 'Upload a File'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        on_press: root.manager.current = 'Upload'
    
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
        
<UploadFileScreen>:
    name: 'Upload'
    
    MDFlatButton : 
        text : "open File Manager"
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
              
"""

class MenuScreen(Screen):
    pass

class TakePhotoScreen(Screen):
    pass

class UploadFileScreen(Screen):
    pass

class ProcessingScreen(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name = 'menu'))
sm.add_widget(TakePhotoScreen(name = 'TakePhoto'))
sm.add_widget(UploadFileScreen(name = 'Upload'))
sm.add_widget(ProcessingScreen(name = 'processing'))


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
        
        HOST = self.get_ip_host()  # The server's hostname or IP address
        PORT = 65432     # The port used by the server
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.connect((HOST, PORT))
            
            # Getting file details.
            file_name = self.path
            file_size = os.path.getsize(file_name)
            
            # Sending file_name and detail.
            s.send(file_name.encode())
            s.send(str(file_size).encode())
            
            # Opening file and sending data.
            with open(file_name, "rb") as file:
                c = 0
            
                # Running loop while c != file_size.
                while c <= file_size:
                    data = file.read(1024)
                    if not (data):
                        break
                    s.sendall(data)
                    c += len(data)

            data = s.recv(1024)
        
        print(f"Received {data!r}")
    
    def receiving_file(self):
        PORT = 65432
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.bind((socket.gethostname(), PORT))
            s.listen()
            
            conn, addr = s.accept()
            
            file_name = s.recv(100).decode()
            file_size = s.recv(100).decode()
            
            with open("./rec/" + file_name, "wb") as file:
                
                print(f"Connected by {addr}")
                
                c = 0
            
                # Running the loop while file is recieved.
                while c <= int(file_size):
                    data = s.recv(1024)
                    if not (data):
                        break
                    file.write(data)
                    c += len(data)
            print("File transfer completed.")
    
    def build(self):
        self.screen = Builder.load_string(screen_helper)
        return self.screen
    
    def get_ip_host(self):
        return self.screen.get_screen('processing').ids.IPadress.text

mainApp = DemoApp()
mainApp.run()