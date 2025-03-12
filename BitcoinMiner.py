import random
import pyautogui
import time
from discord_webhook import DiscordWebhook
import datetime
import os
import sys
import ast
import NavigationFunctions as nf


def secondary_image_function(instance_region_rectangle, serial_number, ad_counter):
    #Attempt to find the secondary buttons
            print("Searching for secondary buttons")
            filePath, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                        'reset_indicator.png',
                                        'store_x_button.png',
                                        'manager_recruit_x_button.png',
                                        'manager_menu_x_button.png',
                                        'development_menu_x_button.png',
                                        'map_select_x_button.png',
                                        'welcome_back_x_button.png',
                                        'portfolio_x_button.png',
                                        'daily_streak_collect_button.png',
                                        'daily_streak_ok_button.png',
                                        'chest_collect_button.png',
                                        ],
                                        parent_directory='Bitcoin_Miner',
                                        region_rectangle=instance_region_rectangle,
                                        timeout=5,settle_delay=0.01,confidence=0.85,gray_scale_flag=False)

            if(filePath == "reset_indicator.png"):
                #Pause execution for 3 seconds
                time.sleep(3)
            
                #Attempt to find the reset indicator again
                reset_indicator, xCor, yCor = nf.MoveToLocation(file_path='reset_indicator.png',
                                                                parent_directory='Bitcoin_Miner',
                                                                timeout=5,
                                                                region_rectangle=instance_region_rectangle,
                                                                confidence=0.95)
                
                #If the reset indicator is found, we reset the game
                if reset_indicator != '':
                    print("Reset indicator found. Resetting the game")
                    #Reset from unknown state
                    nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle, app_icon="bitcoin_miner_app")

                #Reset the ad_counter to 0
                ad_counter = 0

            elif "_button.png" in filePath:
                #Tap on found primary button
                print(f"Tapping on {filePath}")
                nf.tap(xCor, yCor, serial=serial_number, region_rectangle=instance_region_rectangle)
                
                #Reset the ad_counter to 0
                ad_counter = 0


            #If we can't find Secondary buttons, then we assume we're in an advertisement and proceed to clear it    
            else:
                #Call the clear advertisement function
                #If we find an advertisement button, we reset the ad_counter to 0
                if(nf.clear_advertisement_2(timeout=90,serial=serial_number, region_rectangle=instance_region_rectangle)):
                    ad_counter += 1
                
                #If we don't find any advertisement buttons, we increment the ad_counter
                else:
                    nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle, app_icon="bitcoin_miner_app")
                

            return ad_counter


