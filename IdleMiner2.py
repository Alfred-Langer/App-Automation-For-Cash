import datetime
import NavigationFunctions as nf

def open_up_gear():
    
    #Open up any gear packs that are available
    gear_pack, x_cor, y_cor = nf.MoveToLocationList(file_paths=['gear_pack_one.png','gear_pack_two.png'],
                                                    parent_directory='Idle_Miner',
                                                    timeout=5,
                                                    confidence=0.85)
    
    if gear_pack != "":
        print("A gear pack was found. Tapping on the gear pack to open them.")
        nf.tap(x_cor, y_cor)


        reset_tap_flag = False
        while True:
            
            gear_primary, gear_primary_x_cor, gear_primary_y_cor = nf.MoveToLocationList(file_paths=['gear_icon.png','continue_button.png','trophy_icon.png'],
                                                    parent_directory='Idle_Miner',
                                                    timeout=15,
                                                    confidence=0.85)
            if gear_primary == "gear_icon.png" or gear_primary == 'continue_button.png':
                #print("We are still in the gear pack. Tapping on the gear icon to reveal the gear.")
                nf.tap(gear_primary_x_cor, gear_primary_y_cor,settle_delay=5)

                reset_tap_flag = False
            
            elif gear_primary == "trophy_icon.png":
                print("We have reached the end of the gear pack and have returned to the main gameplay screen.")
                break

            else:
                if not reset_tap_flag:
                    print("Unable to find the gear icon or continue button. Tapping on the center of the screen.")
                    nf.tap(nf.PHONE_SCREEN_RESOLUTION[0] / 2, nf.PHONE_SCREEN_RESOLUTION[1] / 2,non_scale=True)
                    reset_tap_flag = True
                else:
                    print("Unable to find the gear icon or continue button or trophy icon for a second time in a row. Exiting the script.")
                    exit()
            

    else:
        print("Unable to find a Gear Pack. Proceeding as normal.")

def identify_mine():
    #Identify which mine we are currently in

    #Search for the Mine Check Button
    mine_check_button, x_cor, y_cor = nf.MoveToLocation(file_path='Mine_Check_Button.png',
                                                                   parent_directory='Idle_Miner',
                                                                   timeout=5)
    
    #If we can't find the Mine Check Button then kill the script
    if mine_check_button == '':
        print("Unable to find the Mine Check Button. Exiting script.")
        exit()

    #Tap the Mine Check Button
    nf.tap(x_cor, y_cor, settle_delay=3)

    #Search for a Mine Indicator
    mine_indicator, mine_indicator_x_cor, mine_indicator_y_cor = nf.MoveToLocationList(file_paths=[
                                    'Starter_Mine-Indicator.png',
                                    'Village_Mine-Indicator.png',
                                    'Deep_Deep_Caves-Indicator.png',
                                    'River_Crossing-Indicator.png',
                                    'Coal_Mines-Indicator.png',
                                    'Gilded_Grasslands-Indicator.png',
                                    'Obsidian_Drains-Indicator.png',
                                    'Trapped_Mine-Indicator.png',
                                    'Muddy_Plains-Indicator.png',
                                    'Redstone_Ravine-Indicator.png'
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.90)
    

    #If we can't find the Mine Indicator then kill the script
    if mine_indicator == '':
        print("Unable to find a Mine Indicator. Exiting script.")
        exit()

    #Update the Mine Name
    mine_name = mine_indicator.split('-')[0]
    print("Mine Name: ", mine_name)

    #Tap the Mine Check Button to close the Mine Check Menu
    nf.tap(x_cor, y_cor)

    #Return the Mine Name
    return mine_name

def reset_tap():
    nf.tap(950, 50)

def starter_mine_routine():

    last_speed_upgrade = datetime.datetime.now()

    open_up_gear()

    while True:
        search_for_gift()
        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'topaz_ore_sign.png'                                
                                    ],
                                    parent_directory='Idle_Miner\\Starter_Mine',
                                    timeout=5,settle_delay=0.01,confidence=0.90)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Topaz Ore Sign
        elif primary_button == "topaz_ore_sign.png":
            #Tap the Topaz Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Starter_Mine',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":
                #Hold the Upgrade Button for 3 seconds
                nf.hold(upgrade_x_cor, upgrade_y_cor, duration=3000, settle_delay= 2)

            #Click on the crates to unlock the ore crystals
            for x_offset in range(60,121,60):
                nf.tap(xCor + x_offset, yCor)

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Starter_Mine',
                                                                        timeout=5,
                                                                        confidence=0.90)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

