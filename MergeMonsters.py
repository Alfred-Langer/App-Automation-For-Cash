import NavigationFunctions as nf
import time
from discord_webhook import DiscordWebhook
import os
import pyautogui
import sys
import ast

def main(side=None, serial=None):

    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)


    if side is not None and serial is not None:
        sys.argv = ["MergeMonstersUnfinished.py",side, serial]

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
    if (nf.reset_from_unknown_state_return(app_icon="merge_monsters_app" , serial=serial_number, region_rectangle=instance_region_rectangle)):
        print("Successfully reset the phone.")
    else:
        print("Unable to find the app icon. Returning false on the Crypto Mining Tycoon main function.")
        return False
    
    ad_counter = 0
    end_time = time.time() + 60*60 * 1.5
    while time.time() < end_time:

        primary_button , x_cor, y_cor = nf.MoveToLocationDictionary(file_paths={
                                                                        'skip_button.png':(
                                                                            instance_region_rectangle[0],
                                                                                (instance_region_rectangle[1]+instance_region_rectangle[3])//2,
                                                                                (instance_region_rectangle[2]+instance_region_rectangle[0])//2,
                                                                                ((instance_region_rectangle[1]+instance_region_rectangle[3]//2) + instance_region_rectangle[3])//2
                                                                        ),
                                                                        'activate_button.png':(
                                                                            (instance_region_rectangle[2]+instance_region_rectangle[0])//2,
                                                                                (instance_region_rectangle[1]+instance_region_rectangle[3])//2,
                                                                                instance_region_rectangle[2],
                                                                                ((instance_region_rectangle[1]+instance_region_rectangle[3]//2) + instance_region_rectangle[3])//2
                                                                        ),
                                                                        'ready_button.png':(
                                                                                instance_region_rectangle[0] + 135,
                                                                                instance_region_rectangle[1]+instance_region_rectangle[3]//2,
                                                                                instance_region_rectangle[0] + 210,
                                                                                instance_region_rectangle[3]
                                                                        ),
                                                                        'close_auto_merge_menu_button.png':instance_region_rectangle,
                                                                        'done_button.png':instance_region_rectangle,
                                                                        'close_button.png':instance_region_rectangle,
                                                                        'main_screen_indicator.png':(
                                                                                instance_region_rectangle[0],
                                                                                instance_region_rectangle[3] - 100,
                                                                                instance_region_rectangle[2],
                                                                                instance_region_rectangle[3]
                                                                        ),
                                                                        },
                                                                        gray_scale_flag=True,
                                                                        parent_directory="Merge_Monsters",
                                                                        timeout=10,
                                                                        confidence=0.85)
        if not primary_button:
                print("No button found, assuming we are in an advertisement.")
                if (not nf.clear_advertisement_2(timeout=180,serial=serial_number, region_rectangle=instance_region_rectangle)):
                    webhook.content = "Unknown advertisement found. Please check the screen for the advertisement and take a screenshot."
                    webhook.execute()
                    pyautogui.screenshot(f"./Screenshots/Advertisements/Advertisement_{time.time()}.png")

                    if (nf.reset_from_unknown_state_return(app_icon="merge_monsters_app" , serial=serial_number, region_rectangle=instance_region_rectangle)):
                        print("Successfully reset the phone.")
                    else:
                        print("Unable to find the app icon. Returning false on the Crypto Mining Tycoon main function.")
                        return False

                else:
                    ad_counter += 1

                    if ad_counter >= 6:
                        print("We've seen 3 ads without a primary button. Performing a reset.")
                        if (nf.reset_from_unknown_state_return(app_icon="merge_monsters_app" , serial=serial_number, region_rectangle=instance_region_rectangle)):
                            print("Successfully reset the phone.")
                        else:
                            print("Unable to find the app icon. Returning false on the Crypto Mining Tycoon main function.")
                            return False
                        ad_counter = 0
                continue
        
        else:
            ad_counter = 0
            if primary_button == "ready_button.png":
                print(f"{primary_button} has been found. Proceeding to activate Boost Sequence")
                nf.tap(x_cor,y_cor, x_offset=150, settle_delay=2,serial=serial_number,region_rectangle=instance_region_rectangle)

            elif "button.png" in primary_button:
                print(f"{primary_button} has been found. Tapping on the button now.")
                nf.tap(x_cor,y_cor,settle_delay=2,serial=serial_number,region_rectangle=instance_region_rectangle)
            
            elif "indicator.png" in primary_button:
                print(f"{primary_button} has been found. We are on the main screen.")
                time.sleep(1)
    
    return True

if __name__ == "__main__":
    main()