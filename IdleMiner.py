
from calendar import c
import subprocess
from turtle import clear, up
import pyautogui
import logging
import time
import sys
from discord_webhook import DiscordWebhook
import datetime

##CONSTANTS
PHONE_SCREEN_REGION_RECTANGLE = (791,96,1128,808)
PIXEL_6_SCREEN_RESOLUTION = (1080, 2400)

#LOCATE IMAGES AND MOVE CURSOR TO LOCATION FUNCTIONS
def MoveToLocation(file_path:str, parent_directory='Idle_Miner', x_offset=0, y_offset=0, click_flag=False, double_click_flag = False, second_click_x_offset=0, second_click_y_offset=0, click_delay=0.0, double_click_delay=1.0, timeout=120, region_rectangle=PHONE_SCREEN_REGION_RECTANGLE, confidence = 0.9, settle_delay=1, grayScaleFlag=False, topLeftCornerFlag=False, timeoutErrorMessage = True, confirmLocationFlag = False, transitionConfirmationImage = ""):
    global move_to_flag
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
            if(move_to_flag):
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

def MoveToLocationList(file_paths:list, parent_directory='Idle_Miner', x_offset=0, y_offset=0, click_flag=False, double_click_flag = False, second_click_x_offset=0, second_click_y_offset=0, click_delay=0.0, timeout=120, region_rectangle=PHONE_SCREEN_REGION_RECTANGLE, confidence = 0.9, settle_delay=1, grayScaleFlag=False, topLeftCornerFlag=False,confirmLocationFlag = False):
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
                if(move_to_flag):
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

def MoveToLocationListIndividualRegions(file_paths:list, parent_directory='Idle_Miner', x_offset=0, y_offset=0, click_flag=False, double_click_flag = False, second_click_x_offset=0, second_click_y_offset=0, click_delay=0.0, timeout=120, region_rectangle_list=PHONE_SCREEN_REGION_RECTANGLE, confidence = 0.9, settle_delay=1, grayScaleFlag=False, topLeftCornerFlag=False,confirmLocationFlag = False):
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

def MoveToLocationAllInstances(file_path:str, parent_directory='Idle_Miner', x_offset=0, y_offset=0, click_flag=False, double_click_flag = False, second_click_x_offset=0, second_click_y_offset=0, click_delay=0.0, double_click_delay=1.0, timeout=120, region_rectangle=PHONE_SCREEN_REGION_RECTANGLE, confidence = 0.9, settle_delay=1, grayScaleFlag=False, topLeftCornerFlag=False, timeoutErrorMessage = True, confirmLocationFlag = False, transitionConfirmationImage = ""):
    global move_to_flag
    # We convert region_rectangle into a region here because we have to convert the dimensions of the rectangle into measurements that Pyautogui understands
    # Pyautogui region: (topCornerXValue, topCornerYValue, widthOfRectangle, heightOfRectangle)
    region = (region_rectangle[0],region_rectangle[1],region_rectangle[2] - region_rectangle[0],region_rectangle[3] - region_rectangle[1])

    # end_time is the time value in which we will stop searching for the object 
    end_time = time.time() + timeout
    locations = []
    while time.time() < end_time:
        try:
            location = pyautogui.locateAllOnScreen(f"./Screenshots/{parent_directory}/{file_path}", 
                                                    confidence=confidence, 
                                                    region=region, 
                                                    grayscale=grayScaleFlag)
            for loc in location:
                final_x, final_y = loc.left + loc.width // 2 + x_offset, loc.top + loc.height // 2 + y_offset
                locations.append([file_path, final_x, final_y])
                if move_to_flag:
                    pyautogui.moveTo(final_x, final_y)
                time.sleep(settle_delay)
            if locations:
                return locations
        
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

    return locations if locations else ("", False, False)

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
    x = scale_value(x, 790, 1128, 0, 1080)
    y = scale_value(y, 57, 808,0, 2400)

    #Send the tap command to the phone through adb
    adb_command(f'input tap {x + x_offset} {y + y_offset}')
    time.sleep(settle_delay)

# Hold down a tap at specific coordinates
def hold(x, y, duration=2000, x_offset=0, y_offset=0, settle_delay = 0):

    #Scale the coordinates from the computer screen to the phone screen
    x = scale_value(x, 790, 1128, 0, 1080)
    y = scale_value(y, 57, 808,0, 2400)

    #Send the hold command to the phone through adb
    adb_command(f'input swipe {x + x_offset} {y + y_offset} {x + x_offset} {y + y_offset} {duration}')

    time.sleep(settle_delay)