def progressing_to_next_mine():

    #Attempt to locate the done button
    done_button, xCor, yCor = nf.MoveToLocation(file_path='done_button.png',
                        parent_directory='Idle_Miner',
                        timeout=25,
                        confidence=0.90)
    
    #If we find the Done Button then we tap it
    if done_button != "":
        nf.tap(xCor, yCor)

    #If we can't find the Done Button we assume we didn't level up and we attempt to locate the Next Level Button
    next_level_button, xCor, yCor = nf.MoveToLocation(file_path='next_level_button.png',
                        parent_directory='Idle_Miner',
                        timeout=25,
                        confidence=0.90)
    
    #If we find the Next Level Button then we tap it
    if next_level_button != "":
        nf.tap(xCor, yCor, settle_delay=10)

        reset_tap()

    else:
        print("Unable to locate the Done or Next Level Button. Resetting the app.")
        exit()

def village_mine_routine():

    last_speed_upgrade = datetime.datetime.now()

    open_up_gear()

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'emerald_ore_sign.png',
                                    'ruby_ore_sign.png',
                                    'generic_ore_sign.png'
                                    ],
                                    parent_directory='Idle_Miner\\Village_Mine',
                                    timeout=5,settle_delay=0.01,confidence=0.90)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:
            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Village_Mine',
                                                                        timeout=5,
                                                                        confidence=0.80)

            if upgrade_ore_button != "":

                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.1)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Village_Mine',
                                                                        timeout=2,
                                                                        confidence=0.80,
                                                                        settle_delay=0.05)

            #Click on the crates to unlock the ore crystals
            for y_offset in range(10,250,10):
                nf.tap(xCor, yCor + y_offset)

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Village_Mine',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

            #Perform a Reset Tap to reset menus
            reset_tap()

def deep_deep_caves_routine():

    last_speed_upgrade = datetime.datetime.now()

    open_up_gear()

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'obsidian_ore_sign.png',
                                    'silver_ore_sign.png',
                                    'copper_ore_sign.png',
                                    'generic_ore_sign.png'
                                    ],
                                    parent_directory='Idle_Miner\\Deep_Deep_Caves',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Deep_Deep_Caves',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":

                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.1)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Deep_Deep_Caves',
                                                                        timeout=2,
                                                                        confidence=0.85,
                                                                        settle_delay=0.05)

            if primary_button == "copper_ore_sign.png":
                #Click on the crates to unlock the ore crystals
                for x_offset in range(50,200,50):
                    nf.tap(xCor + x_offset, yCor)
            else:
                #Click on the crates to unlock the ore crystals
                for y_offset in range(50,200,50):
                    nf.tap(xCor, yCor + y_offset)

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Deep_Deep_Caves',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

def river_crossing_routine():

    last_speed_upgrade = datetime.datetime.now()

    open_up_gear()

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    #'gift_icon.png',
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'gold_ore_sign.png',
                                    'emerald_ore_sign.png',
                                    'onyx_ore_sign.png',
                                    'topaz_ore_sign.png',
                                    'generic_ore_sign.png'
                                    ],
                                    parent_directory='Idle_Miner\\River_Crossing',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\River_Crossing',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":

                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.1)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\River_Crossing',
                                                                        timeout=2,
                                                                        confidence=0.85,
                                                                        settle_delay=0.05)


            #Click on the crates to unlock the ore crystals
            for y_offset in range(40,161,40):
                nf.tap(xCor, yCor + y_offset)

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\River_Crossing',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

        else:
            secondary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'costumes_x_button.png',
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.85)
            
            if secondary_button:
                nf.tap(xCor, yCor)

