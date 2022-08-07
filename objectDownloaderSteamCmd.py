#test collection : 2780825371

#testItem : 917386837

import requests
import json
import os
import shutil
import subprocess
import glob
import threading
from sys import platform

#this class defines the necessary methods to download objects from the steam Workshop
class objectDownloaderSteamCmd(threading.Thread):
    
    #the constructor needs a queue in order to communicate with the father thread that manages it
    def __init__(self, queue, steamCMDlocation, fileDest, objectID,  gameid, withWine=False):
        threading.Thread.__init__(self)
        self.steamCMDlocation = steamCMDlocation
        self.fileDest = fileDest
        self.gameid = gameid
        self.objectID = objectID
        self.queue = queue
        self.result = None
        self.withWine= withWine
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
        self.downloadObjects(self.objectID)
        
    
    #this function allows to get the id.s of all objects in a collection or the id of the object
    #parameter : the id of the object you want to download
    #returns : the id.s of the object you want to download with steamcmd
    def __getItemsIds(self, objectId):
        url="https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/" #URL of the steam API
        data={'collectioncount':'1', 'publishedfileids[0]':str(objectId)} #parameters for the steam API to work
        r=requests.post(url, data) #get POST request results

        requestResult = json.loads(r.text) #extract the results of the request  from the JSON they came in to a usable Python dict
        #The try catch allows me to know if the objectiD correspond to an Item or a collection.
        #if I can't read the 'children' key of requestResult, this mean it doesn't exist for this object so this object is an item.
        elementsIds = []
        try: 
            list = requestResult['response']['collectiondetails'][0]['children']
            
            
            for element in list:
                elementsIds.append(element['publishedfileid'])      
        except KeyError:
            elementsIds.append(str(objectId))
        
        return(elementsIds)


    #check if the folder passed in parameter is writable
    def __checkWritable(self,  folderPath):
        if os.access(folderPath, os.W_OK):
            self.queue.put("File is writable, continuing...")
            return True
        else :
            self.queue.put("File is not writable")
            return False
        
    #Copy the folder content in src to the dest folder
    def __copyDownloadedFiles(self, src, dest):
        if self.__checkWritable(dest):
            filez = glob.glob(src + "\\*")
            for file in filez:
                shutil.copy2(file, dest+"\\"+file.split("\\")[len(file.split("\\")) - 1])
    
    #Move the folder content in src to the dest folder            
    def __moveDownloadedFiles(self, src, dest):
        if self.__checkWritable(dest):
            filez = glob.glob(src + "\\*")
            for file in filez:
                shutil.move(file, dest+"\\"+file.split("\\")[len(file.split("\\")) - 1], copy_function=shutil.copy2)
        else:
            exit()            
    
    #Uses steamCMD to download the content you pass in Item Id
    def __steamCMDdownload(self, steamCMDDir, dest, itemId):
        if self.withWine:
            self.result= subprocess.run(["wine", steamCMDDir+"\steamcmd.exe", "+login", "anonymous", "+workshop_download_item", str(self.gameid),  str(itemId) , "+quit"], capture_output=True)
        elif platform=="win32":
            self.result = subprocess.run([steamCMDDir+"\\steamcmd.exe", "+login", "anonymous", "+workshop_download_item", str(self.gameid),  str(itemId) , "+quit"], capture_output=True)
        else:
            self.result = subprocess.run([steamCMDDir+"/steamcmd.sh", "+login", "anonymous", "+workshop_download_item", str(self.gameid),  str(itemId) , "+quit"], capture_output=True)
        
        if self.result.stderr:
            raise subprocess.CalledProcessError(
                    returncode = self.result.returncode,
                    cmd = self.result.args,
                    stderr = self.result.stderr
                    )
        if self.result.stdout:
            self.__moveDownloadedFiles(steamCMDDir + "\\steamapps\\workshop\\content\\" + str(self.gameid) + '\\' + str(itemId), dest)
            self.queue.put(format(self.result.stdout.decode('utf-8')))
                

    #Call every methods to download a Steam Workshop Item or collection
    def downloadObjects(self, objectId):
        ids = self.__getItemsIds(objectId)
        i=0
        for id in ids:
            if not self.stopped():
                i=i+1
                self.queue.put("\nDownloading item "+ str(i) + " out of " + str(len(ids))+"\n\n")
                self.__steamCMDdownload(self.steamCMDlocation, self.fileDest, id)
            else:
                break
            