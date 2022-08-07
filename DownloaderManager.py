import threading
from tkinter import *
from queue import Queue
from objectDownloaderSteamCmd import objectDownloaderSteamCmd

#This class is used to manage the objectDownloader class and to communicate with the GUI
class DownloaderManager(threading.Thread):
    
    def __init__(self, window, textBox, endFunction, steamCMDlocation, fileDest, objectID,  gameid, withWine=False):
        self.window = window
        self.textBox = textBox
        self.endFunction = endFunction
        self.queue = Queue()
        self.downloader = objectDownloaderSteamCmd(self.queue, steamCMDlocation, fileDest, objectID, gameid, withWine)
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def stop(self):
        self.downloader.stop()
        self._stop_event.set()        
        while self.downloader.is_alive():
            txtOut = str(self.queue.get())
            if txtOut:
                self.__insertIntoTextBox(txtOut)
                self.window.update()
        self.__insertIntoTextBox("\nSteam as finished to download\n\nReady for a new task")
        self.endFunction()

    def stopped(self):
        return self._stop_event.is_set()
        
    def run(self):
        self.__startDownloader()
        
    def __startDownloader(self):
        self.downloader.start()
        self.__deleteTextBoxContent()
        self.__insertIntoTextBox("Starting Download\n")
        while not self.stopped() and self.downloader.is_alive():
            txtOut = str(self.queue.get())
            if txtOut:
                self.__insertIntoTextBox(txtOut)
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