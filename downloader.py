import tkinter
from DownloaderManager import DownloaderManager
from AppUpdater import AppUpdater
from tkinter import *
import tkinter.scrolledtext as st
from tkinter import messagebox
from tkinter import filedialog
from subprocess import CalledProcessError


class mainWindow:
    def __init__(self):
        
        self.myWindow = Tk()
        self.myWindow.resizable(False, False)
        self.myWindow.title('Steam Workshop Easy Downloader')
        self.dmInstance=None
        self.consoleOutput= st.ScrolledText(self.myWindow)
        self.consoleOutput.configure(state='disabled')    
        
        #creation of all variable entry field and buttons that need to be shared in the class
        self.gameid = Entry(self.myWindow)
        self.objectid = Entry(self.myWindow)
        self.gameid.insert(END, '365960')
        self.objectid.insert(END, '917430973')
        self.steamCMDlocation = r"C:\Racing\steamcmd"
        self.fileDest=r"C:\Racing\rfactor2-dedicated\Packages"
        self.startButton=Button(self.myWindow, text="Start Download", command= self.startDownManager)
        self.stopButton=Button(self.myWindow, text="Stop Download", command=self.stopDownManager)
        self.updateButton = Button(self.myWindow, text="Install / Update Rfactor2 Server", command= self.updateRF2Serv)
        
        #every elements placement
        Label(self.myWindow, text = "Game Steam ID :").grid(row=0, column=0, sticky=E)
        self.gameid.grid(row=0, column=1, sticky=W)
        Label(self.myWindow, text = "Object Workshop ID :").grid(row=1, column=0, sticky=E)
        self.objectid.grid(row=1, column=1, sticky=W)
        Button(self.myWindow, text="Select SteamCMD directory", command= self.askForSteamCMDFolder).grid(row=2, column=0, sticky=E)
        Label(self.myWindow, text= self.steamCMDlocation).grid(row=2, column=1, sticky=W)
        Button(self.myWindow, text="Select destination directory", command= self.askFileDest).grid(row=3, column=0, sticky=E)
        Label(self.myWindow, text= self.fileDest).grid(row=3, column=1, sticky=W)
        self.startButton.grid(row=4, column=1, sticky=W)
        self.useWine =  tkinter.IntVar()
        Checkbutton(self.myWindow, text="use Wine", variable=self.useWine).grid(row=4, column=0, sticky=E)
        Label(self.myWindow, text = "SteamCMD output:" ).grid(column=0,row=6, sticky=W)
        self.updateButton.grid(row=5, column=0, columnspan=2)
        self.consoleOutput.grid(column=0,row=7, columnspan=2)



        self.myWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.myWindow.mainloop()
    
    #Allow the GUI to know if the ids entered are valid
    def _validate(self, P):
        return P.isdigit()
      
    def startDownManager(self):
        if(hasattr(self, "steamCMDlocation") and hasattr(self, "fileDest")):
            try:
                objID = int(self.objectid.get())
                if(objID <= 0):
                    raise ValueError()
                try:
                    gameID = int(self.gameid.get())
                    if(gameID <= 0):
                        raise ValueError()
                    self.dmInstance = DownloaderManager(self.myWindow, self.consoleOutput,  self.showActionButtons, self.steamCMDlocation, self.fileDest, objID, gameID, self.useWine.get())
                    try:
                        self.dmInstance.start()
                        self.hideActionButtons()
                    except CalledProcessError:
                        messagebox.showerror("SteamCMD Error", "SteamCMD couldn't execute your request or couldn't been executed")
                    
                except ValueError:
                    messagebox.showerror("Wrong Game ID", "The game ID is not a valid number, enter a positive numeric value and try again")
            except ValueError:
                messagebox.showerror("Wrong Object ID", "The object ID is not a valid number, enter a positive numeric value and try again")
        else:
            messagebox.showerror("Directories Not Specified", "One or both of the directories haven't been specified")
        
        
    def stopDownManager(self):
        self.stopButton.grid_forget()
        messagebox.showinfo("Program End", "Program is ending, it will wait till steam finishes to download the current item then close itself")
        self.dmInstance.stop()
       
        
    #custom closing function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if(self.dmInstance != None and self.dmInstance.is_alive() and not self.dmInstance.stopped()):
                self.dmInstance.stop()
                messagebox.showinfo("Program End", "Program is ending, it will wait till steam finishes to download the current item then close itself")
                self.dmInstance.join()
            self.myWindow.destroy()
            
    def askForSteamCMDFolder(self):
        self.steamCMDlocation = filedialog.askdirectory()
        Label(self.myWindow, text= self.steamCMDlocation).grid(row=2, column=1, sticky=W)
        self.myWindow.update()
    
    def askFileDest(self):
        self.fileDest = filedialog.askdirectory()
        Label(self.myWindow, text= self.fileDest).grid(row=3, column=1, sticky=W)
        self.myWindow.update()
    
    #Allow users to launch a rFactor2 server update command
    def updateRF2Serv(self):
        if hasattr(self, "steamCMDlocation"):
            try:
                self.hideActionButtons(False)
                AppUpdater(self.myWindow, self.consoleOutput, self.showActionButtons, self.steamCMDlocation, self.useWine.get()).start()
            except CalledProcessError:
                messagebox.showerror("SteamCMD Error", "SteamCMD couldn't execute your request or couldn't been executed")
        else:
            messagebox.showerror("Directory Not Specified", "SteamCMD direcory hasn't been specified")
            
    def showActionButtons(self):
        self.stopButton.grid_remove()
        self.startButton.grid()
        self.updateButton.grid()
        self.myWindow.update()
        
        
    def hideActionButtons(self, showStopButton=True):
        self.updateButton.grid_remove()
        self.startButton.grid_remove()
        if(showStopButton):
            self.stopButton.grid(row=5, column=0, columnspan=2)
                


#This simple call to the mainWindow constructor lauches the program            
mainWindow()
