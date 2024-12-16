import pyautogui
import datetime
import time
import sys
import os


def main():
    # Check to see if a directory was passed in as an argument
    if len(sys.argv) >= 2:
        screenshot_dir = os.path.join("./Screenshots/", sys.argv[1])
        if os.path.exists(screenshot_dir):
            print(f"Placing screenshots in directory: {screenshot_dir}")
    else:
        print("Provide a single valid directory to place screenshots in.")
        sys.exit(1)

    # Check if a delay was passed in as an argument
    if len(sys.argv) >= 3:
        try:
            delay = float(sys.argv[2])
        except ValueError:
            print("Invalid delay passed in. Defaulting to 0.5 seconds.")
            delay = 0.5
    else:
        print("No delay was passed in. Defaulting to 0.5 seconds.")
        delay = 0.5

    # Take a screenshot of the current screen and save it to the specified directory
    time.sleep(delay)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(screenshot_dir, f"{timestamp}.png")
    pyautogui.screenshot(screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")

if __name__ == "__main__":
    main()