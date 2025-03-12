
import NavigationFunctions as nf
import time
from discord_webhook import DiscordWebhook
import os
import pyautogui
import sys
import ast

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)


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


last_auto_merge = time.time()

while True:

    primary_button , x_cor, y_cor = nf.MoveToLocationList(file_paths=[
                                                                      #'accept_offer_button.png',
                                                                      'no_thanks_button.png',
                                                                      'auto_click_button.png',
                                                                      'main_screen_indicator.png'
                                                                      ],
                                                                      gray_scale_flag=True,
                                                                      parent_directory="Make_Cash",
                                                                      region_rectangle=instance_region_rectangle,
                                                                      timeout=10,
                                                                      confidence=0.75)
    
    if primary_button == "accept_offer_button.png":
        print("Accept Offer Button has been found. Tapping on the button now and then proceeding to look for advertisements.")
        nf.tap(x_cor,y_cor,settle_delay=2,serial=serial_number,region_rectangle=instance_region_rectangle)


        #Look for clear advertisement buttons
        if (not nf.clear_advertisement_2(timeout=300,serial=serial_number, region_rectangle=instance_region_rectangle)):
            webhook.content = f"Unknown advertisement found. Please check the screen for the advertisement and take a screenshot."
            webhook.execute()
            pyautogui.screenshot(f"./Screenshots/Advertisements/Advertisement_{time.time()}.png")

            #Reset from unknown state
            nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle, app_icon="make_cash_app")

    elif primary_button == "auto_click_button.png" or primary_button == "no_thanks_button.png":
        print(f"{primary_button} has been found. Tapping on the button now.")
        nf.tap(x_cor,y_cor,settle_delay=2,serial=serial_number,region_rectangle=instance_region_rectangle)
    
    elif "indicator.png" in primary_button:
        print(f"{primary_button} has been found. We are on the main screen.")
        time.sleep(2)
    else:
        print("Could not find any of the primary images, assuming we are in an advertisement.")
        if (not nf.clear_advertisement_2(timeout=150,serial=serial_number, region_rectangle=instance_region_rectangle)):
            webhook.content = f"Unknown advertisement found. Please check the screen for the advertisement and take a screenshot."
            webhook.execute()
            pyautogui.screenshot(f"./Screenshots/Advertisements/Advertisement_{time.time()}.png")

            #Reset from unknown state
            nf.reset_from_unknown_state(serial=serial_number, region_rectangle=instance_region_rectangle, app_icon="make_cash_app")

