import random
import pyautogui
import time
from discord_webhook import DiscordWebhook
import datetime
import os
import NavigationFunctions as nf



# Function to prestige the game once we get the opportunity
def prestige():
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
                                                    timeout=5)

    #If the prestige button is found, we proceed to click on it
    if prestige_button != '':
        #Tap on the prestige button
        print("Prestige button found. Tapping on it")
        nf.tap(xCor, yCor)
        
        #Attempt to find the please_wait indicator
        please_wait, xCor, yCor = nf.MoveToLocation(file_path='prestige_please_wait_indicator.png',
                                                    parent_directory='Bitcoin_Miner',
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
                                                        timeout=5)

            #If the sell button is found, we proceed to click on it
            if sell_button != '':
                #Tap on the sell button
                print("Sell button found. Tapping on it")
                nf.tap(xCor, yCor,settle_delay=1)

                #Attempt to find the keep button
                keep_button, xCor, yCor = nf.MoveToLocation(file_path='prestige_keep_button.png',
                                                            parent_directory='Bitcoin_Miner',
                                                            timeout=5)

                #If the keep button is found, we proceed to click on it
                if keep_button != '':
                    #Tap on the keep button
                    print("Keep button found. Tapping on it")
                    nf.tap(xCor, yCor,settle_delay=1)

                    #Allow the prestige to commence and reset the upgrade_counter and mine_pickaxe_counter to 0
                    print("Prestige has commenced")
                    print("Waiting for 30 seconds for the prestige to complete")
                    time.sleep(30)
                    upgrade_counter = 0
                    mine_pickaxe_counter = 0
                    ad_counter = 0
                    current_map = 1
                    return(True)
    
    else:
        nf.clear_advertisement()

    #If we get to this point, then the prestige has failed and we attempt to return to the main while loop
    current_time = datetime.datetime.now()
    print(f"Prestige has failed. Assuming we are in a screen that is not allowing us to prestige. Time: {current_time}")
    webhook.content = f"Prestige has failed. Assuming we are in a screen that is not allowing us to prestige. Time: {current_time}"
    webhook.execute()
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
    gold_server_icon, xCor, yCor = nf.MoveToLocation(file_path='gold_server_icon.png',
                                                     parent_directory='Bitcoin_Miner',
                                                     timeout=2)
    
    #If the gold server is not found, continue scrolling down until it is found or the counter reaches 8
    while(gold_server_icon == "" and gold_server_scroll_counter < 8):

        #Attempt to find the coin fragment icon
        coin_fragment_icon, xCor, yCor = nf.MoveToLocation(file_path='coin_fragment_icon.png',
                                                           parent_directory='Bitcoin_Miner',
                                                           timeout=5,
                                                           region_rectangle=(((nf.SCRCPY_REGION_RECTANGLE[0] + nf.SCRCPY_REGION_RECTANGLE[2])//2),
                                                                             nf.SCRCPY_REGION_RECTANGLE[1],
                                                                             nf.SCRCPY_REGION_RECTANGLE[2],
                                                                             ((nf.SCRCPY_REGION_RECTANGLE[1] + nf.SCRCPY_REGION_RECTANGLE[3])//2))
                                                           )
        
        #If the coin fragment icon is not found, we break the loop and assume we are in an advertisement
        if coin_fragment_icon == '':
            print("Coin Fragment icon is not found. Assuming we are in an advertisement")
            gold_server_not_in_view = True
            return None
        
        else:
            print("Found Coin Fragment icon. Scrolling down")

        #Scroll down slightly
        nf.scroll_down(x1 = 540, y1 = 1000, x2 = 540, y2 = 950, settle_delay=0.5)
        
        #Attempt to find the location of the gold server
        print("Attempting to find the location of the gold server")
        gold_server_icon, xCor, yCor = nf.MoveToLocation(file_path='gold_server_icon.png',
                                                         parent_directory='Bitcoin_Miner',
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
            return None

    #If we can't find the gold server after 8 scrolls, we assume we are in an advertisement
    if gold_server_scroll_counter == 8:
        print("Gold Server has not been found after 8 scrolls. We are most likely viewing an advertisement.")
        gold_server_not_in_view = True
    
    #Otherwise, we assume the gold server is in view and we don't need to scroll
    else:
        print("Gold Server is in view. No need to scroll")
        gold_server_not_in_view = False


def prestige_and_farming(time_between_prestiges, time_since_last_prestige,current_map,disable_farm):

        current_time = datetime.datetime.now()

        #If 30 minutes have passed since the last prestige or the prestige ready icon was found, we attempt to prestige
        if current_time - time_since_last_prestige >= time_between_prestiges and not disable_farm:
            print("30 MINUTES or Prestige Ready Icon was found. Attempting to perform a prestige")
            if(prestige()):
                return (True)

        #If 30 minutes have not passed since the last prestige, we'll attempt to farm gifts and satoshis
        else:
            print("30 minutes have not passed since the last prestige. We will attempt to farm gifts and satoshis.")
            
            end_time = time_since_last_prestige + time_between_prestiges
            while(datetime.datetime.now() < end_time or disable_farm):

                    #Attempt to find the following images
                    file_path, xCor, yCor = nf.MoveToLocationListIndividualRegions(
                        file_paths=['prestige_icon_ready.png',
                                    'manager_ability_magnet.png', 
                                    'manager_ability_power_up.png',
                                    'top_of_screen_indicator.png',
                                    'obtain_gift.png',
                                    'chest_collect_button.png'
                                    ],
                        parent_directory='Bitcoin_Miner',
                        timeout=4,
                        # region_rectangle_list=[((nf.SCRCPY_REGION_RECTANGLE[0] + nf.SCRCPY_REGION_RECTANGLE[2])//2, nf.SCRCPY_REGION_RECTANGLE[1], nf.SCRCPY_REGION_RECTANGLE[2], (nf.SCRCPY_REGION_RECTANGLE[1] + nf.SCRCPY_REGION_RECTANGLE[3])//4),
                        #                        (nf.SCRCPY_REGION_RECTANGLE[0], (nf.SCRCPY_REGION_RECTANGLE[1] + nf.SCRCPY_REGION_RECTANGLE[3])//4, nf.SCRCPY_REGION_RECTANGLE[2]//2, nf.SCRCPY_REGION_RECTANGLE[3]//4),
                        #                        (905, 648, 125, 22),
                        #                        (1147,569,61,34),
                        #                        (851,954,216,87),
                        #                        (1133,187,70,65)],
                        gray_scale_flag=False,
                        settle_delay=0.0025,
                        confidence=0.90)

                    #If the shiba icon is found, we tap on that farming area
                    if(file_path == 'top_of_screen_indicator.png'):
                        #Tap on area to collect gifts and satoshis
                        print("Tapping on farming area for gifts and satoshis")
                        nf.tap(xCor, yCor, y_offset=-40, settle_delay=0)
                        #nf.tap(xCor, yCor, x_offset=-242, y_offset=-156, settle_delay=0)

                    #If the obtain_gift icon is found, we tap on it
                    elif(file_path == 'obtain_gift.png'):
                        #Tap on the obtain gift icon
                        print("Tapping on obtain gift icon to collect gift")
                        nf.tap(xCor, yCor, settle_delay=2, y_offset=60)
                        
                    #If the magnet power up icon is found, we tap on it
                    elif file_path == 'manager_ability_magnet.png':
                        #Tap on the magnet power up icon
                        print("Tapping on magnet power up icon to collect gifts and satoshis")
                        nf.tap(xCor, yCor, settle_delay=0)
                    
                    #If the magnet power up icon is found, we tap on it
                    elif file_path == 'manager_ability_power_up.png':
                        #Tap on the magnet power up icon
                        print("Tapping on bomb power up icon to collect gifts and satoshis")
                        nf.tap(xCor, yCor, settle_delay=0)

                    #If the collect button is found, we tap on it
                    elif file_path == 'chest_collect_button.png':
                        #Tap on the collect button
                        print("Tapping on collect button to collect gifts and satoshis")
                        nf.tap(xCor, yCor, settle_delay=0)

                    #If the prestige ready icon is found, we set the 
                    elif file_path == 'prestige_icon_ready.png' and not disable_farm:
                        #Set time since last prestige so that a prestige will get triggered next iteration
                        print("Prestige ready icon was found. Prestige must be ready.")
                        webhook.content = f"Prestige ready icon was found. Prestige must be ready. Time: {datetime.datetime.now()}"
                        webhook.execute()

                        if(prestige()):
                            return (True)
                        else:
                            continue

                    #If neither is found we will either scroll up or assume we are in an advertisement
                    else:
                        #Attempt to find the coin fragment icon
                        coin_fragment_icon, xCor, yCor = nf.MoveToLocation(file_path='coin_fragment_icon.png',
                                                                           parent_directory='Bitcoin_Miner',
                                                                           timeout=5,
                                                                           )
                        
                        #If the coin fragment icon is found, we scroll up to the top of the screen
                        if coin_fragment_icon != '':
                            #Scroll all the way up to the top of the screen
                            print("Scrolling up to the top of the screen")
                            for x in range(3):
                                nf.scroll_up(x1 = 540, y1 = 700, x2 = 540, y2 = 1100, settle_delay=0.75)
                            

                        #If we can't find the coin fragment icon, we assume we are in an advertisement
                        else:
                            #Call the clear advertisement function

                            #If we find an advertisement button, we reset the ad_counter to 0
                            if(nf.clear_advertisement()):
                                ad_counter = 0
                            
                            #If we don't find any advertisement buttons, we increment the ad_counter
                            else:
                                ad_counter += 1
                        
                            continue
                    
                    #Reset the ad counter to 0
                    ad_counter = 0                            

            return(False)

def check_for_screenshots():
    screenshot_files = [
        '2x_income_button.png', 
        'chest_collect_button.png', 
        'coin_fragment_icon.png', 
        'continue_prestige_button.png', 
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

if __name__ == "__main__":

    #Check for all the necessary screenshots
    if not check_for_screenshots():
        print("Please add the necessary screenshots before running this script")
        exit()

    #Initialize global variables
    move_to_flag = False
    gold_server_not_in_view = True
    mine_pickaxe_counter = 0
    upgrade_counter = 0
    ad_counter = 0
    upgrade_counter_limit = 15
    ad_counter_limit = 3
    mine_pickaxe_counter_limit = 5
    current_map = 1
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    TIME_BETWEEN_PRESTIGES = datetime.timedelta(seconds=1800)
    disable_farm_flag = False

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
                                    disable_farm=disable_farm_flag)):
                
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
            nf.reset_from_unknown_state()

            #Reset the ad_counter to 0
            ad_counter = 0

        #If we have not reached the Upgrade Counter limit or the Ad Counter limit, we continue with the main loop
        print(f"Upgrade Counter is {upgrade_counter} out of {upgrade_counter_limit}")
        print(f"Ad Counter is {ad_counter} out of {ad_counter_limit}")

        #Attempt to find the primary buttons
        print("Searching for primary buttons")
        filePath, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'store_x_button.png',
                                    'manager_recruit_x_button.png',
                                    'development_menu_x_button.png',
                                    'map_select_x_button.png',
                                    'welcome_back_x_button.png',
                                    'prestige_icon_ready.png',
                                    'chest_collect_button.png',
                                    'unlock_coin_button.png',
                                    'map_button.png',
                                    'manager_ability_income.png',
                                    'manager_ability_magnet.png',
                                    'manager_ability_power_up.png',
                                    #'power_surge_button.png',
                                    #'2x_income_button.png',
                                    'daily_streak_collect_button.png',
                                    'daily_streak_ok_button.png',
                                    'mine_button_shrink.png',
                                    'mine_button.png',
                                    ],
                                    parent_directory='Bitcoin_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.90)
        
        #If we find a button, then we proceed
        if(filePath != ''):

            #print the name of the file that was found
            print(f"Found {filePath}")

            #If the file path contains x_button, we close the gift window
            if("x_button" in filePath):
                #Close the gift window
                print("Closing gift window")
                nf.tap(xCor, yCor,settle_delay=2)
                continue
            
            #If the gold server is not in view, we need to scroll down until we find it
            if(gold_server_not_in_view):
                print("Gold Server is not in view. Attempting to scroll down.")
                scroll_to_golden_server()

            #If the file path is either or mine_button.png, we'll either tap on it or attempt to upgrade
            elif(filePath == 'mine_button.png'):
                #If the mine pickaxe counter is less than the limit, we tap on the mine button and increment the counter
                if(mine_pickaxe_counter < mine_pickaxe_counter_limit):
                    for x in range(10):
                        #Tap on the mine button 10 times
                        nf.tap(xCor, yCor, y_offset=random.randint(-120, -60),settle_delay=0.01)
                    mine_pickaxe_counter += 1
                    print(f"Mine pickaxe count is {mine_pickaxe_counter}")
                
                #If we have reached the mine pickaxe counter limit, we attempt to upgrade production and coins
                else:
                    #Attempt to find the upgrade button
                    print("Mine pickaxe limit reached. Attempt upgrade")
                    upgrade_button, xCor, yCor = nf.MoveToLocation(file_path='development_menu_button.png',
                                                                   parent_directory='Bitcoin_Miner',
                                                                   timeout=5)
                    #If the upgrade button is found, we proceed to upgrade
                    if upgrade_button != '':
                        #Tap on the upgrade button
                        print("Found upgrade Button")
                        nf.tap(xCor, yCor, settle_delay=1)
                        
                        #Attempt to find the quick buy button
                        print("Attempting to upgrade")
                        quick_buy_button, xCor, yCor = nf.MoveToLocation(file_path='development_quick_buy_button.png',
                                                                              parent_directory='Bitcoin_Miner',
                                                                              timeout=5,
                                                                              confidence=0.80)
                        
                        #If the quick buy button is found, we tap on it
                        if quick_buy_button != '':
                            #Tap on the quick buy button
                            print("Quick buy button was found. Tapping on it")
                            nf.tap(xCor, yCor)
                        
                        #Otherwise, we assume that we have insufficient funds to upgrade
                        else:
                            print("Quick buy button was not found. Assuming we have insufficient funds to upgrade")
                            pass

                        
                        
                        #Attempt to close the development menu 
                        development_menu_x_button, xCor, yCor = nf.MoveToLocation(file_path='development_menu_x_button.png',
                                                                            parent_directory='Bitcoin_Miner',
                                                                            timeout=5)
                        #If the close button is found, we tap on it
                        if development_menu_x_button != '':
                            #Tap on the development menu close button
                            print("Closing the development menu")
                            nf.tap(xCor, yCor, settle_delay=2)

                    #Upgrade your coins if you have leftover funds three times
                    for x in range(3):

                        #Attempt to find the coin_upgrade_button
                        print("Attempting to upgrade a coin with leftover funds.")
                        coin_upgrade, xCor, yCor = nf.MoveToLocation(file_path='coin_upgrade_button.png',
                                                                                parent_directory='Bitcoin_Miner',
                                                                                timeout=5,
                                                                                confidence=0.80)
                    
                        #If the coin upgrade button is found, we tap on it
                        if coin_upgrade != '':
                            print("Coin upgrade button was found. Tapping on it")
                            nf.hold(xCor, yCor, settle_delay=1)

                        #If we can't find the coin upgrade button, we assume we have insufficient funds and break out of the loop
                        else:
                            print("Coin upgrade button was not found. Assuming we have insufficient funds to upgrade")
                            break

                    #Regardless if we have upgraded production or the most recent coin, we reset the mine pickaxe counter
                    #and in increment the upgrade counter
                    print("Upgrade complete. Resetting mine pickaxe count")
                    mine_pickaxe_counter = 0
                    upgrade_counter += 1

            #If the file path is map_button.png, we attempt to open the map and move to the next island
            elif(filePath == 'map_button.png'):
                
                #Tap on the map button
                print("Attempting to open the map")
                nf.tap(xCor, yCor, settle_delay=4)

                #Attempt to find one of the next islands
                island_path, xCor, yCor = nf.MoveToLocation(file_path=f'island_{current_map + 1}.png',
                                                            parent_directory='Bitcoin_Miner',
                                                            timeout=10)

                #If an island is found, we proceed to select the island and enter the site
                if island_path != '':
                    #Tap on the next island
                    print("Next Island Selected")
                    nf.tap(xCor, yCor,settle_delay=3.0)
                    
                    #Attempt to find the enter site button
                    print("Attempting to enter the site")
                    enter_site, xCor, yCor = nf.MoveToLocation(file_path='map_enter_site_button.png',
                                                               parent_directory='Bitcoin_Miner',
                                                               timeout=10,
                                                               confidence=0.75)
                    #If the enter site button is found, we proceed to enter the site and reset the mine pickaxe counter
                    if enter_site != '':
                        #Tap on the enter site button
                        nf.tap(xCor, yCor, settle_delay=5)
                        print("Site entered. Resetting mine pickaxe count")
                        mine_pickaxe_counter = 0
                        current_map += 1

            #If the file path is unlock_button.png, we attempt to unlock the next coin
            elif(filePath == "unlock_coin_button.png"):
                #Tap on the unlock button
                print("Next coin has been unlocked. Scrolling down until Gold Server is visible")
                nf.tap(xCor, yCor,settle_delay=0.5)
                
                #Scroll down to find the gold server
                scroll_to_golden_server()

                #Reset the mine pickaxe and upgrade counter
                mine_pickaxe_counter = 0
                upgrade_counter = 0
            
            #If the file path is prestige_ready.png, we set the upgrade counter to upgrade counter limit
            elif(filePath == "prestige_icon_ready.png"):
                #Set the upgrade counter to the limit
                print("Prestige is ready. Setting upgrade counter to limit")
                upgrade_counter = upgrade_counter_limit

            #If the file path is 2x_income.png, we click on it. WE DO NOT TAP, tapping does not work for some reason
            elif(filePath == "2x_income_button.png"):
                #Click on the 2x income button
                print("2x Income button found. Clicking on it")
                pyautogui.doubleClick(xCor, yCor)
                time.sleep(0.5)

            #If any other button is found, we simply tap on it
            else:
                #Tap on found primary button
                print(f"Tapping on {filePath}")
                nf.tap(xCor, yCor)

            #If any primary button is found, we reset the ad_counter to 0
            ad_counter = 0

        #If we don't find any primary buttons, we assume we're in an advertisement and proceed to clear it    
        else:    
            #Call the clear advertisement function
            #If we find an advertisement button, we reset the ad_counter to 0
            if(nf.clear_advertisement()):
                ad_counter = 0
            
            #If we don't find any advertisement buttons, we increment the ad_counter
            else:
                ad_counter += 1





            