def coal_mines_routine():

    last_speed_upgrade = datetime.datetime.now()

    open_up_gear()

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'firestone_ore_sign.png',
                                    'copper_ore_sign.png',
                                    'silver_ore_sign.png',
                                    'gold_ore_sign.png',
                                    'ruby_ore_sign.png',
                                    'generic_ore_sign.png'
                                    ],
                                    parent_directory='Idle_Miner\\Coal_Mines',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Coal_Mines',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":

                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.1)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Coal_Mines',
                                                                        timeout=2,
                                                                        confidence=0.85,
                                                                        settle_delay=0.05)

            if "gold" in primary_button:
                #Click on the crates to unlock the ore crystals
                for x_offset in range(50,200,50):
                    nf.tap(xCor + x_offset, yCor)
            else:        
                #Click on the crates to unlock the ore crystals
                for y_offset in range(40,161,40):
                    nf.tap(xCor, yCor + y_offset)

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Coal_Mines',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

        else:
            secondary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'costumes_x_button.png',
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.85)
            
            if secondary_button:
                nf.tap(xCor, yCor)

def gilded_grasslands_routine():

    last_speed_upgrade = datetime.datetime.now()

    agate_ore_maxed = False

    open_up_gear()

    while True:

        search_for_gift()

        if agate_ore_maxed:
            primary_button_list =[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'topaz_ore_sign.png',
                                    'emerald_ore_sign.png',
                                    'onyx_ore_sign.png',
                                    'gold_ore_sign.png',
                                    'firestone_ore_sign.png',
                                    'generic_ore_sign.png'
                                ]

        else:
            primary_button_list =[
                                    'upgrade_available_button.png',
                                    'agate_ore_sign.png',
                                ]

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=primary_button_list,
                                    parent_directory='Idle_Miner\\Gilded_Grasslands',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocationList(file_paths=[
                                                                        'claim_button.png',
                                                                        'upgrade_ore_button.png'
                                                                        ],
                                                                        parent_directory='Idle_Miner\\Gilded_Grasslands',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_ore_button == "claim_button.png":
                print("Accidentally clicked on a gift. Resetting the routine.")
                nf.tap(upgrade_x_cor, upgrade_y_cor)
                continue

            elif upgrade_ore_button != "":

                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.1)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocationList(file_paths=[
                                                                        'claim_button.png',
                                                                        'upgrade_ore_button.png'
                                                                        ],
                                                                        parent_directory='Idle_Miner\\Gilded_Grasslands',
                                                                        timeout=2,
                                                                        confidence=0.85,
                                                                        settle_delay=0.05)
                    
                if primary_button == "claim_button.png":
                    print("Accidentally clicked on a gift. Resetting the routine.")
                    nf.tap(upgrade_x_cor, upgrade_y_cor)
                    continue  

                elif "gold" in primary_button or "topaz" in primary_button:
                    #Click on the crates to unlock the ore crystals
                    for x_offset in range(50,200,50):
                        nf.tap(xCor + x_offset, yCor)

                elif "emerald" in primary_button:
                    #Click on the crates to unlock the ore crystals
                    nf.tap(xCor + 50 , yCor)
                    nf.tap(xCor + 50 , yCor + 50)
                    nf.tap(xCor, yCor + 50)

                elif "firestone" in primary_button:
                    #Click on the crates to unlock the ore crystals
                    nf.tap(xCor - 50 , yCor)
                    nf.tap(xCor - 50 , yCor + 50)
                    nf.tap(xCor, yCor + 50)

                elif "onyx" in primary_button or "agate" in primary_button:        
                    #Click on the crates to unlock the ore crystals
                    for y_offset in range(40,121,40):
                        nf.tap(xCor, yCor + y_offset)

            else:
                print("Found the Ore Sign but couldn't locate the Upgrade Button. Tapping around the Ore Sign to unlock crates")
                nf.tap(xCor + 50, yCor)
                nf.tap(xCor - 50, yCor)
                nf.tap(xCor, yCor + 50)
                nf.tap(xCor, yCor - 50)
                nf.tap(xCor + 50, yCor + 50)
                nf.tap(xCor - 50, yCor - 50)
                

            if "agate" in primary_button:
                agate_ore_maxed_indicator, agate_ore_maxed_x_cor, agate_ore_maxed_y_cor = nf.MoveToLocation(file_path='agate_ore_maxed_indicator.png',
                                                                    parent_directory='Idle_Miner\\Gilded_Grasslands',
                                                                    timeout=15,
                                                                    confidence=0.80)
                if agate_ore_maxed_indicator != "":
                    print("Agate has been maxed, scrolling down the map.")
                    agate_ore_maxed = True

                    #Scrolling down the map since agate is now maxed
                    for x in range(10):
                        nf.scroll_down(settle_delay=0.1)

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Gilded_Grasslands',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

        else:
            secondary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'costumes_x_button.png',
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.85)
            
            if secondary_button:
                nf.tap(xCor, yCor)

