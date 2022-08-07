import subprocess
import threading
from tkinter import *
from sys import platform

#This class manages rFactor2 dedicated server Update so you don't need to call the program via steamcmd yourself
class AppUpdater(threading.Thread):
    
    def __init__(self, window, textBox, endFunction, steamCMDlocation, withWine=False):
        threading.Thread.__init__(self)
        self.steamCMDlocation = steamCMDlocation
        self.window = window
        self.textBox= textBox
        self.withWine= withWine
        self.endFunction = endFunction
        self.steamCMDlocation = steamCMDlocation
        self._stop_event = threading.Event()

    def run(self):
            self.__deleteTextBoxContent()
            self.__insertIntoTextBox("Updating rFactor2 server\n\n")
        
            if self.withWine:
                result= subprocess.run(["wine", self.steamCMDlocation+"\steamcmd.exe", "+login", "anonymous", "+force_install_dir", "../rFactor2-Dedicated",  "+app_update" , "400300" , "+quit"], capture_output=True)
            elif platform=="win32":
                result = subprocess.run([self.steamCMDlocation+"\\steamcmd.exe", "+login", "anonymous", "+force_install_dir", "../rFactor2-Dedicated",  "+app_update" , "400300" , "+quit"], capture_output=True)
            else:
                result = subprocess.run([self.steamCMDlocation+"/steamcmd.sh", "+login", "anonymous", "+force_install_dir", "../rFactor2-Dedicated",  "+app_update" , "400300" , "+quit"], capture_output=True)
            
            if result.stderr:
                raise subprocess.CalledProcessError(
                        returncode = result.returncode,
                        cmd = result.args,
                        stderr = result.stderr
                        )
            if result.stdout:
                self.__insertIntoTextBox(format(result.stdout.decode('utf-8')))
                self.__insertIntoTextBox("\nSteam as finished to download\n\nReady for a new task")
            self.endFunction()
                
    def __insertIntoTextBox(self, message):
        self.textBox.configure(state='normal')
        self.textBox.insert(INSERT, message)
        self.textBox.configure(state='disabled')
        self.window.update()                
        
    def __deleteTextBoxContent(self):
        self.textBox.configure(state='normal')
        self.textBox.delete(1.0,END)
        self.textBox.configure(state='disabled')
        self.window.update()