# Swipe from one set of coordinates to another (This function does not scale the coordinates)
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
def clear_app(return_to_home_screen=False):
    #Swipe up to clear the app
    swipe(540, 1200, 540, 800, settle_delay=3)
    
    if return_to_home_screen:
        #Return to the home screen
        go_to_home_screen()
    
    else:
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
def clear_advertisement():

    #Begin searching for any buttons that will skip, close, or advance the advertisement
    print("Searching for advertisement buttons")
    filePath, xCor, yCor = MoveToLocationList(
    [
    'ad_continue_button.png',
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
    'x_button_47.png',
    'google_play_store.png'],
    settle_delay=0.5,confidence=0.90,timeout=120,grayScaleFlag=True,region_rectangle=(778,41,1167,835)
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

    #Clear the Idle Miner app
    clear_app(return_to_home_screen=True)

    #Open the Idle Miner app

    #Attempt to find the Idle Miner app
    idle_miner_app, xCor, yCor = MoveToLocation('idle_miner_app.png',timeout=5)
    
    #If the Idle Miner app is found, open it by tapping on the app
    if idle_miner_app != '':
        tap(xCor, yCor)
        print("Idle Miner app has been opened")
        time.sleep(10)
    #If the Idle Miner app is not found, then we kill the script so the program does not go haywire
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
    print("Prestige has failed. Assuming we are in a screen that is not allowing us to prestige")
    pyautogui.screenshot(f"./Screenshots/Unknown_States_Bitcoin_Miner/{timestamp}-prestige_failed.png")
    return(False)

# Function to find the location of the gold server and scroll down if it is not in view
def scroll_to_golden_server():
    #Set a reference to the global variable gold_server_not_in_view
    global gold_server_not_in_view

    #Initialize a counter to keep track of how many times we have scrolled down
    gold_server_scroll_counter = 0

    #Attempt to find the location of the gold server
    print("Attempting to find the location of the gold server")
    gold_server_icon, xCor, yCor = MoveToLocation('gold_server_icon.png',timeout=2)
    
    #If the gold server is not found, continue scrolling down until it is found or the counter reaches 8
    while(gold_server_icon == "" and gold_server_scroll_counter < 8):
        #Scroll down slightly
        scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 950, settle_delay=0.5)
        
        #Attempt to find the location of the gold server
        print("Attempting to find the location of the gold server")
        gold_server_icon, xCor, yCor = MoveToLocation('gold_server_icon.png',timeout=2)
        
        #If the gold server is not found, increment the counter
        if gold_server_icon == "":
            #Increment the counter 
            gold_server_scroll_counter += 1

        #If the gold server is found, break out of the loop and set the gold_server_not_in_view flag to False
        else:
            print("Gold Server has been found. No longer scrolling")
            gold_server_not_in_view = False
            
            #Before breaking out of the loop, we just want to settle for a bit before proceeding
            time.sleep(2.5)
            return None

    #If we can't find the gold server after 8 scrolls, we assume we are in an advertisement
    if gold_server_scroll_counter == 8:
        print("Gold Server has not been found after 8 scrolls. We are most likely viewing an advertisement.")
        gold_server_not_in_view = True
    
    #Otherwise, we assume the gold server is in view and we don't need to scroll
    else:
        print("Gold Server is in view. No need to scroll")
        gold_server_not_in_view = False
   