def obsidian_drains_routine():

    last_speed_upgrade = datetime.datetime.now()

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    #'gift_icon.png',
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'sapphire_ore_sign.png',
                                    'ruby_ore_sign.png',
                                    'silver_ore_sign.png',
                                    'copper_ore_sign.png',
                                    'gold_ore_sign.png',
                                    'agate_ore_sign.png',
                                    'generic_ore_sign.png'
                                    ],
                                    parent_directory='Idle_Miner\\Obsidian_Drains',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Obsidian_Drains',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":

                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.1)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Obsidian_Drains',
                                                                        timeout=2,
                                                                        confidence=0.85,
                                                                        settle_delay=0.05)

            for y_offset in range(40,161,40):
                nf.tap(xCor, yCor + y_offset)

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Obsidian_Drains',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

        else:
            secondary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'costumes_x_button.png',
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.85)
            
            if secondary_button:
                nf.tap(xCor, yCor)

def trapped_mine_routine():

    last_speed_upgrade = datetime.datetime.now()

    #Scroll up to the very top
    for x in range(20):
        nf.scroll_up(settle_delay=0.1)


    for x in range(100):
        nf.scroll_down(settle_delay=0.1)
        scroll_down_indicator, scroll_down_x_cor, scroll_down_y_cor = nf.MoveToLocation(file_path='scroll_down_indicator.png',
                                                                        parent_directory='Idle_Miner\\Trapped_Mine',
                                                                        timeout=3,
                                                                        confidence=0.80,
                                                                        region_rectangle=(nf.SCRCPY_REGION_RECTANGLE[0],
                                                                                          nf.SCRCPY_REGION_RECTANGLE[1],
                                                                                          nf.SCRCPY_REGION_RECTANGLE[2],
                                                                                          int(nf.SCRCPY_REGION_RECTANGLE[3] / 2.65))
        )
        
        if scroll_down_indicator != "":
            print("We have reached the ideal to begin the routine")
            break

    
    open_up_gear()

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'mushrock_ore_sign.png',
                                    'agate_ore_sign.png',
                                    'gold_ore_sign.png',
                                    'topaz_ore_sign.png',
                                    'ruby_ore_sign.png',
                                    'firestone_ore_sign.png',
                                    'sapphire_ore_sign.png',
                                    'generic_ore_sign.png'
                                ],
                                    parent_directory='Idle_Miner\\Trapped_Mine',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Trapped_Mine',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":
                
                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.01)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Trapped_Mine',
                                                                        timeout=2,
                                                                        settle_delay=0.01,
                                                                        confidence=0.85)

            if "mushrock" in primary_button or "firestone" in primary_button:
                for x in range(40,81,40):
                    nf.tap(xCor + x, yCor)

                # for y in range(40,81,40):
                #     nf.tap(xCor, yCor - y)

            elif "agate" in primary_button or "sapphire" in primary_button:
                for x in range(40,81,40):
                    nf.tap(xCor - x, yCor)

                # for y in range(40,81,40):
                #     nf.tap(xCor, yCor + y)

            elif "ruby" in primary_button or "topaz" in primary_button:
                for x in range(40,81,40):
                    nf.tap(xCor - x, yCor)
                
                for y in range(40,81,40):
                    nf.tap(xCor, yCor + y)

            elif "gold" in primary_button:
                for x in range(40,81,40):
                    nf.tap(xCor + x, yCor)
                
                for y in range(40,81,40):
                    nf.tap(xCor, yCor + y)


            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Trapped_Mine',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

        else:
            secondary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'costumes_x_button.png',
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.85)
            
            if secondary_button:
                nf.tap(xCor, yCor)

