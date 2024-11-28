import pyautogui
import logging
import time
from dotenv import load_dotenv
import os
import subprocess
import sys
import ast


#Load the environment variables
load_dotenv()

##CONSTANTS
SCRCPY_REGION_RECTANGLE = ast.literal_eval(os.getenv("SCRCPY_REGION_RECTANGLE"))
PHONE_SCREEN_RESOLUTION = ast.literal_eval(os.getenv("PHONE_SCREEN_RESOLUTION"))
PHONE_MODEL = os.getenv("PHONE_MODEL")

##LOCATE IMAGES AND MOVE CURSOR TO LOCATION FUNCTIONS
def MoveToLocation(file_path:str, 
                   parent_directory,
                   x_offset=0, 
                   y_offset=0, 
                   timeout=120, 
                   region_rectangle=SCRCPY_REGION_RECTANGLE, 
                   confidence = 0.9, 
                   settle_delay=1, 
                   gray_scale_flag=False, 
                   top_left_corner_flag=False, 
                   time_out_error_message = True,
                   move_to_flag = False):

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
                                                        grayscale=gray_scale_flag)

            final_x, final_y = location[0] + x_offset, location[1] + y_offset
            if(move_to_flag):
                pyautogui.moveTo(final_x, final_y)
            
            time.sleep(settle_delay)
            return ([file_path,location[0],location[1]])
        
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)  # Short sleep to avoid high CPU usage
        except Exception as e:
            print(file_path)
            print(e)
            print("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
            
            logging.critical(e)
            logging.critical("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
            
    if time_out_error_message:
        print(f"Timeout reached, {file_path} not found.")
        logging.critical(f"Timeout reached, {file_path} not found.")   

    return ("",False, False)


def MoveToLocationList(file_paths:list, 
                        parent_directory,
                        x_offset=0, 
                        y_offset=0, 
                        timeout=120, 
                        region_rectangle=SCRCPY_REGION_RECTANGLE, 
                        confidence=0.9, 
                        settle_delay=1, 
                        gray_scale_flag=False, 
                        top_left_corner_flag=False,
                        time_out_error_message = True,
                        move_to_flag = False):
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
                                                              grayscale=gray_scale_flag)

                final_x, final_y = location[0] + x_offset, location[1] + y_offset
                if(move_to_flag):
                    pyautogui.moveTo(final_x, final_y)

                time.sleep(settle_delay)
                return ([file_path,location[0],location[1]])
                
            except pyautogui.ImageNotFoundException:
                    time.sleep(0.1)  # Short sleep to avoid high CPU usage
            except Exception as e:
                print(file_path)
                print(e)
                print("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")

                logging.critical(e)
                logging.critical("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
                
                #This will break out of the loop
                end_time = time.time()

    
    if time_out_error_message:

        print(f"Timeout reached, could not find any of the requested images: {str(file_paths)}")
        logging.critical(f"Timeout reached, could not find any of the requested images: {str(file_paths)}")

    return ("",False, False)


def MoveToLocationListIndividualRegions(file_paths:list, 
                                        parent_directory,
                                        timeout=120, 
                                        region_rectangle_list=[(0,0,1920,1200)] * 6, 
                                        confidence = 0.9, 
                                        settle_delay=1, 
                                        gray_scale_flag=False,
                                        top_left_corner_flag=False,
                                        time_out_error_message = True,
                                        move_to_flag = False):

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
                                                              grayscale=gray_scale_flag)

                if(move_to_flag):
                    pyautogui.moveTo(location[0], location[1])

                time.sleep(settle_delay)
                return ([file_path,location[0],location[1]])
                
            except pyautogui.ImageNotFoundException:
                    pass
                    
            except Exception as e:
                print(file_path)
                print(e)
                print("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")

                logging.critical(e)
                logging.critical("THERE IS AN ERROR MAKE SURE TO LOG THIS SOMEHOW. MAKE HASSAAN DO IT!")
                
                #This will break out of the loop
                end_time = time.time()

    if time_out_error_message:

        print(f"Timeout reached, could not find any of the requested images: {str(file_paths)}")
        logging.critical(f"Timeout reached, could not find any of the requested images: {str(file_paths)}")

    return ("",False, False)



##PRIMARY ADB AND PHONE INTERACTION FUNCTIONS

# Function to execute adb shell command
def adb_command(command):
    subprocess.run(['adb', 'shell'] + command.split())

# Function to scale pixel coodinates from the OBS computer screen to the phone screen
def scale_value(unscaled_value, original_min, original_max, target_min, target_max):
    
    # Apply the scaling formula
    scaled_value = target_min + (unscaled_value - original_min) * (target_max - target_min) / (original_max - original_min)
    return scaled_value

# Tap at specific coordinates
def tap(x, y, x_offset=0, y_offset=0,settle_delay=0):

    #Scale the coordinates from the computer screen to the phone screen
    x = scale_value(x + x_offset, 
                    SCRCPY_REGION_RECTANGLE[0], 
                    SCRCPY_REGION_RECTANGLE[2], 
                    0, 
                    PHONE_SCREEN_RESOLUTION[0])
    
    y = scale_value(y + y_offset, 
                    SCRCPY_REGION_RECTANGLE[1], 
                    SCRCPY_REGION_RECTANGLE[3],
                    0, 
                    PHONE_SCREEN_RESOLUTION[1])

    #Send the tap command to the phone through adb
    adb_command(f'input tap {x} {y}')
    time.sleep(settle_delay)

# Hold down a tap at specific coordinates
def hold(x, y, duration=2000, x_offset=0, y_offset=0, settle_delay = 0):

    #Scale the coordinates from the computer screen to the phone screen
    x = scale_value(x + x_offset, 
                    SCRCPY_REGION_RECTANGLE[0],
                    SCRCPY_REGION_RECTANGLE[2], 
                    0, 
                    PHONE_SCREEN_RESOLUTION[0])
    
    y = scale_value(y + y_offset, 
                    SCRCPY_REGION_RECTANGLE[1], 
                    SCRCPY_REGION_RECTANGLE[3],
                    0, 
                    PHONE_SCREEN_RESOLUTION[1])

    #Send the hold command to the phone through adb
    adb_command(f'input swipe {x} {y} {x} {y} {duration}')

    time.sleep(settle_delay)

# Swipe from one set of coordinates to another (This functino does not scale the coordinates)
def swipe(x1, y1, x2, y2, duration=100, settle_delay=0):

    #Send the swipe command to the phone through adb
    adb_command(f'input swipe {x1} {y1} {x2} {y2} {duration}')
    time.sleep(settle_delay)


##SECONDARY ADB AND PHONE INTERACTION FUNCTIONS

# Function to view currently running apps
def view_running_apps():
    adb_command('input keyevent KEYCODE_APP_SWITCH')
    time.sleep(2.5)

# Function to go to the home screen
def go_to_home_screen():
    adb_command('input keyevent KEYCODE_HOME')
    time.sleep(2.5)    

# Function to scroll up in the game
def scroll_up(x1=(PHONE_SCREEN_RESOLUTION[0] / 2),
              y1=(PHONE_SCREEN_RESOLUTION[1] / 2 - 200), 
              x2=(PHONE_SCREEN_RESOLUTION[0] / 2), 
              y2=(PHONE_SCREEN_RESOLUTION[1] / 2), 
              duration = 100, 
              settle_delay=0.5):
    
    swipe(x1, y1, x2, y2, duration)
    time.sleep(settle_delay)

# Function to scroll down in the game
def scroll_down(x1=(PHONE_SCREEN_RESOLUTION[0] / 2),
                y1=(PHONE_SCREEN_RESOLUTION[1] / 2), 
                x2=(PHONE_SCREEN_RESOLUTION[0] / 2), 
                y2=(PHONE_SCREEN_RESOLUTION[1] / 2 - 200), 
                duration = 100, 
                settle_delay=0.5):

    swipe(x1, y1, x2, y2, duration)
    time.sleep(settle_delay)



##COMPLEX FUNCTIONS

# Function to be used while viewing running apps. This function will swipe up to clear the app
def clear_app(unknown_state_flag=False):

    #If we are in an unknown state, we need to reset the state by clearing all apps and returning to the home screen
    if unknown_state_flag:
        
        #Swipe up to clear the app
        for x in range(3):
            swipe(x1=int(PHONE_SCREEN_RESOLUTION[0] * 0.1), 
                  y1=int(PHONE_SCREEN_RESOLUTION[1] / 2), 
                  x2=int(PHONE_SCREEN_RESOLUTION[0] * 0.9), 
                  y2=int(PHONE_SCREEN_RESOLUTION[1] / 2), 
                  settle_delay=1)

        #Attempt to find the clear all button
        clear_all_button, xCor, yCor = MoveToLocation(file_path='clear_all_button.png',
                                                      parent_directory="Phone_Images",
                                                      timeout=5, 
                                                      gray_scale_flag=True)
        
        #If the Clear All Button is not found we kill the script
        if clear_all_button == '':
            print("Clear all button was not found. Stopping the script.")
            sys.exit()  # Terminates the script

        #Otherwise, we tap on the Clear All Button
        else:
            tap(xCor, yCor, settle_delay=3)
    
    #If we are not in an unknown state, we just need to swipe up to clear the app
    #Usually only occurs when we are in Google Play Store
    else:
        #Depending on the phone model, swiping and clearing the app may be different
        
        if(PHONE_MODEL == "Samsung Galaxy S20"):
            #If we have a Samsung Galaxy S20, we need to swipe to left first once we view the currently running apps
            swipe(
                x1=int(PHONE_SCREEN_RESOLUTION[0] * 0.1), 
                y1=int(PHONE_SCREEN_RESOLUTION[1] / 2),
                x2=int(PHONE_SCREEN_RESOLUTION[0] * 0.9), 
                y2=int(PHONE_SCREEN_RESOLUTION[1] / 2),
                settle_delay=3)

       
        #At this point, we should be able to swipe up to clear the app
        
        #Swipe up to clear the app
        swipe(
            x1=int(PHONE_SCREEN_RESOLUTION[0] / 2),
            y1=int(PHONE_SCREEN_RESOLUTION[1]),
            x2=int(PHONE_SCREEN_RESOLUTION[0] / 2),
            y2=int(PHONE_SCREEN_RESOLUTION[1] * 0.66),
            settle_delay=3)

        #Tap on the screen to return to the last open app
        tap(
            x=int(PHONE_SCREEN_RESOLUTION[0] / 2), 
            y=int(PHONE_SCREEN_RESOLUTION[1] / 2), 
            settle_delay=2)

# Function to reset the game if we are in an unknown state. (Typically used if we come across an advertisement we can't find the exit button for)
def reset_from_unknown_state():
    print("Resetting from unknown state")
    #Go to home screen
    go_to_home_screen()

    #Open running apps
    view_running_apps()

    #Clear the Bitcoin Miner app
    clear_app(unknown_state_flag=True)

    #Open the Bitcoin Miner app

    #Attempt to find the Bitcoin Miner app
    bitcoin_miner_app, xCor, yCor = MoveToLocation(file_path='bitcoin_miner_app.png',
                                                   parent_directory="Phone_Images",
                                                   timeout=5)
    
    #If the Bitcoin Miner app is found, open it by tapping on the app
    if bitcoin_miner_app != '':
        tap(xCor, yCor)
        print("Bitcoin Miner app has been opened")
        time.sleep(10)
    #If the Bitcoin Miner app is not found, then we kill the script so the program does not go haywire
    else:
        print("Stopping the script.")
        sys.exit()  # Terminates the script


# Function to clear advertisement that appear in the game/app
def clear_advertisement():

    #Begin searching for any buttons that will skip, close, or advance the advertisement
    print("Searching for advertisement buttons")
    filePath, xCor, yCor = MoveToLocationList(
    [
    'ad_continue_button.png',
    'ad_continue_button_2.png',
    'ad_skip_button.png',
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
    'google_play_store.png'],
    parent_directory="Advertisements",
    settle_delay=0.5,confidence=0.90,timeout=120,gray_scale_flag=True,
    region_rectangle=(
        SCRCPY_REGION_RECTANGLE[0],
        SCRCPY_REGION_RECTANGLE[1],
        SCRCPY_REGION_RECTANGLE[2],
        int(SCRCPY_REGION_RECTANGLE[3] * 0.5)
    )
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

