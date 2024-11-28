import pyautogui
import datetime
import time

#Take a screenshot of the current screen
for x in range(1):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pyautogui.screenshot(f"./Screenshots/Bitcoin_Miner/{timestamp}.png")
    time.sleep(0.5)