def muddy_plains_routine():

    last_speed_upgrade = datetime.datetime.now()


    for x in range(100):
        nf.scroll_down(settle_delay=0.1)
        scroll_down_indicator, scroll_down_x_cor, scroll_down_y_cor = nf.MoveToLocation(file_path='scroll_down_indicator.png',
                                                                        parent_directory='Idle_Miner\\Muddy_Plains',
                                                                        timeout=3,
                                                                        confidence=0.80,
        )
        
        if scroll_down_indicator != "":
            print("We have reached the ideal to begin the routine")
            break

    phase_one_complete = False

    open_up_gear()

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'peridot_ore_sign.png',
                                    'copper_ore_sign.png',
                                    'onyx_ore_sign.png',
                                    'emerald_ore_sign.png',
                                    'silver_ore_sign.png',
                                    'ruby_ore_sign.png',
                                    'mushrock_ore_sign.png',
                                    'generic_ore_sign.png'
                                ],
                                    parent_directory='Idle_Miner\\Muddy_Plains',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Muddy_Plains',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":
                
                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.01)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Muddy_Plains',
                                                                        timeout=2,
                                                                        settle_delay=0.01,
                                                                        confidence=0.85)


                
            if "ruby" in primary_button or "mushrock" in primary_button:
                for y in range(40,201,40):
                    nf.tap(xCor, yCor + y)
            
            elif "silver" in primary_button:
                for x in range(40,121,40):
                    nf.tap(xCor + x, yCor + 20)

            elif "emerald" in primary_button:
                for x in range(40,81,40):
                    nf.tap(xCor - x, yCor)
                
                for y in range(40,161,40):
                    nf.tap(xCor, yCor + y)

            elif "onyx" in primary_button:
                for x in range(40,81,40):
                    nf.tap(xCor + x, yCor)
                
                for y in range(40,161,40):
                    nf.tap(xCor, yCor + y)
            
            elif "peridot" in primary_button:
                for x in range(40,81,40):
                    xCor += x
                    nf.tap(xCor, yCor)
                
                for y in range(40,121,40):
                    nf.tap(xCor, yCor + y)
            
            elif "copper" in primary_button:    
                for x in range(40,81,40):
                    xCor += (x * -1)
                    nf.tap(xCor, yCor)
                
                for y in range(40,121,40):
                    nf.tap(xCor, yCor + y)
                    

            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Muddy_Plains',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

        else:
            secondary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'costumes_x_button.png',
                                    'upgrades_x_button.png'
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.85)
            
            if secondary_button:
                nf.tap(xCor, yCor)

