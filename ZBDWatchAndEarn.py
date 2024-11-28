import subprocess
import pyautogui
import logging
import time
import sys
from discord_webhook import DiscordWebhook
import datetime


time.sleep()


##CONSTANTS
PHONE_SCREEN_REGION_RECTANGLE = (704,23,1214,1159)
PIXEL_6_SCREEN_RESOLUTION = (1080, 2400)

#LOCATE IMAGES AND MOVE CURSOR TO LOCATION FUNCTIONS
def MoveToLocation(file_path:str, parent_directory='ZBD_Videos', x_offset=0, y_offset=0, click_flag=False, double_click_flag = False, second_click_x_offset=0, second_click_y_offset=0, click_delay=0.0, double_click_delay=1.0, timeout=120, region_rectangle=PHONE_SCREEN_REGION_RECTANGLE, confidence = 0.9, settle_delay=1, grayScaleFlag=False, topLeftCornerFlag=False, timeoutErrorMessage = True, moveToFlag = False, confirmLocationFlag = False, transitionConfirmationImage = ""):
    #We convert region_rectangle into a region here because we have to convert the dimensions of the rectangle into measurements that Pyautogui understands
    #Pyautogui region: (topCornerXValue, topCornerYValue, widthOfRectangle, heightOfRectangle)
    region = (region_rectangle[0],region_rectangle[1],region_rectangle[2] - region_rectangle[0],region_rectangle[3] - region_rectangle[1])


    #end_time is the time value in which we will stop searching for the object 
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            
            location = pyautogui.locateCenterOnScreen(f"./Screenshots/{parent_directory}/{file_path}", 
                                                        confidence=confidence, 
                                                        region=region, 
                                                        grayscale=grayScaleFlag)

            final_x, final_y = location[0] + x_offset, location[1] + y_offset
            if(moveToFlag):
                pyautogui.moveTo(final_x, final_y)
            
            time.sleep(settle_delay)
            return ([file_path,location[0],location[1]])
        
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)  # Short sleep to avoid high CPU usage
        except Exception as e:
            print(e)
            print("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
            
            logging.critical(e)
            logging.critical("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
            
    if timeoutErrorMessage:
        print(f"Timeout reached, {file_path} not found.")
        logging.critical(f"Timeout reached, {file_path} not found.")   

    return ("",False, False)

def MoveToLocationList(file_paths:list, parent_directory='ZBD_Videos', x_offset=0, y_offset=0, click_flag=False, double_click_flag = False, second_click_x_offset=0, second_click_y_offset=0, click_delay=0.0, timeout=120, region_rectangle=PHONE_SCREEN_REGION_RECTANGLE, confidence = 0.9, settle_delay=1, grayScaleFlag=False, topLeftCornerFlag=False,moveToFlag=False, confirmLocationFlag = False):
    """
    Moves the mouse to a specified location of an image on the screen and optionally clicks, within a specified timeout.

    :param file_path: String representing the file path of the image.
    :param x_offset: Integer representing the horizontal offset from the location.
    :param y_offset: Integer representing the vertical offset from the location.
    :param click_flag: Boolean indicating whether to click at the location (default: True).
    :param click_delay: Float representing the delay in seconds before clicking (default: 0).
    :param timeout: Integer representing the number of seconds to keep retrying the search.
    :param region_rectangle: Tuple representing the region where Pyautogui will search for the requested image
    :param confidence: Float representing how sure/accurate Pyautogui requires when searching for the requested image
    :param settle_delay: Integer representing the number of seconds that the program will pause after finding/clicking on the request image before moving onto the next action so things can settle
    """

    #We convert region_rectangle into a region here because we have to convert the dimensions of the rectangle into measurements that Pyautogui understands
    #Pyautogui region: (topCornerXValue, topCornerYValue, widthOfRectangle, heightOfRectangle)
    region = (region_rectangle[0],region_rectangle[1],region_rectangle[2] - region_rectangle[0],region_rectangle[3] - region_rectangle[1])


    #end_time is the time value in which we will stop searching for the object 
    end_time = time.time() + timeout
    while time.time() < end_time:
        for file_path in file_paths:
            
            try:
                location = pyautogui.locateCenterOnScreen(f"./Screenshots/{parent_directory}/{file_path}", 
                                                              confidence=confidence,
                                                              region=region, 
                                                              grayscale=grayScaleFlag)

                final_x, final_y = location[0] + x_offset, location[1] + y_offset
                if(moveToFlag):
                    pyautogui.moveTo(final_x, final_y)

                time.sleep(settle_delay)
                return ([file_path,location[0],location[1]])
                
            except pyautogui.ImageNotFoundException:
                    time.sleep(0.1)  # Short sleep to avoid high CPU usage
            except Exception as e:
                print(e)
                print("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")

                logging.critical(e)
                logging.critical("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
                
                #This will break out of the loop
                end_time = time.time()

    print("Timeout reached, could not find any of the requested images")
    logging.critical("Timeout reached, could not find any of the requested images")
    return ("",False, False)

def MoveToLocationListIndividualRegions(file_paths:list, parent_directory='ZBD_Videos', x_offset=0, y_offset=0, click_flag=False, double_click_flag = False, second_click_x_offset=0, second_click_y_offset=0, click_delay=0.0, timeout=120, region_rectangle_list=PHONE_SCREEN_REGION_RECTANGLE, confidence = 0.9, settle_delay=1, grayScaleFlag=False, topLeftCornerFlag=False,confirmLocationFlag = False):
    """
    Moves the mouse to a specified location of an image on the screen and optionally clicks, within a specified timeout.

    :param file_path: String representing the file path of the image.
    :param x_offset: Integer representing the horizontal offset from the location.
    :param y_offset: Integer representing the vertical offset from the location.
    :param click_flag: Boolean indicating whether to click at the location (default: True).
    :param click_delay: Float representing the delay in seconds before clicking (default: 0).
    :param timeout: Integer representing the number of seconds to keep retrying the search.
    :param region_rectangle_list: List of tuples representing the region where Pyautogui will search for the requested image
    :param confidence: Float representing how sure/accurate Pyautogui requires when searching for the requested image
    :param settle_delay: Integer representing the number of seconds that the program will pause after finding/clicking on the request image before moving onto the next action so things can settle
    """

    #end_time is the time value in which we will stop searching for the object 
    end_time = time.time() + timeout
    while time.time() < end_time:
        for file_path, region_rectangle in zip(file_paths,region_rectangle_list):
            
            try:
                #We convert region_rectangle into a region here because we have to convert the dimensions of the rectangle into measurements that Pyautogui understands
                #Pyautogui region: (topCornerXValue, topCornerYValue, widthOfRectangle, heightOfRectangle)
                #region = (region_rectangle[0],region_rectangle[1],region_rectangle[2] - region_rectangle[0],region_rectangle[3] - region_rectangle[1])

                location = pyautogui.locateCenterOnScreen(f"./Screenshots/{parent_directory}/{file_path}", 
                                                              confidence=confidence,
                                                              region=region_rectangle, 
                                                              grayscale=grayScaleFlag)

                #final_x, final_y = location[0] + x_offset, location[1] + y_offset
                #if(move_to_flag):
                #    pyautogui.moveTo(final_x, final_y)

                time.sleep(0.05)
                return ([file_path,location[0],location[1]])
                
            except pyautogui.ImageNotFoundException:
                    pass
                    #time.sleep(0.01)  # Short sleep to avoid high CPU usage
            except Exception as e:
                print(e)
                print("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")

                logging.critical(e)
                logging.critical("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
                
                #This will break out of the loop
                end_time = time.time()

    print("Timeout reached, could not find any of the requested images")
    logging.critical("Timeout reached, could not find any of the requested images")
    return ("",False, False)


#PRIMARY ADB AND PHONE INTERACTION FUNCTIONS

# Function to execute adb shell command
def adb_command(command):
    subprocess.run(['adb', 'shell'] + command.split())

# Function to scale pixel coodinates from the OBS computer screen to the phone screen
def scale_value(x, original_min, original_max, target_min, target_max):
    
    # Apply the scaling formula
    y = target_min + (x - original_min) * (target_max - target_min) / (original_max - original_min)
    return y

# Tap at specific coordinates
def tap(x, y, x_offset=0, y_offset=0,settle_delay=0):

    #Scale the coordinates from the computer screen to the phone screen
    x = scale_value(x + x_offset, PHONE_SCREEN_REGION_RECTANGLE[0], PHONE_SCREEN_REGION_RECTANGLE[2], 0, PIXEL_6_SCREEN_RESOLUTION[0])
    y = scale_value(y + y_offset, PHONE_SCREEN_REGION_RECTANGLE[1], PHONE_SCREEN_REGION_RECTANGLE[3],0, PIXEL_6_SCREEN_RESOLUTION[1])

    #Send the tap command to the phone through adb
    adb_command(f'input tap {x} {y}')
    time.sleep(settle_delay)

# Hold down a tap at specific coordinates
def hold(x, y, duration=2000, x_offset=0, y_offset=0, settle_delay = 0):

    #Scale the coordinates from the computer screen to the phone screen
    x = scale_value(x + x_offset, PHONE_SCREEN_REGION_RECTANGLE[0], PHONE_SCREEN_REGION_RECTANGLE[2], 0, PIXEL_6_SCREEN_RESOLUTION[0])
    y = scale_value(y + y_offset, PHONE_SCREEN_REGION_RECTANGLE[1], PHONE_SCREEN_REGION_RECTANGLE[3],0, PIXEL_6_SCREEN_RESOLUTION[1])

    #Send the hold command to the phone through adb
    adb_command(f'input swipe {x} {y} {x} {y} {duration}')

    time.sleep(settle_delay)

# Swipe from one set of coordinates to another (This functino does not scale the coordinates)
def swipe(x1, y1, x2, y2, duration=100, settle_delay=0):

    #Send the swipe command to the phone through adb
    adb_command(f'input swipe {x1} {y1} {x2} {y2} {duration}')
    time.sleep(settle_delay)

#SECONDARY ADB AND PHONE INTERACTION FUNCTIONS

# Function to view currently running apps
def view_running_apps():
    adb_command('input keyevent KEYCODE_APP_SWITCH')
    time.sleep(2.5)

# Function to go to the home screen
def go_to_home_screen():
    adb_command(f'input keyevent KEYCODE_HOME')
    time.sleep(2.5)

# Function to be used while viewing running apps. This function will swipe up to clear the app
def clear_app():
    #Swipe up to clear the app
    swipe(540, 1200, 540, 800, settle_delay=3)
    
    #Tap on the screen to return to the last open app
    tap(960, 430, settle_delay=2)

# Function to scroll up in the game
def scroll_up(x1 = 540, y1 = 800, x2 = 540, y2 = 1000, duration = 100, settle_delay=0.5):
    swipe(x1, y1, x2, y2, duration)
    time.sleep(settle_delay)

# Function to scroll down in the game
def scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 800, duration = 100, settle_delay=0.5):
    swipe(x1, y1, x2, y2, duration)
    time.sleep(settle_delay)

 

#COMPLEX FUNCTIONS

# Function to clear advertisements
# def clear_advertisement():

#     #Begin searching for any buttons that will skip, close, or advance the advertisement
#     print("Searching for advertisement buttons")
#     filePath, xCor, yCor = MoveToLocationList(
#     [
#     'x_button_1.png',
#     'x_button_2.png',
#     'x_button_3.png',
#     'x_button_4.png',
#     'x_button_5.png',
#     'x_button_6.png',
#     'x_button_7.png',
#     'x_button_8.png',
#     'x_button_9.png',
#     'x_button_10.png',
#     'x_button_11.png',
#     'x_button_12.png',
#     'x_button_13.png',
#     'x_button_14.png',
#     'x_button_15.png',
#     'x_button_16.png',
#     'x_button_17.png',
#     'x_button_18.png',
#     'x_button_19.png',
#     'x_button_20.png',
#     'x_button_21.png',
#     'x_button_22.png',
#     'x_button_23.png',
#     'x_button_24.png',
#     'x_button_25.png',
#     'x_button_26.png',
#     'x_button_27.png',
#     'x_button_28.png',
#     'x_button_29.png',
#     'x_button_30.png',
#     'x_button_31.png',
#     'x_button_32.png',
#     'google_play_store.png'],
#     settle_delay=0.5,confidence=0.90,timeout=120,grayScaleFlag=True,region_rectangle=(778,41,1167,835)
#     )

#     #If we find something, we proceed to click on it
#     if(filePath != ''):
#         #Tap on the button
#         print(f"Found {filePath}")
#         tap(xCor, yCor)

#         #If you find the Google Play Store icon, we assume we are in the store and we need to retun to the game
#         if(filePath == 'google_play_store.png'):
#             print("Google Play Store was opened. Closing the app and returning to the game")
#             #View currently running apps
#             view_running_apps()

#             #Clear the Google Play Store App
#             clear_app()
#             print("App has been cleared. We should be back in the game")
        
#         #Returning True if we managed to find a an advertisement button
#         return True
    
#     #If we don't find anything, we continue with the main while loop
#     else:
#         print("Couldn't find any advertisement buttons.")
#         return False

# Function to clear advertisements
def clear_advertisement():

    #Begin searching for any buttons that will skip, close, or advance the advertisement
    print("Searching for advertisement buttons")
    filePath, xCor, yCor = MoveToLocationList(
    [
    'ad_continue_button.png',
    'google_play_store.png',
    'x_button_1.png',
    'x_button_2.png',
    'x_button_3.png',
    'x_button_4.png',
    'x_button_5.png',
    'x_button_6.png',
    'x_button_7.png',
    'x_button_8.png',
    'x_button_9.png',
    'x_button_10.png',
    'x_button_11.png',
    'x_button_12.png',
    'x_button_13.png',
    'x_button_14.png',
    'x_button_15.png',
    'x_button_16.png',
    'x_button_17.png',
    'x_button_18.png',
    'x_button_19.png',
    'x_button_20.png',
    'x_button_21.png',
    'x_button_22.png',
    'x_button_23.png',
    'x_button_24.png',
    'x_button_25.png',
    'x_button_26.png',
    'x_button_27.png',
    'x_button_28.png',
    'x_button_29.png',
    'x_button_30.png',
    'x_button_31.png',
    'x_button_32.png',
    'x_button_33.png',
    'x_button_34.png',
    'x_button_35.png',
    'x_button_36.png',
    'x_button_37.png',
    'x_button_38.png',
    'x_button_39.png',
    'x_button_40.png',
    'x_button_41.png',
    'x_button_42.png',
    'x_button_43.png',
    'x_button_44.png',
    'x_button_45.png',
    'x_button_46.png',
    ],
    settle_delay=0.5,confidence=0.875,timeout=120,grayScaleFlag=True,region_rectangle=(704,23,1214,800)
    )

    #If we find something, we proceed to click on it
    if(filePath != ''):
        #Tap on the button
        print(f"Found {filePath}")
        tap(xCor, yCor)

        #If you find the Google Play Store icon, we assume we are in the store and we need to retun to the game
        if(filePath == 'google_play_store.png'):

            print("Google Play Store was opened. Closing the app and returning to the game")
            #View currently running apps
            view_running_apps()

            #Clear the Google Play Store App
            clear_app()
            print("App has been cleared. We should be back in the game")
            
            
        
        #Returning True if we managed to find a an advertisement button
        return True
    
    #If we don't find anything, we continue with the main while loop
    else:
        print("Couldn't find any advertisement buttons.")
        return False

# Function to reset the game if we are in an unknown state. (Typically used if we come across an advertisement we can't find the exit button for)
def reset_from_unknown_state():
    print("Resetting from unknown state")
    #Go to home screen
    go_to_home_screen()

    #Open running apps
    view_running_apps()

    #Clear the Bitcoin Miner app
    clear_app()

    #Open the Bitcoin Miner app

    #Attempt to find the Bitcoin Miner app
    bitcoin_miner_app, xCor, yCor = MoveToLocation('bitcoin_miner_app.png',timeout=5)
    
    #If the Bitcoin Miner app is found, open it by tapping on the app
    if bitcoin_miner_app != '':
        tap(xCor, yCor)
        print("Bitcoin Miner app has been opened")
        time.sleep(10)
    #If the Bitcoin Miner app is not found, then we kill the script so the program does not go haywire
    else:
        print("Stopping the script.")
        sys.exit()  # Terminates the script

# Function to prestige the game once we get the opportunity
def prestige():
    #Set a reference to the global variables upgrade_counter and mine_pickaxe_counter
    global upgrade_counter
    global mine_pickaxe_counter
    global ad_counter
    global current_map

    #Take a screenshot of the current screen
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pyautogui.screenshot(f"./Screenshots/Prestige/{timestamp}-prestige.png")

    #Attempt to find the prestige button
    print("Attempting to prestige")
    prestige_button, xCor, yCor = MoveToLocation('prestige_icon.png',timeout=5)

    #If the prestige button is found, we proceed to click on it
    if prestige_button != '':
        #Tap on the prestige button
        print("Prestige button found. Tapping on it")
        tap(xCor, yCor)
        
        #Attempt to find the please_wait indicator
        please_wait, xCor, yCor = MoveToLocation('please_wait_indicator.png',timeout=5)

        #If the please_wait indicator is found, then the prestige is not possible so we reset the upgrade_counter to 0
        if please_wait != '':
            print("Prestige cannot be performed. Resetting upgrade_counter and mine_pickaxe_counter to 0.")
            upgrade_counter = 0
            mine_pickaxe_counter = 0
            return(False)
        
        #If the please_wait indicator is not found, then the prestige should be possible so we proceed to find the sell button
        else:
            #Attempt to find the sell button
            sell_button, xCor, yCor = MoveToLocation('sell_button.png',timeout=5)

            #If the sell button is found, we proceed to click on it
            if sell_button != '':
                #Tap on the sell button
                print("Sell button found. Tapping on it")
                tap(xCor, yCor,settle_delay=1)

                #Attempt to find the keep button
                keep_button, xCor, yCor = MoveToLocation('keep_button.png',timeout=5)

                #If the keep button is found, we proceed to click on it
                if keep_button != '':
                    #Tap on the keep button
                    print("Keep button found. Tapping on it")
                    tap(xCor, yCor,settle_delay=1)

                    #Allow the prestige to commence and reset the upgrade_counter and mine_pickaxe_counter to 0
                    print("Prestige has commenced")
                    print("Waiting for 30 seconds for the prestige to complete")
                    time.sleep(30)
                    upgrade_counter = 0
                    mine_pickaxe_counter = 0
                    ad_counter = 0
                    current_map = 1
                    return(True)
    
    #If we get to this point, then the prestige has failed and we attempt to return to the main while loop
    print("Prestige has failed. Assuming we are in an advertisement")
    clear_advertisement()
    return(False)

# Function to find the location of the watch button and scroll down if it is not in view
def scroll_to_watch_button():

    #Initialize a counter to keep track of how many times we have scrolled down
    watch_button_scroll_counter = 0

    #Attempt to find the location of the watch button
    print("Attempting to find the location of the watch button")
    watch_button, xCor, yCor = MoveToLocation('watch_button.png',timeout=2)
    
    #If the watch button is not found, continue scrolling down until it is found or the counter reaches 8
    while(watch_button == "" and watch_button_scroll_counter < 8):
        #Scroll down slightly
        scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 925, settle_delay=1)
        
        #Attempt to find the location of the watch button
        print("Attempting to find the location of the watch button")
        watch_button, xCor, yCor = MoveToLocation('watch_button.png',timeout=2)
        
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
    go_to_home_screen()

    #Search for the ZBD app
    print("Searching for the ZBD app")
    zbd_app, xCor, yCor = MoveToLocation('zbd_app.png',timeout=8)

    #If the ZBD app is found, open it by tapping on the app
    if zbd_app != '':
        tap(xCor, yCor)
        print("ZBD app has been opened")
        time.sleep(10)
    
    #If the ZBD app is not found, then we kill the script so the program does not go haywire
    else:
        print("ZBD app not found. Stopping the script.")
        sys.exit()

    #We now want to search for an indication that the app is open
    print("Searching for an indication that the app has opened")
    app_open, xCor, yCor = MoveToLocation('zbd_app_has_loaded.png',timeout=5)
    
    #If we can't find the app open indication, we assume the app has not opened properly and we kill the script
    if app_open == "":
        print("ZBD app has not opened properly. Stopping the script.")
        sys.exit()

    
    #We now want to search for the earn icon
    print("Searching for the earn icon")
    earn_icon, xCor, yCor = MoveToLocation('earn_icon.png',timeout=5)

    #If we can't find the earn icon, we assume the app has not opened properly and we kill the script
    if earn_icon != "":
        print("Earn icon found. Tapping on it")
        tap(xCor, yCor)
        time.sleep(3)
    
    else:
        print("Earn icon not found. Stopping the script.")
        sys.exit()

    #Search for the watch button by scrolling down
    print("Searching for the watch button")
    scroll_to_watch_button()

    print("Beginning the watch video process")
    while True:

        filePath, xCor, yCor = MoveToLocation(
            'watch_button.png',settle_delay=1, timeout=5)
        
        if filePath == 'watch_button.png':
            tap(xCor, yCor)
            limit_image, xCor, yCor = MoveToLocation('limit_has_been_reached.png',settle_delay=1, timeout=10,region_rectangle=(725,156,800,232))
            if limit_image == 'limit_has_been_reached.png':
                print("The limit has been reached. Returning to home and stopping the script.")
                sys.exit()

        else:
            clear_advertisement()

            
