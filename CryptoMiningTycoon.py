import re
import pyautogui
import NavigationFunctions as nf
import time
from discord_webhook import DiscordWebhook
import os
import sys
import ast

def main(side=None, serial=None):
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    ad_counter = 0
    

    if side is not None and serial is not None:
        sys.argv = ["CryptoMiningTycoonUnfinished.py",side, serial]

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
    if (nf.reset_from_unknown_state_return(app_icon="crypto_mining_tycoon_app" , serial=serial_number, region_rectangle=instance_region_rectangle)):
        print("Successfully reset the phone.")
    else:
        print("Unable to find the app icon. Returning false on the Crypto Mining Tycoon main function.")
        return False
    
    end_time = time.time() + 60*60 * 1.5
    while time.time() < end_time:

        primary_button, x_cor, y_cor = nf.MoveToLocationList(file_paths=['continue_button.png','close_offer_button.png','in_game_ad_x_button.png','x_button.png','claim_button.png','ad_incoming.png','pay_bill.png','shopping_cart_button.png'],
                                                                            parent_directory='Crypto_Mining_Tycoon',
                                                                            timeout=25,
                                                                            gray_scale_flag=False,
                                                                            region_rectangle=instance_region_rectangle,
                                                                            confidence=0.85)
        if not primary_button:
            print("No button found, assuming we are in an advertisement.")
            if (not nf.clear_advertisement_2(timeout=300,serial=serial_number, region_rectangle=instance_region_rectangle)):
                webhook.content = f"Unknown advertisement found. Please check the screen for the advertisement and take a screenshot."
                webhook.execute()
                pyautogui.screenshot(f"./Screenshots/Advertisements/Advertisement_{time.time()}.png")

                if (nf.reset_from_unknown_state_return(app_icon="crypto_mining_tycoon_app" , serial=serial_number, region_rectangle=instance_region_rectangle)):
                    print("Successfully reset the phone.")
                else:
                    print("Unable to find the app icon. Returning false on the Crypto Mining Tycoon main function.")
                    return False

            else:
                ad_counter += 1

                if ad_counter >= 6:
                    print("We've seen 3 ads without a primary button. Performing a reset.")
                    if (nf.reset_from_unknown_state_return(app_icon="crypto_mining_tycoon_app" , serial=serial_number, region_rectangle=instance_region_rectangle)):
                        print("Successfully reset the phone.")
                    else:
                        print("Unable to find the app icon. Returning false on the Crypto Mining Tycoon main function.")
                        return False
                    ad_counter = 0
            continue

        else:
            print(primary_button)
            ad_counter = 0

            if primary_button == "claim_button.png":
                nf.tap(x_cor, y_cor, x_offset=150, y_offset=220, serial=serial_number,region_rectangle=instance_region_rectangle)
            
            elif primary_button == "ad_incoming.png":
                print("Found ad_incoming. Simply continuing.")
                continue
            
            elif primary_button == "shopping_cart_button.png":
                print("On the main screen so we are swiping down.")
                nf.swipe(
                        x1=int(nf.PHONE_SCREEN_RESOLUTION[0] / 2),
                        y1=int(nf.PHONE_SCREEN_RESOLUTION[1] * 0.1),
                        x2=int(nf.PHONE_SCREEN_RESOLUTION[0] / 2),
                        y2=int(nf.PHONE_SCREEN_RESOLUTION[1] *  0.7),
                        duration=100,
                        settle_delay=0.1,
                        serial=serial)
            else:
                nf.tap(x_cor, y_cor, serial=serial_number,region_rectangle=instance_region_rectangle)

        
    return True

if __name__ == "__main__":
    main()