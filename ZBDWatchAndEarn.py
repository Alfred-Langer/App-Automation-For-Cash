
import time
import sys
from discord_webhook import DiscordWebhook
import NavigationFunctions as nf
import os
import ast

# Function to find the location of the watch button and scroll down if it is not in view
def scroll_to_watch_button(region_rectangle, serial):

    #Initialize a counter to keep track of how many times we have scrolled down
    watch_button_scroll_counter = 0

    #Attempt to find the location of the watch button
    print("Attempting to find the location of the watch button")
    watch_button, xCor, yCor = nf.MoveToLocation(file_path=f'watch_button_{serial}.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            region_rectangle=region_rectangle,
                                            confidence=0.80)
    
    #If the watch button is not found, continue scrolling down until it is found or the counter reaches 8
    while(watch_button == "" and watch_button_scroll_counter < 8):
        #Scroll down slightly
        nf.scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 925, settle_delay=1, serial=serial)
        
        #Attempt to find the location of the watch button
        print("Attempting to find the location of the watch button")
        watch_button, xCor, yCor = nf.MoveToLocation(file_path=f'watch_button_{serial}.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            region_rectangle=region_rectangle,
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
    
    #Otherwise, we assume the watch button is in view and we don't need to scroll
    else:
        print("Watch button has been found. No longer scrolling")
        time.sleep(3)  # Pause for a second to let the screen settle





if __name__ == "__main__":

    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)


    if len(sys.argv) >= 2:
        if sys.argv[1] == "left":
            instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_LEFT_REGION_RECTANGLE"))
        elif sys.argv[1] == "right":
            instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_RIGHT_REGION_RECTANGLE"))
        elif sys.argv[1] == "center":
            instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_REGION_RECTANGLE"))
        else:
            print("Invalid argument. Please enter either 'left' or 'right' as an argument.")
            exit()
        
    else:
        instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_REGION_RECTANGLE"))


    if len(sys.argv) == 3:
        serial_number = sys.argv[2]
    else:
        serial_number = None

    #This script should be used after Bitcoin Miner farming has finished

    #Search for the ZBD app
    print("Searching for the ZBD app")
    zbd_app, xCor, yCor = nf.MoveToLocation(file_path=f'zbd_app_{serial_number}.png',
                                            parent_directory='Phone_Images',
                                            region_rectangle=instance_region_rectangle,
                                            timeout=5,
                                            confidence=0.80)

    #If the ZBD app is found, open it by tapping on the app
    if zbd_app != '':
        nf.tap(xCor, yCor, serial=serial_number, region_rectangle=instance_region_rectangle)
        print("ZBD app has been opened")
        time.sleep(10)
    
    #If the ZBD app is not found, then we kill the script so the program does not go haywire
    else:
        print("ZBD app not found. Stopping the script.")
        sys.exit()

    # #We now want to search for an indication that the app is open
    # print("Searching for an indication that the app has opened")
    # app_open, xCor, yCor = nf.MoveToLocation(file_path='zbd_app_has_loaded.png',
    #                                         parent_directory='ZBD_Videos',
    #                                         region_rectangle=instance_region_rectangle,
    #                                         timeout=5,
    #                                         confidence=0.80)
    
    # #If we can't find the app open indication, we assume the app has not opened properly and we kill the script
    # if app_open == "":
    #     print("ZBD app has not opened properly. Stopping the script.")
    #     sys.exit()

    
    #We now want to search for the earn icon
    print("Searching for the earn icon")
    earn_icon, xCor, yCor = nf.MoveToLocation(file_path='earn_icon.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            region_rectangle=instance_region_rectangle,
                                            confidence=0.70)

    #If we can't find the earn icon, we assume the app has not opened properly and we kill the script
    if earn_icon != "":
        print("Earn icon found. Tapping on it")
        nf.tap(xCor, yCor,serial=serial_number, region_rectangle=instance_region_rectangle)
        time.sleep(3)
    
    else:
        print("Earn icon not found. Stopping the script.")
        sys.exit()

    #Search for the watch button by scrolling down
    print("Searching for the watch button")
    scroll_to_watch_button(region_rectangle=instance_region_rectangle, serial=serial_number)

    print("Beginning the watch video process")
    while True:

        watch_button, xCor, yCor = nf.MoveToLocation(file_path=f'watch_button_{serial_number}.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=5,
                                            settle_delay=1,
                                            region_rectangle=instance_region_rectangle,
                                            confidence=0.80)
        
        if watch_button:
            nf.tap(xCor, yCor, serial=serial_number, region_rectangle=instance_region_rectangle)
            limit_image, xCor, yCor = nf.MoveToLocation(file_path=f'limit_has_been_reached_{serial_number}.png',
                                            parent_directory='ZBD_Videos',
                                            timeout=30,
                                            settle_delay=1,
                                            region_rectangle=instance_region_rectangle,
                                            confidence=0.60)
            if limit_image:
                print("The limit has been reached. Returning to home and stopping the script.")
                sys.exit()

        else:
            if not(nf.clear_advertisement_2(timeout=120,serial=serial_number, region_rectangle=instance_region_rectangle)):
                print("Unknown advertisement found. Resetting to the home screen.")
                nf.go_to_home_screen(serial=serial_number)

                #Search for the ZBD app
                print("Searching for the ZBD app")
                zbd_app, xCor, yCor = nf.MoveToLocation(file_path=f'zbd_app_{serial_number}.png',
                                                        parent_directory='Phone_images',
                                                        region_rectangle=instance_region_rectangle,
                                                        timeout=5,
                                                        confidence=0.80)

                #If the ZBD app is found, open it by tapping on the app
                if zbd_app != '':
                    nf.tap(xCor, yCor, serial=serial_number, region_rectangle=instance_region_rectangle)
                    print("ZBD app has been reopened")
                    
                
                #If the ZBD app is not found, then we kill the script so the program does not go haywire
                else:
                    print("ZBD app not found. Stopping the script.")
                    sys.exit()
                    
   