if __name__ == "__main__":

    #Initialize global variables
    move_to_flag = False
    # gold_server_not_in_view = True
    # mine_pickaxe_counter = 0
    # upgrade_counter = 0 
    ad_counter = 0
    idle_counter = 0
    upgrade_fail_counter = 0
    upgrade_success_counter = 0
    # upgrade_counter_limit = 8
    # mine_pickaxe_counter_limit = 15
    # current_map = 1
    # DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1301305402532827156/3YfReb2XbGqZHk3QMPvpuwl6P4fveX_3ONepieeu05SqpT6l5UZ3Nh2Ml3UD74XR465G"
    # webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    # TIME_BETWEEN_PRESTIGES = datetime.timedelta(seconds=1800)
    # first_run_flag = False
    
    #These are functions that I use for debugging occasionally
    # view_running_apps()
    # clear_app()
    #prestige()
    #reset_from_unknown_state()

    #After opening the app, watch an ad to double the income from idle mining
    #CODE TO WATCH AN AD AND DOUBLE THE INCOME

    #Set the time since the last prestige as the current time
    #time_since_last_double_speed = None
    time_since_last_double_speed = datetime.datetime.now()

    scroll_photo = pyautogui.screenshot(region=(903,766,1015,804))

    #Main while loop
    while(True):
        
        if upgrade_success_counter >= 10:
            print("Upgrade success counter has reached 10. Resetting the app.")
            reset_from_unknown_state()
            upgrade_success_counter = 0
            upgrade_fail_counter = 0

        #Obtain the current time
        current_time = datetime.datetime.now()

        #If the time since the last double speed is None, or more than 5 minutes have passed since the last double speed, we attempt to double the speed
        if time_since_last_double_speed == None or current_time - time_since_last_double_speed >= datetime.timedelta(minutes=5):
            print("5 minutes have passed since the last double speed. Attempting to double the speed")

            #Attempt to find the 2x speed button
            double_speed_button, xCor, yCor = MoveToLocation('double_speed.png',timeout=5)
            
            #If the 2x speed button is found, we tap on it
            if double_speed_button != '':
                #Tap on the 2x speed button
                print("2x speed button found. Tapping on it")
                tap(xCor, yCor, settle_delay=1, x_offset=-95)

                #Set the time since the last double speed to the current time
                time_since_last_double_speed = datetime.datetime.now()
                
                clear_advertisement()
            
            #If the 2x speed button is not found, we assume we are in an advertisement
            else:
                print("2x speed button not found. Assuming we are in an advertisement")

        #Attempt to find the primary buttons
        print("Searching for primary buttons")
        filePath, xCor, yCor = MoveToLocationList([
                                    'done_button.png',
                                    'continue_button.png',
                                    'select_button.png',
                                    'next_level.png',
                                    'five_times_gift_reward_button.png',
                                    'close_menu_button.png',
                                    'clothing_gift.png',
                                    'backside_clothing_token.png',
                                    'floating_gift_icon.png',
                                    'upgrade_production.png',
                                    'upgrade_ore_arrow.png',
                                    #'upgrade_ore_arrow_two.png',
                                    'upgrade_ore_arrow_three.png',
                                    'idle_icon.png'
                                    ],timeout=5,settle_delay=0,confidence=0.8)
        

        #If we find a floating_gift_icon, we tap on it
        if(filePath == 'floating_gift_icon.png'):
            #Tap on the floating gift icon
            print("Tapping on the floating gift icon")
            tap(xCor, yCor, settle_delay=1)

            #We might add to this later in order to account for the gift floating around the screen

            #Attempt to find the five times claim button
            five_times_claim_button, xCor, yCor = MoveToLocation('five_times_gift_reward_button.png',timeout=5)

            #If the five times claim button is found, we tap on it
            if five_times_claim_button != '':
                #Tap on the five times claim button
                print("Tapping on the five times claim button")
                tap(xCor, yCor, settle_delay=1)

                clear_advertisement()
            else:
                print("Five times claim button not found. Assuming we are in an advertisement.")

        #If the filePath contains the word close, we tap on the close button
        elif(filePath == 'close_menu_button.png'):
            #Tap on the close button
            print("Tapping on the close button")
            tap(xCor, yCor, settle_delay=1)

        #If the filePath contains the word crate, we tap on the crate
        elif filePath[0:5] == "crate":
            #Tap on the crate
            print("Tapping on the crate")
            tap(xCor, yCor, y_offset=-50, settle_delay=1)

        #If the filePath is upgrade_production.png, we attempt to upgrade production
        elif filePath == 'upgrade_production.png':
            #Tap on the upgrade production button
            print("Tapping on the upgrade production button")
            tap(xCor, yCor, settle_delay=1)

            #Attempt to find the an available upgrade button
            upgrade_button, xCor, yCor = MoveToLocation('upgrade_production_available_button.png',timeout=5)

            #If the upgrade button is found, we tap on it
            if upgrade_button != '':
                #Tap on the upgrade button
                print("Tapping on the upgrade button")
                tap(xCor, yCor, settle_delay=0.25)
                upgrade_success_counter += 1

            

        #If the filePath is upgrade_ore_arrow.png, we attempt to upgrade the ore
        elif 'upgrade_ore_arrow' in filePath:
            # upgrade_ore_arrow_list = MoveToLocationAllInstances('upgrade_ore_arrow.png',timeout=5,confidence=0.82)

            # #If the upgrade_ore_arrow_list is not empty, we iterate through the list and tap on each upgrade ore arrow
            # for upgrade_ore_arrow in upgrade_ore_arrow_list:
            #     #Tap on the upgrade ore arrow
            #     print("Tapping on the upgrade ore arrow")
            #     tap(upgrade_ore_arrow[1], upgrade_ore_arrow[2], settle_delay=1)

            #Tap on the upgrade ore arrow
            print("Tapping on the upgrade ore arrow")
            tap(xCor, yCor, x_offset=10, settle_delay=1)
            
            for counter in range(10):
                #Attempt to find the an available upgrade ore available icon
                upgrade_button, upgrade_xCor, upgrade_yCor = MoveToLocation('upgrade_ore_available.png',timeout=1.5,region_rectangle=(xCor-90,yCor-85,xCor+90,yCor),settle_delay=0.1)

                #If the upgrade button is found, we tap on it
                if upgrade_button != '':
                    #Tap on the upgrade button
                    print("Tapping on the upgrade button")
                    tap(upgrade_xCor, upgrade_yCor, settle_delay=0.1)
                    upgrade_fail_counter = 0
                    upgrade_success_counter += 0.1
                    
                else:
                    print("Upgrade button not found, assuming that the ore cannot be upgraded anymore at this time.")
                    upgrade_fail_counter += 1

                    #There is a bug in which, if the upgrade ore arrow is tapped on the upgrade ore button will not appear. Only way to fix this is to reset the app
                    if upgrade_fail_counter >= 10:
                        print("Upgrade fail counter has reached 10. Resetting the app.")
                        reset_from_unknown_state()
                        upgrade_fail_counter = 0
                        upgrade_success_counter = 0
                    break
                    
            #Tap on the upgrade ore arrow again to close the upgrade menu
            tap(xCor, yCor, settle_delay=1)

        #If the filePath is five_times_gift_reward_button.png, we tap on the five times claim button
        #This usually appears if we tap on the floating gift icon accidentally
        elif(filePath == 'five_times_gift_reward_button.png'):
            print("Tapping on the five times claim button")
            tap(xCor, yCor, settle_delay=1)

        #If the filePath is idle_icon.png, then we just assume there is nothing to do and we continue with the main loop
        elif(filePath == 'idle_icon.png'):
            print("Idle icon found. Assuming there is nothing to do at this time.")
            idle_counter += 1

            if(idle_counter >= 12):
                print("Idle counter has reached 12. Scrolling down slightly and reset the idle counter")
                scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 850, settle_delay=0.5)
                idle_counter = 0
            
            continue
        
        #If the filePath is tip_one.png or tip_two.png, we tap on the tip
        elif(filePath == 'tip_one.png' or filePath == 'tip_two.png' or filePath == 'tip_three.png'):
            print("Tapping on the tip")
            tap(xCor, yCor, settle_delay=1)

        #If the filePath is select_next_level.png, we tap on the select next level button
        elif(filePath == 'select_button.png'):
            print("Tapping on the select next level button")
            tap(xCor, yCor, settle_delay=1)
        
        #If the filePath is continue_button.png, we tap on the continue button
        elif(filePath == 'continue_button.png'):
            print("Tapping on the continue button")
            tap(xCor, yCor, settle_delay=1)

        #If the filePath is next_level.png, we tap on the upgrade production available button
        elif(filePath == 'next_level.png'):
            print("Tapping on the next level button")
            tap(xCor, yCor, settle_delay=1)

        #If the filePath is clothing_gift.png, we tap on the clothing gift
        elif(filePath == 'clothing_gift.png' or filePath == 'backside_clothing_token.png'):
            print("Tapping on the clothing gift")
            tap(xCor, yCor, settle_delay=5)

            backside_clothing_token, xCor, yCor = MoveToLocation('backside_clothing_token.png',timeout=5)

            #If the backside_clothing_token is found, we tap on it
            if backside_clothing_token != '':
                print("Backside clothing token found. Tapping on it")
                tap(xCor, yCor, settle_delay=1)

            #This is a tap to close the clothing gift menu
            tap(xCor, yCor, settle_delay=1)

        #If we don't find any primary buttons, we assume we're in an advertisement and proceed to clear it    
        else:    
            #Call the clear advertisement function
            #If we find an advertisement button, we reset the ad_counter to 0
            if(clear_advertisement()):
                ad_counter = 0
            
            #If we don't find any advertisement buttons, we increment the ad_counter
            else:
                ad_counter += 1

            print(f"Ad Counter is {ad_counter}")



            