def redstone_ravine_routine():

    last_speed_upgrade = datetime.datetime.now()

    agate_ore_maxed = False

    while True:

        search_for_gift()

        primary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'continue_button.png',
                                    'upgrade_available_button.png',
                                    'ruby_ore_sign.png',
                                    'firestone_ore_sign.png',
                                    'agate_ore_sign.png',
                                    'emerald_ore_sign.png',
                                    'mushrock_ore_sign.png',
                                    'onyx_ore_sign.png',
                                    'peridot_ore_sign.png',
                                    'generic_ore_sign.png'
                                ],
                                    parent_directory='Idle_Miner\\Redstone_Ravine',
                                    timeout=5,settle_delay=0.01,confidence=0.85)

        if primary_button == 'continue_button.png':
            print("We have completed the Starter Mine Routine")
            nf.tap(xCor, yCor)
            return True

        #Found the Emerald Ore Sign
        elif "ore_sign.png" in primary_button:

            print(primary_button)

            #Tap the Ore Sign
            nf.tap(xCor, yCor)

            #Locate the Ore Upgrade Button
            upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Redstone_Ravine',
                                                                        timeout=5,
                                                                        confidence=0.85)

            if upgrade_ore_button != "":
                
                
                #Hold the Upgrade Button for 3 seconds
                while upgrade_ore_button != "":
                    nf.tap(upgrade_x_cor, upgrade_y_cor, settle_delay= 0.01)
                    upgrade_ore_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_ore_button.png',
                                                                        parent_directory='Idle_Miner\\Redstone_Ravine',
                                                                        timeout=5,
                                                                        settle_delay=0.01,
                                                                        confidence=0.85)

            if "onyx" in primary_button:
                #Click on the crates to unlock the ore crystals
                for y_offset in range(50,201,50):
                    nf.tap(xCor, yCor - y_offset)

                for x_offset in range(50,251,50):
                    nf.tap(xCor + x_offset, yCor)

            elif "peridot" in primary_button:
                #Click on the crates to unlock the ore crystals
                for y_offset in range(50,201,50):
                    nf.tap(xCor, yCor - y_offset)

                for x_offset in range(50,251,50):
                    nf.tap(xCor - x_offset, yCor)
            else:   
                #Click on the crates to unlock the ore crystals
                for y_offset in range(25,101,25):
                    nf.tap(xCor, yCor + y_offset)
                    nf.tap(xCor + 40,yCor + y_offset)


            #Perform a Reset Tap to reset menus
            reset_tap()
    

        elif primary_button == "upgrade_available_button.png":

            #Tap the Upgrade Available Button
            nf.tap(xCor, yCor)

            #Locate the Upgrade Button
            upgrade_button, upgrade_x_cor, upgrade_y_cor = nf.MoveToLocation(file_path='upgrade_button.png',
                                                                        parent_directory='Idle_Miner\\Redstone_Ravine',
                                                                        timeout=5,
                                                                        confidence=0.85)
            
            if upgrade_button != "":
                #Tap the Upgrade Button 10 times
                for x in range(10):
                    nf.tap(upgrade_x_cor, upgrade_y_cor)

                #Perform a Reset Tap to reset menus
                reset_tap()

        else:
            secondary_button, xCor, yCor = nf.MoveToLocationList(file_paths=[
                                    'costumes_x_button.png',
                                    'upgrades_x_button.png'
                                    ],
                                    parent_directory='Idle_Miner',
                                    timeout=5,settle_delay=0.01,confidence=0.85)
            
            if secondary_button:
                nf.tap(xCor, yCor)

routine_dictionary = {
    "Starter_Mine": starter_mine_routine,
    "Village_Mine": village_mine_routine,
    "Deep_Deep_Caves": deep_deep_caves_routine,
    "River_Crossing": river_crossing_routine,
    "Coal_Mines": coal_mines_routine,
    "Gilded_Grasslands": gilded_grasslands_routine,
    "Obsidian_Drains": obsidian_drains_routine,
    "Trapped_Mine": trapped_mine_routine,
    "Muddy_Plains":muddy_plains_routine,
    "Redstone_Ravine":redstone_ravine_routine
}


def search_for_gift():
    #Locate the Upgrade Button
    gift_icon, gift_icon_x_cor, gift_icon_y_cor = nf.MoveToLocation(file_path='gift_icon.png',
                                                                        parent_directory='Idle_Miner',
                                                                        timeout=3,
                                                                        confidence=0.75)
    
    if gift_icon != "":
        nf.tap(gift_icon_x_cor, gift_icon_y_cor)

        #Locate the Upgrade Button
        claim_icon, claim_icon_x_cor, claim_icon_y_cor = nf.MoveToLocation(file_path='claim_gift_button.png',
                                                                        parent_directory='Idle_Miner',
                                                                        timeout=3,
                                                                        confidence=0.85)
        
        if claim_icon != "":
            nf.tap(claim_icon_x_cor, claim_icon_y_cor)

            return True
        
    return False

if __name__ == "__main__":
    print("done")
    
    while(True):

        #Determine which mine you are currently in
        mine_name = identify_mine()

        #Run the routine for the current mine
        if (routine_dictionary[mine_name]()):
            print("We have completed the routine for the current mine")
            
            #Progress to the next mine
            progressing_to_next_mine()

        else:
            print("The routine for the current mine has failed. Exiting script.")
            exit()
    


