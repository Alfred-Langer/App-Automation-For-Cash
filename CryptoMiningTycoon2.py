import pyautogui
import NavigationFunctions as nf
import time




while True:
    primary_button, x_cor, y_cor = nf.MoveToLocationList(file_paths=['increase_quantity.png','pay_bill.png'],
                                                                        parent_directory='Crypto_Mining_Tycoon',
                                                                        timeout=5,
                                                                        gray_scale_flag=False,
                                                                        confidence=0.90)
    print(primary_button)

    
    nf.tap(x_cor, y_cor)


    if primary_button == "increase_quantity.png":
        take_button, x_cor, y_cor = nf.MoveToLocation(file_path='take_button.png',
                                                                        parent_directory='Crypto_Mining_Tycoon',
                                                                        timeout=5,
                                                                        confidence=0.85)
        if take_button:
            nf.tap(x_cor, y_cor)

