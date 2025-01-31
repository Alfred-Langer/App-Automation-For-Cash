import NavigationFunctions as nf
import time
from discord_webhook import DiscordWebhook
import os
import pyautogui

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)

last_auto_merge = time.time()

while True:

    primary_button , x_cor, y_cor = nf.MoveToLocationList(file_paths=[
                                                                      'activate_auto_merge_button.png',
                                                                      'close_auto_merge_menu_button.png',
                                                                      'done_button.png',
                                                                      'close_button.png',
                                                                      'auto_merge_button.png',
                                                                      'main_screen_indicator.png'
                                                                      ],
                                                                      gray_scale_flag=False,
                                                                      parent_directory="Merge_Monsters",
                                                                      timeout=10,
                                                                      confidence=0.975)
    
    if primary_button == "auto_merge_button.png":
        if time.time() > last_auto_merge:
            print(f"{primary_button} has been found. Proceeding to activate Auto Merge Sequence")
            nf.tap(x_cor,y_cor,settle_delay=2)
            last_auto_merge = time.time() + 120

        else:
            main_screen_indicator =nf.MoveToLocation(file_path="main_screen_indicator.png",
                              parent_directory="Merge_Monsters",
                              timeout=10,
                              confidence=0.85)
            
            if main_screen_indicator[0] == "main_screen_indicator.png":
                print("We are on the main screen waiting for one minute to pass before proceeding to activate auto merge again.")

            else:
                print("Unable to find the main screen indictaor, assuming we are in an advertisement.")
                
                if (not nf.clear_advertisement_2()):
                    webhook.content = f"Unknown advertisement found. Please check the screen for the advertisement and take a screenshot."
                    webhook.execute()
                    pyautogui.screenshot(f"./Screenshots/Advertisements/Advertisement_{time.time()}.png")

    elif "button.png" in primary_button:
        print(f"{primary_button} has been found. Tapping on the button now.")
        nf.tap(x_cor,y_cor,settle_delay=2)
    
    elif "indicator.png" in primary_button:
        print(f"{primary_button} has been found. We are on the main screen.")
        time.sleep(1)
    else:
        print("Could not find any of the primary images, assuming we are in an advertisement.")
        if (not nf.clear_advertisement_2()):
            webhook.content = f"Unknown advertisement found. Please check the screen for the advertisement and take a screenshot."
            webhook.execute()
            pyautogui.screenshot(f"./Screenshots/Advertisements/Advertisement_{time.time()}.png")


