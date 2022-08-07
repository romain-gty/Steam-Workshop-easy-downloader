This software allow the user to download steam workshop collection and Items with a simple GUI

This software is not created by Valve and is not affiliated with Steam or rFactor2.
This is a fan project to make life easier to steam dedicated game servers owners that need to use the Steam Workshop to add content to their servers (like rFactor2, which is the game I had in mind while creating this software)



This software uses SteamCMD that is not provided in this repository so you'll have to download it yourself first. This is easy and there is a lot of documentation out there.



This software simply calls to SteamCMD command and Steam API to download the workshop content you want to download.



It also includes a update rFactor2 server command that will install / update rFactor2 dedicated server. It will download rFactor 2 server in the default folder of the documentation which is here on your drive: Your steamCMD folder../rFactor2 dedicated

If you want to install it in another folder, modify the command call, the "../rFactor2-Dedicated"  (line 24, 26, 28) in AppUpdater.py



This softwares uses a Tkinter to generate a GUI
