import subprocess
import pyautogui
import logging
import time
import sys
from discord_webhook import DiscordWebhook
import datetime
import NavigationFunctions as nf

# Function to find the location of the watch button and scroll down if it is not in view
def scroll_to_watch_button():

    #Initialize a counter to keep track of how many times we have scrolled down
    watch_button_scroll_counter = 0

    #Attempt to find the location of the watch button
    print("Attempting to find the location of the watch button")
    watch_button, xCor, yCor = nf.MoveToLocation(file_path='watch_button.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            confidence=0.80)
    
    #If the watch button is not found, continue scrolling down until it is found or the counter reaches 8
    while(watch_button == "" and watch_button_scroll_counter < 8):
        #Scroll down slightly
        nf.scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 925, settle_delay=1)
        
        #Attempt to find the location of the watch button
        print("Attempting to find the location of the watch button")
        watch_button, xCor, yCor = nf.MoveToLocation(file_path='watch_button.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            confidence=0.80)
        
        #If the watch button is not found, increment the counter
        if watch_button == "":
            #Increment the counter 
            watch_button_scroll_counter += 1

        #If the watch button is found, break out of the loop and set the watch_button_not_in_view flag to False
        else:
            print("Watch button has been found. No longer scrolling")
            time.sleep(3)  # Pause for a second to let the screen settle
            
            return None

    #If we can't find the watch button after 20 scrolls, we assume we are in an advertisement
    if watch_button_scroll_counter > 20:
        print("Watch button has not been found after 20 scrolls. We are most likely viewing an advertisement.")
        watch_button_not_in_view = True
    
    #Otherwise, we assume the watch button is in view and we don't need to scroll
    else:
        print("Watch button has been found. No longer scrolling")
        time.sleep(3)  # Pause for a second to let the screen settle
   

if __name__ == "__main__":

    #This script should be used after Bitcoin Miner farming has finished

    #Go to the home screen first
    print("Going to the home screen")
    nf.go_to_home_screen()

    #Search for the ZBD app
    print("Searching for the ZBD app")
    zbd_app, xCor, yCor = nf.MoveToLocation(file_path='zbd_app.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            confidence=0.80)

    #If the ZBD app is found, open it by tapping on the app
    if zbd_app != '':
        nf.tap(xCor, yCor)
        print("ZBD app has been opened")
        time.sleep(10)
    
    #If the ZBD app is not found, then we kill the script so the program does not go haywire
    else:
        print("ZBD app not found. Stopping the script.")
        sys.exit()

    #We now want to search for an indication that the app is open
    print("Searching for an indication that the app has opened")
    app_open, xCor, yCor = nf.MoveToLocation(file_path='zbd_app_has_loaded.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            confidence=0.80)
    
    #If we can't find the app open indication, we assume the app has not opened properly and we kill the script
    if app_open == "":
        print("ZBD app has not opened properly. Stopping the script.")
        sys.exit()

    
    #We now want to search for the earn icon
    print("Searching for the earn icon")
    earn_icon, xCor, yCor = nf.MoveToLocation(file_path='earn_icon.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            confidence=0.80)

    #If we can't find the earn icon, we assume the app has not opened properly and we kill the script
    if earn_icon != "":
        print("Earn icon found. Tapping on it")
        nf.tap(xCor, yCor)
        time.sleep(3)
    
    else:
        print("Earn icon not found. Stopping the script.")
        sys.exit()

    #Search for the watch button by scrolling down
    print("Searching for the watch button")
    scroll_to_watch_button()

    print("Beginning the watch video process")
    while True:

        watch_button, xCor, yCor = nf.MoveToLocation(file_path='watch_button.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            settle_delay=1,
                                            confidence=0.80)
        
        if watch_button:
            nf.tap(xCor, yCor)
            limit_image, xCor, yCor = nf.MoveToLocation(file_path='limit_has_been_reached.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=30,
                                            settle_delay=1,
                                            confidence=0.75)
            if limit_image:
                print("The limit has been reached. Returning to home and stopping the script.")
                sys.exit()

        else:
            nf.clear_advertisement(timeout=45, region_rectangle=nf.SCRCPY_REGION_RECTANGLE)

            