# Function to prestige the game once we get the opportunity
def prestige(serial=None, instance_region_rectangle=nf.SCRCPY_REGION_RECTANGLE):
    #Set a reference to the global variables upgrade_counter and mine_pickaxe_counter
    global upgrade_counter
    global mine_pickaxe_counter
    global ad_counter
    global current_map

    #Take a screenshot of the current screen
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #pyautogui.screenshot(f"./Screenshots/Prestige/{timestamp}-prestige.png")

    #Attempt to find the prestige button
    print("Attempting to prestige")
    prestige_button, xCor, yCor = nf.MoveToLocation(file_path='prestige_icon.png',
                                                    parent_directory='Bitcoin_Miner',
                                                    region_rectangle=instance_region_rectangle,
                                                    confidence=0.80,
                                                    timeout=5)

    #If the prestige button is found, we proceed to click on it
    if prestige_button != '':
        #Tap on the prestige button
        print("Prestige button found. Tapping on it")
        nf.tap(xCor, yCor,serial=serial, region_rectangle=instance_region_rectangle)
        
        #Attempt to find the please_wait indicator
        please_wait, xCor, yCor = nf.MoveToLocation(file_path='prestige_please_wait_indicator.png',
                                                    parent_directory='Bitcoin_Miner',
                                                    region_rectangle=instance_region_rectangle,
                                                    timeout=5)

        #If the please_wait indicator is found, then the prestige is not possible so we reset the upgrade_counter to 0
        if please_wait != '':
            print("Prestige cannot be performed. Resetting upgrade_counter and mine_pickaxe_counter to 0.")
            upgrade_counter = 0
            mine_pickaxe_counter = 0
            return(False)
        
        #If the please_wait indicator is not found, then the prestige should be possible so we proceed to find the sell button
        else:
            #Attempt to find the sell button
            sell_button, xCor, yCor = nf.MoveToLocation(file_path='prestige_sell_button.png',
                                                        parent_directory='Bitcoin_Miner',
                                                        timeout=5,
                                                        region_rectangle=instance_region_rectangle)

            #If the sell button is found, we proceed to click on it
            if sell_button != '':
                #Tap on the sell button
                print("Sell button found. Tapping on it")
                nf.tap(xCor, yCor,settle_delay=1,serial=serial, region_rectangle=instance_region_rectangle)

                #Attempt to find the keep button
                keep_button, xCor, yCor = nf.MoveToLocation(file_path='prestige_keep_button.png',
                                                            parent_directory='Bitcoin_Miner',
                                                            timeout=5,
                                                            confidence=0.75,
                                                            region_rectangle=instance_region_rectangle)

                #If the keep button is found, we proceed to click on it
                if keep_button != '':
                    #Tap on the keep button
                    print("Keep button found. Tapping on it")
                    nf.tap(xCor, yCor,settle_delay=1,serial=serial, region_rectangle=instance_region_rectangle)

                    #Attempt to find the continue button
                    continue_button, xCor, yCor = nf.MoveToLocation(file_path='prestige_continue_button.png',
                                                            parent_directory='Bitcoin_Miner',
                                                            timeout=5,
                                                            confidence=0.75,
                                                            region_rectangle=instance_region_rectangle)
                    
                    #If the continue button is found, we proceed to click on it
                    if continue_button != '':
                        nf.tap(xCor, yCor,settle_delay=1,serial=serial, region_rectangle=instance_region_rectangle)

                    
                    #Attempt to find the prestige skip button
                    skip_button, xCor, yCor = nf.MoveToLocation(file_path='prestige_skip_button.png',
                                                            parent_directory='Bitcoin_Miner',
                                                            timeout=5,
                                                            confidence=0.75,
                                                            region_rectangle=instance_region_rectangle)
                    
                    #If the skip button is found, we proceed to click on it
                    if skip_button != '':
                        nf.tap(xCor, yCor,settle_delay=1,serial=serial, region_rectangle=instance_region_rectangle)


                    # counter = 0
                    # while counter < 5:
                    #     #Attempt to find the 2x income button
                    #     income_button, xCor, yCor = nf.MoveToLocation(file_path='2x_income_button.png',
                    #                                                 parent_directory='Bitcoin_Miner',
                    #                                                 timeout=30,
                    #                                                 confidence=0.75,
                    #                                                 region_rectangle=instance_region_rectangle)
                        
                    #     #If the 2x income button is found, we proceed to click on it
                    #     if income_button != '':
                    #         nf.tap(xCor, yCor,settle_delay=1,serial=serial, region_rectangle=instance_region_rectangle)
                    #         counter += 1

                    #         print(f"2x Income button found. Tapping on it. Counter is at {counter}")

                    #     else:
                    #         #Attempt to find the coin fragment icon
                    #         coin_fragment_icon, xCor, yCor = nf.MoveToLocation(file_path='coin_fragment_icon.png',
                    #                                                         parent_directory='Bitcoin_Miner',
                    #                                                         timeout=5,
                    #                                                         region_rectangle=(((instance_region_rectangle[0] + instance_region_rectangle[2])//2),
                    #                                                                             instance_region_rectangle[1],
                    #                                                                             instance_region_rectangle[2],
                    #                                                                             ((instance_region_rectangle[1] + instance_region_rectangle[3])//2))
                    #                                                         )
                            
                    #         #If the coin fragment icon is not found, we break the loop and assume we are in an advertisement
                    #         if coin_fragment_icon == '':
                    #             print("Coin Fragment icon is not found. Assuming we are in an advertisement")
                    #             nf.clear_advertisement_2(timeout=60,serial=serial, region_rectangle=instance_region_rectangle)

                    #         else:
                    #             print("Found Coin Fragment icon but could not find 2x Income button. Assuming we have reacehd the limit 2x income")
                    #             counter = 5


                    upgrade_counter = 0
                    mine_pickaxe_counter = 0
                    ad_counter = 0
                    current_map = 1
                    return(True)
    
    else:
        #Call the clear advertisement function
        #If we find an advertisement button, we reset the ad_counter to 0
        if(nf.clear_advertisement_2(timeout=90,serial=serial_number, region_rectangle=instance_region_rectangle)):
            ad_counter += 1
        
        #If we don't find any advertisement buttons, we increment the ad_counter
        else:
            nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle, app_icon="bitcoin_miner_app")


    #If we get to this point, then the prestige has failed and we attempt to return to the main while loop
    current_time = datetime.datetime.now()
    print(f"Prestige has failed. Assuming we are in a screen that is not allowing us to prestige. Time: {current_time}")
    webhook.content = f"Prestige has failed. Assuming we are in a screen that is not allowing us to prestige. Time: {current_time}"
    webhook.execute()
    pyautogui.screenshot(f"./Screenshots/Unknown_States_Bitcoin_Miner/{timestamp}-prestige_failed.png")
    return(False)

# Function to find the location of the gold server and scroll down if it is not in view
def scroll_to_golden_server(serial=None, instance_region_rectangle=nf.SCRCPY_REGION_RECTANGLE):
    #Set a reference to the global variable gold_server_not_in_view
    global gold_server_not_in_view

    #Initialize a counter to keep track of how many times we have scrolled down
    gold_server_scroll_counter = 0

    #Attempt to find the location of the gold server
    print("Attempting to find the location of the gold server")
    gold_server_icon, xCor, yCor = nf.MoveToLocation(file_path='gold_server_icon.png',
                                                     parent_directory='Bitcoin_Miner',
                                                     region_rectangle=(
                                                           instance_region_rectangle[0],
                                                           instance_region_rectangle[1] + instance_region_rectangle[3]//3,
                                                           instance_region_rectangle[2],
                                                           instance_region_rectangle[3]
                                                         ),
                                                     timeout=2)
    
    if gold_server_icon != "":
        print("Gold Server has been found. No need to scroll")
        gold_server_not_in_view = False
        return True
    
    #If the gold server is not found, continue scrolling down until it is found or the counter reaches 8
    while(gold_server_icon == "" and gold_server_scroll_counter < 32):

        #Attempt to find the coin fragment icon
        coin_fragment_icon, xCor, yCor = nf.MoveToLocation(file_path='coin_fragment_icon.png',
                                                           parent_directory='Bitcoin_Miner',
                                                           timeout=5,
                                                           region_rectangle=(((instance_region_rectangle[0] + instance_region_rectangle[2])//2),
                                                                             instance_region_rectangle[1],
                                                                             instance_region_rectangle[2],
                                                                             ((instance_region_rectangle[1] + instance_region_rectangle[3])//2))
                                                           )
        
        #If the coin fragment icon is not found, we break the loop and assume we are in an advertisement
        if coin_fragment_icon == '':
            print("Coin Fragment icon is not found. Assuming we are in an advertisement")
            gold_server_not_in_view = True
            return False
        
        else:
            print("Found Coin Fragment icon. Scrolling down")

        #Scroll down slightly
        nf.scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 950, settle_delay=0.5,serial=serial)
        
        #Attempt to find the location of the gold server
        print("Attempting to find the location of the gold server")
        gold_server_icon, xCor, yCor = nf.MoveToLocation(file_path='gold_server_icon.png',
                                                         parent_directory='Bitcoin_Miner',
                                                         region_rectangle=(
                                                           instance_region_rectangle[0],
                                                           instance_region_rectangle[1] + instance_region_rectangle[3]//2,
                                                           instance_region_rectangle[2],
                                                           instance_region_rectangle[3]
                                                         ),
                                                         timeout=2)
        
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
            return True

    #If we can't find the gold server after 32 scrolls, we assume we are in an advertisement
    print("Gold Server has not been found after 32 scrolls. We are most likely viewing an advertisement.")
    gold_server_not_in_view = True
    return False


def prestige_and_farming(time_between_prestiges, time_since_last_prestige,current_map,disable_farm,serial=None, instance_region_rectangle=nf.SCRCPY_REGION_RECTANGLE, ad_counter = 0):

        current_time = datetime.datetime.now()

        #If 30 minutes have passed since the last prestige or the prestige ready icon was found, we attempt to prestige
        if current_time - time_since_last_prestige >= time_between_prestiges and not disable_farm:
            print("30 MINUTES or Prestige Ready Icon was found. Attempting to perform a prestige")
            if(prestige(serial=serial, instance_region_rectangle=instance_region_rectangle)):
                return (True)

        #If 30 minutes have not passed since the last prestige, we'll attempt to farm gifts and satoshis
        else:
            print("30 minutes have not passed since the last prestige. We will attempt to farm gifts and satoshis.")
            
            end_time = time_since_last_prestige + time_between_prestiges
            while(datetime.datetime.now() < end_time or disable_farm):
                    
                    #If we have been stuck in an advertisement for too long, we assume we are in an unknown state and attempt to reset
                    if ad_counter >= ad_counter_limit:
                        print("Assuming we have been stuck in an advertisement for too long. Attempting to reset")

                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                        #Send Discord message
                        webhook.content = f"Encountered an unknown advertisement. Attempting to reset. Make sure to add advertisement to the list of images. Time: {timestamp}"
                        webhook.execute()

                        #Take a screenshot of the unknown advertisement
                        pyautogui.screenshot(f"./Screenshots/Unknown_Advertisements/{timestamp}-unknown_advertisement.png")

                        #Reset from unknown state
                        nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle, app_icon="bitcoin_miner_app")


                    #Attempt to find the following images
                    file_path, xCor, yCor = nf.MoveToLocationListIndividualRegions(
                        file_paths=['prestige_icon_ready.png',
                                    'manager_ability_magnet.png', 
                                    'manager_ability_power_up.png',
                                    'top_of_screen_indicator.png',
                                    'obtain_gift.png',
                                    'chest_collect_button.png'
                                    ],
                        region_rectangle_list=[((instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[1], instance_region_rectangle[2], instance_region_rectangle[3]//2),
                                              (instance_region_rectangle[0], instance_region_rectangle[1], (instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[3]),
                                              (instance_region_rectangle[0], instance_region_rectangle[1], (instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[3]),
                                              (instance_region_rectangle[2] - 160, instance_region_rectangle[1] + 350, instance_region_rectangle[2], instance_region_rectangle[3]//2),
                                              (instance_region_rectangle[0], instance_region_rectangle[1] + 500, instance_region_rectangle[2], instance_region_rectangle[1] + 700),
                                              (instance_region_rectangle[0], instance_region_rectangle[3] - 300, instance_region_rectangle[2], instance_region_rectangle[3])
                                              ],
                        parent_directory='Bitcoin_Miner',
                        timeout=4,
                        gray_scale_flag=False,
                        settle_delay=0.0025,
                        confidence_list=[0.90,0.90,0.90,0.75,0.90,0.90])

                    #If the shiba icon is found, we tap on that farming area
                    if(file_path == 'top_of_screen_indicator.png'):
                        #Tap on area to collect gifts and satoshis
                        print("Tapping on farming area for gifts and satoshis")
                        nf.tap(xCor, yCor, x_offset=-182 ,y_offset=-82, settle_delay=0,serial=serial, region_rectangle=instance_region_rectangle)

                    #If the obtain_gift icon is found, we tap on it
                    elif(file_path == 'obtain_gift.png'):
                        #Tap on the obtain gift icon
                        print("Tapping on obtain gift icon to collect gift")
                        nf.tap(xCor, yCor, settle_delay=2, y_offset=60, serial=serial, region_rectangle=instance_region_rectangle)
                        
                    #If the magnet power up icon is found, we tap on it
                    elif file_path == 'manager_ability_magnet.png':
                        #Tap on the magnet power up icon
                        print("Tapping on magnet power up icon to collect gifts and satoshis")
                        nf.tap(xCor, yCor, settle_delay=0, serial=serial, region_rectangle=instance_region_rectangle)
                    
                    #If the magnet power up icon is found, we tap on it
                    elif file_path == 'manager_ability_power_up.png':
                        #Tap on the magnet power up icon
                        print("Tapping on bomb power up icon to collect gifts and satoshis")
                        nf.tap(xCor, yCor, settle_delay=0, serial=serial, region_rectangle=instance_region_rectangle)

                    #If the collect button is found, we tap on it
                    elif file_path == 'chest_collect_button.png':
                        #Tap on the collect button
                        print("Tapping on collect button to collect gifts and satoshis")
                        nf.tap(xCor, yCor, settle_delay=0, serial=serial, region_rectangle=instance_region_rectangle)

                    #If the prestige ready icon is found, we set the 
                    elif file_path == 'prestige_icon_ready.png' and not disable_farm:
                        #Set time since last prestige so that a prestige will get triggered next iteration
                        print("Prestige ready icon was found. Prestige must be ready.")
                        webhook.content = f"Prestige ready icon was found. Prestige must be ready. Time: {datetime.datetime.now()}"
                        webhook.execute()

                        if(prestige(serial=serial, instance_region_rectangle=instance_region_rectangle)):
                            return (True)
                        else:
                            continue

                    #If neither is found we will either scroll up or assume we are in an advertisement
                    else:
                        #Attempt to find the coin fragment icon
                        coin_fragment_icon, xCor, yCor = nf.MoveToLocation(file_path='coin_fragment_icon.png',
                                                                           parent_directory='Bitcoin_Miner',
                                                                           timeout=5,
                                                                           region_rectangle=instance_region_rectangle
                                                                           )
                        
                        #If the coin fragment icon is found, we scroll up to the top of the screen
                        if coin_fragment_icon != '':
                            #Scroll all the way up to the top of the screen
                            print("Scrolling up to the top of the screen")
                            for x in range(3):
                                nf.scroll_up(x1 = 540, y1 = 700, x2 = 540, y2 = 1100, settle_delay=0.75, serial=serial)
                            

                        #If we can't find the coin fragment icon, we assume we are in an advertisement
                        else:
                            #Call the clear advertisement function

                            #If we find an advertisement button, we reset the ad_counter to 0
                            if(nf.clear_advertisement_2(timeout=90,serial=serial, region_rectangle=instance_region_rectangle)):
                                ad_counter += 1
                            
                            #If we don't find any advertisement buttons, we increment the ad_counter
                            else:
                                ad_counter = ad_counter_limit

                            continue
                    
                    #Reset the ad counter to 0
                    ad_counter = 0                            

            return(False)

def check_for_screenshots():
    screenshot_files = [
        '2x_income_button.png', 
        'chest_collect_button.png', 
        'coin_fragment_icon.png', 
        'daily_streak_collect_button.png', 
        'daily_streak_ok_button.png', 
        'development_menu_button.png', 
        'development_menu_x_button.png', 
        'development_upgrade_button.png', 
        'gold_server_icon.png', 
        'island_2.png', 
        'island_3.png', 
        'manager_ability_income.png', 
        'manager_ability_magnet.png', 
        'manager_ability_power_up.png', 
        'manager_recruit_x_button.png', 
        'map_button.png', 
        'map_enter_site_button.png', 
        'map_select_x_button.png', 
        'mine_button.png',
        'mine_button_shrink.png',
        'mission_completed.png', 
        'obtain_gift.png', 
        'ok_button.png', 
        'power_surge_button.png', 
        'prestige_icon.png', 
        'prestige_continue_button.png',
        'prestige_icon_ready.png', 
        'prestige_keep_button.png', 
        'prestige_please_wait_indicator.png', 
        'prestige_sell_button.png',  
        'prestige_skip_button.png', 
        'store_x_button.png', 
        'top_of_screen_indicator.png', 
        'unlock_coin_button.png', 
        'unlock_coin_button_grey.png',
        'welcome_back_x_button.png'
    ]

    base_directory = "./Screenshots/Bitcoin_Miner"
    missing_screenshots = [file for file in screenshot_files if not os.path.exists(os.path.join(base_directory, file))]

    for file in missing_screenshots:
        print(f"{file} does not exist in the {base_directory} directory. Please take a screenshot of the missing file before running this script")

    for file in set(screenshot_files) - set(missing_screenshots):
        print(f"{file} exists")

    # If there are no missing screenshots, we return True
    return len(missing_screenshots) == 0





#Initialize global variables
move_to_flag = False
gold_server_not_in_view = True
mine_pickaxe_counter = 0
upgrade_counter = 0
ad_counter = 0
upgrade_counter_limit = 7
ad_counter_limit = 8
mine_pickaxe_counter_limit = 15
current_map = 1
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
TIME_BETWEEN_PRESTIGES = datetime.timedelta(seconds=1800)
disable_farm_flag = False
serial_number = None
instance_region_rectangle = nf.SCRCPY_REGION_RECTANGLE

def main(side=None, serial=None):
    # #Check for the necessary arguments
    global move_to_flag
    global gold_server_not_in_view
    global mine_pickaxe_counter
    global upgrade_counter
    global ad_counter
    global upgrade_counter_limit
    global ad_counter_limit
    global mine_pickaxe_counter_limit
    global current_map
    global webhook
    global TIME_BETWEEN_PRESTIGES
    global disable_farm_flag
    global serial_number
    global instance_region_rectangle


    #Set the region rectangle based on the argument
    if side is not None and serial is not None:
        sys.argv = ["BitcoinMinerUnfinished.py",side, serial]

    if len(sys.argv) >= 2:
        if sys.argv[1] == "left":
            instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_LEFT_REGION_RECTANGLE"))
        elif sys.argv[1] == "right":
            instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_RIGHT_REGION_RECTANGLE"))
        else:
            print("Invalid argument. Please enter either 'left' or 'right' as an argument.")
            exit()
        
    else:
        instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_REGION_RECTANGLE"))


    if len(sys.argv) == 3:
        serial_number = sys.argv[2]
    else:
        serial_number = None

    #We call a reset in order to move the phone to the home screen and then open up the Crypto Mining Tycoon app.
    if (nf.reset_from_unknown_state_return(app_icon="bitcoin_miner_app" , serial=serial_number, region_rectangle=instance_region_rectangle)):
        print("Successfully reset the phone.")
    else:
        print("Unable to find the app icon. Returning false on the Crypto Mining Tycoon main function.")
        return False

    #Check for all the necessary screenshots
    if not check_for_screenshots():
        print("Please add the necessary screenshots before running this script")
        exit()

    

    #Set the time since the last prestige as the current time
    time_since_last_prestige = datetime.datetime.now()

    #Main while loop
    while(True):
       
        #If the upgrade counter has reached the limit, we enter the farming and prestige phase
        if(upgrade_counter >= upgrade_counter_limit):
            print("Upgrade Counter has reached the limit. Attempting to prestige")

            #When the prestige and farming function returns True, we reset the ad_counter and upgrade_counter to 0
            if(prestige_and_farming(time_between_prestiges=TIME_BETWEEN_PRESTIGES,
                                    time_since_last_prestige=time_since_last_prestige,
                                    current_map=current_map,
                                    disable_farm=disable_farm_flag,
                                    serial=serial_number,
                                    instance_region_rectangle=instance_region_rectangle,
                                    ad_counter = ad_counter)):
                
                print("Prestige and farming function returned True. Resetting upgrade counter and mine pickaxe counter to 0")
                time_since_last_prestige = datetime.datetime.now()
                ad_counter = 0
                upgrade_counter = 0

            #If the prestige and farming function returns False, we assume we are in an Advertisement
            else:
                print("Prestige and farming function returned False. Attempting once again")
                

        #Otherwise, we continue with the main loop and print the current upgrade counter for debugging purposes
        else:
            print(f"Current upgrade counter is {upgrade_counter}")


        #If we have been stuck in an advertisement for too long, we assume we are in an unknown state and attempt to reset
        if ad_counter >= ad_counter_limit:
            print("Assuming we have been stuck in an advertisement for too long. Attempting to reset")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            #Send Discord message
            webhook.content = f"Encountered an unknown advertisement. Attempting to reset. Make sure to add advertisement to the list of images. Time: {timestamp}"
            webhook.execute()

            #Take a screenshot of the unknown advertisement
            pyautogui.screenshot(f"./Screenshots/Unknown_Advertisements/{timestamp}-unknown_advertisement.png")

            #Reset from unknown state
            nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle, app_icon="bitcoin_miner_app")

            #Reset the ad_counter to 0
            ad_counter = 0
            mine_pickaxe_counter_limit = 0
            upgrade_counter = 0
            gold_server_not_in_view = True

        #If we have not reached the Upgrade Counter limit or the Ad Counter limit, we continue with the main loop
        print(f"Mine Pickaxe Counter is {mine_pickaxe_counter} out of {mine_pickaxe_counter_limit}")
        print(f"Upgrade Counter is {upgrade_counter} out of {upgrade_counter_limit}")
        print(f"Ad Counter is {ad_counter} out of {ad_counter_limit}")

        #Attempt to find the primary buttons
        print("Searching for primary buttons")
        filePath, xCor, yCor = nf.MoveToLocationListIndividualRegions(file_paths=[
                                    'prestige_icon_ready.png',
                                    'welcome_back_2x_button.png',
                                    'welcome_back_collect_button.png',
                                    'obtain_gift.png',
                                    'daily_manager_button.png',
                                    'coin_upgrade_button.png',
                                    'unlock_coin_button.png',
                                    'map_button.png',
                                    'manager_ability_income.png',
                                    'manager_ability_magnet.png',
                                    'manager_ability_power_up.png',
                                    'mine_button_shrink.png',
                                    'mine_button.png',
                                    'collect_manager_button.png'
                                    ],
                                    parent_directory='Bitcoin_Miner',
                                    region_rectangle_list=[
                                    ((instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[1], instance_region_rectangle[2], 200),
                                    (instance_region_rectangle[0], (instance_region_rectangle[1] + instance_region_rectangle[3]) // 2, (instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], (instance_region_rectangle[1] + instance_region_rectangle[3]) // 2, instance_region_rectangle[2], instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], instance_region_rectangle[1] + 500, instance_region_rectangle[2], instance_region_rectangle[1] + 700),
                                    ((instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, 990, instance_region_rectangle[2], 1100),
                                    (instance_region_rectangle[2] - 110, instance_region_rectangle[1], instance_region_rectangle[2], 935),
                                    (instance_region_rectangle[0], instance_region_rectangle[1] + instance_region_rectangle[3]//3, instance_region_rectangle[2],instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], instance_region_rectangle[1] + instance_region_rectangle[3]//3, instance_region_rectangle[2],instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], instance_region_rectangle[1], (instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], instance_region_rectangle[1], (instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], instance_region_rectangle[1], (instance_region_rectangle[0] + instance_region_rectangle[2]) // 2, instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], instance_region_rectangle[3] - 100, instance_region_rectangle[2], instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], instance_region_rectangle[3] - 100, instance_region_rectangle[2], instance_region_rectangle[3]),
                                    (instance_region_rectangle[0], 1085, instance_region_rectangle[2], 1145),
                                    ],
                                    confidence_list=[
                                        0.85,
                                        0.75,
                                        0.80,
                                        0.80,
                                        0.85,
                                        0.85,
                                        0.85,
                                        0.95,
                                        0.95,
                                        0.95,
                                        0.85,
                                        0.85,
                                        0.85,
                                        0.75
                                    ],
                                    timeout=5,settle_delay=1.0,gray_scale_flag=False)
        
        #If we find a button, then we proceed
        if(filePath != ''):

            #print the name of the file that was found
            print(f"Found {filePath}")

            #If the file path contains x_button, we close the gift window
            if("welcome" in filePath or "daily_streak" in filePath):
                #Close the gift window
                print("Closing popup windows.")
                nf.tap(xCor, yCor,settle_delay=2, serial=serial_number, region_rectangle=instance_region_rectangle)
                continue

            #If the file path is prestige_ready.png, we set the upgrade counter to upgrade counter limit
            if(filePath == "prestige_icon_ready.png"):
                #Set the upgrade counter to the limit
                print("Prestige is ready. Setting upgrade counter to limit")
                upgrade_counter = upgrade_counter_limit
                continue

            if(filePath == "collect_manager_button.png"):
                #Tap on the collect manager button
                print("Tapping on collect manager button")
                nf.tap(xCor, yCor, settle_delay=2, serial=serial_number, region_rectangle=instance_region_rectangle)
                continue
                
            
            #If the gold server is not in view, we need to scroll down until we find it
            if(gold_server_not_in_view):
                print("Gold Server is not in view. Attempting to scroll down.")
                if(not scroll_to_golden_server(serial=serial_number, instance_region_rectangle=instance_region_rectangle)):
                    ad_counter = secondary_image_function(instance_region_rectangle, serial_number, ad_counter)
                    

            #If the file path is either or mine_button.png, we'll either tap on it or attempt to upgrade
            elif(filePath == 'mine_button.png'):
                #If the mine pickaxe counter is less than the limit, we tap on the mine button and increment the counter
                if(mine_pickaxe_counter < mine_pickaxe_counter_limit):
                    for x in range(10):
                        #Tap on the mine button 10 times
                        nf.tap(xCor, yCor, y_offset=random.randint(-120, -60),settle_delay=0.01,serial=serial_number, region_rectangle=instance_region_rectangle)
                    mine_pickaxe_counter += 1
                    print(f"Mine pickaxe count is {mine_pickaxe_counter}")
                
                #If we have reached the mine pickaxe counter limit, we attempt to upgrade production and coins
                else:
                    #Attempt to find the upgrade button
                    print("Mine pickaxe limit reached. Attempt upgrade")
                    upgrade_button, xCor, yCor = nf.MoveToLocation(file_path='development_menu_button.png',
                                                                   parent_directory='Bitcoin_Miner',
                                                                   timeout=5,
                                                                   region_rectangle=instance_region_rectangle)
                    #If the upgrade button is found, we proceed to upgrade
                    if upgrade_button != '':
                        #Tap on the upgrade button
                        print("Found upgrade Button")
                        nf.tap(xCor, yCor, settle_delay=1,serial=serial_number, region_rectangle=instance_region_rectangle)
                        
                        #Attempt to find the quick buy button
                        print("Attempting to upgrade")
                        quick_buy_button, xCor, yCor = nf.MoveToLocation(file_path='development_quick_buy_button.png',
                                                                              parent_directory='Bitcoin_Miner',
                                                                              timeout=5,
                                                                              confidence=0.80,
                                                                              region_rectangle=instance_region_rectangle)
                        
                        #If the quick buy button is found, we tap on it
                        if quick_buy_button != '':
                            #Tap on the quick buy button
                            print("Quick buy button was found. Tapping on it")
                            nf.tap(xCor, yCor,serial=serial_number, region_rectangle=instance_region_rectangle)
                        
                        #Otherwise, we assume that we have insufficient funds to upgrade
                        else:
                            print("Quick buy button was not found. Assuming we have insufficient funds to upgrade")
                            pass

                        
                        
                        #Attempt to close the development menu 
                        development_menu_x_button, xCor, yCor = nf.MoveToLocation(file_path='development_menu_x_button.png',
                                                                            parent_directory='Bitcoin_Miner',
                                                                            timeout=5,
                                                                            region_rectangle=instance_region_rectangle)
                        #If the close button is found, we tap on it
                        if development_menu_x_button != '':
                            #Tap on the development menu close button
                            print("Closing the development menu")
                            nf.tap(xCor, yCor, settle_delay=2, serial=serial_number, region_rectangle=instance_region_rectangle)

                    
                    print("Upgrade complete. Resetting mine pickaxe count")
                    mine_pickaxe_counter = 0
                    upgrade_counter += 1
                    gold_server_not_in_view = True

            #If the file path is map_button.png, we attempt to open the map and move to the next island
            elif(filePath == 'map_button.png'):
                
                #Tap on the map button
                print("Attempting to open the map")
                nf.tap(xCor, yCor, settle_delay=4, serial=serial_number, region_rectangle=instance_region_rectangle)

                #Attempt to find one of the next islands
                island_path, xCor, yCor = nf.MoveToLocation(file_path=f'island_{current_map + 1}.png',
                                                            parent_directory='Bitcoin_Miner',
                                                            region_rectangle=instance_region_rectangle,
                                                            timeout=10)

                #If an island is found, we proceed to select the island and enter the site
                if island_path != '':
                    #Tap on the next island
                    print("Next Island Selected")
                    nf.tap(xCor, yCor,settle_delay=3.0,serial=serial_number, region_rectangle=instance_region_rectangle)
                    
                    #Attempt to find the enter site button
                    print("Attempting to enter the site")
                    enter_site, xCor, yCor = nf.MoveToLocation(file_path='map_enter_site_button.png',
                                                               parent_directory='Bitcoin_Miner',
                                                               timeout=10,
                                                               region_rectangle=instance_region_rectangle,
                                                               confidence=0.75)
                    #If the enter site button is found, we proceed to enter the site and reset the mine pickaxe counter
                    if enter_site != '':
                        #Tap on the enter site button
                        nf.tap(xCor, yCor, settle_delay=5,serial=serial_number,region_rectangle=instance_region_rectangle)
                        print("Site entered. Resetting mine pickaxe count")
                        mine_pickaxe_counter = 0
                        current_map += 1

            #If the file path is unlock_button.png, we attempt to unlock the next coin
            elif(filePath == "unlock_coin_button.png"):
                #Tap on the unlock button
                print("Next coin has been unlocked. Scrolling down until Gold Server is visible")
                nf.tap(xCor, yCor,settle_delay=0.5,serial=serial_number, region_rectangle=instance_region_rectangle)
                
                #Scroll down to find the gold server
                scroll_to_golden_server(serial=serial_number, instance_region_rectangle=instance_region_rectangle)

                #Reset the mine pickaxe and upgrade counter
                mine_pickaxe_counter = 0
                upgrade_counter = 0


            #If the file path is reset_indicator .png, we double check it with a higher confidence. If we find it again, then we reset
            elif(filePath == "reset_indicator.png"):
                #Pause execution for 3 seconds
                time.sleep(3)
            
                #Attempt to find the reset indicator again
                reset_indicator, xCor, yCor = nf.MoveToLocation(file_path='reset_indicator.png',
                                                                parent_directory='Bitcoin_Miner',
                                                                timeout=5,
                                                                region_rectangle=instance_region_rectangle,
                                                                confidence=0.95)
                
                #If the reset indicator is found, we reset the game
                if reset_indicator != '':
                    print("Reset indicator found. Resetting the game")
                    #Reset from unknown state
                    nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle)

            #IF the file path is daily_manager_button.png, we tap on the daily manager button
            elif(filePath == "daily_manager_button.png"):
                #Tap on the daily manager button
                print("Tapping on daily manager button")
                nf.tap(xCor, yCor, settle_delay=2, serial=serial_number, region_rectangle=instance_region_rectangle)

                search_manager_button, xCor, yCor = nf.MoveToLocation(file_path='daily_search_manager_button.png',
                                                                   parent_directory='Bitcoin_Miner',
                                                                   timeout=5,
                                                                   region_rectangle=instance_region_rectangle)
                #If the upgrade button is found, we proceed to upgrade
                if search_manager_button != '':
                    #Tap on the upgrade button
                    print("Tapping on search_manager_button button")
                    nf.tap(xCor, yCor, settle_delay=1,serial=serial_number, region_rectangle=instance_region_rectangle)

            

            #If any other button is found, we simply tap on it
            else:
                #Tap on found primary button
                print(f"Tapping on {filePath}")
                nf.tap(xCor, yCor, serial=serial_number, region_rectangle=instance_region_rectangle, settle_delay=1.5)

            #If any primary button is found, we reset the ad_counter to 0
            ad_counter = 0

        #If we don't find any primary buttons, we attempt to locate seconday images
        else:    
            #Attempt to find the secondary buttons
            ad_counter = secondary_image_function(instance_region_rectangle, serial_number, ad_counter)


if __name__ == "__main__":
    main()