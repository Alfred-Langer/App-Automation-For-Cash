import CryptoMiningTycoon
import MergeMonsters
import BitcoinMiner
import NavigationFunctions as nf
import os
import sys
import ast
from discord_webhook import DiscordWebhook

if __name__ == "__main__":

    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1349207128002531448/rDeX_u8bD4pT0SPvtQsCzID6FgvLABPZCQXiaFpY3ttS_z4IAxwxLBlUuOg1_neWFpcg")

    if len(sys.argv) >= 2:
        if sys.argv[1] == "left":
            instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_LEFT_REGION_RECTANGLE"))
            side = sys.argv[1]
        elif sys.argv[1] == "right":
            instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_RIGHT_REGION_RECTANGLE"))
            side = sys.argv[1]
        else:
            print("Invalid argument. Please enter either 'left' or 'right' as an argument.")
            exit()
        
    else:
        instance_region_rectangle = ast.literal_eval(os.getenv("SCRCPY_REGION_RECTANGLE"))


    if len(sys.argv) == 3:
        serial_number = sys.argv[2]
    else:
        serial_number = None
    
    # crypto_mining_tycoon_result = CryptoMiningTycoonUnfinished.main(side, serial_number)
    # #crypto_mining_tycoon_result = CryptoMiningTycoonUnfinished.main("left", "21121FDF6005BU")
    # #crypto_mining_tycoon_result = CryptoMiningTycoonUnfinished.main("right", "RFCR10L1D7D")
    # if(crypto_mining_tycoon_result):
    #     print("Successfully completed the Crypto Mining Tycoon main function.")
    #     webhook.content = "Successfully completed the Crypto Mining Tycoon main function."
    #     webhook.execute()

    # else:
    #     print("Failed to complete the Crypto Mining Tycoon main function.")
    #     webhook.content = "Failed to complete the Crypto Mining Tycoon main function."
    #     webhook.execute()

    # merge_monsters_result = MergeMonstersUnfinished.main(side, serial_number)
    # #merge_monsters_result = MergeMonstersUnfinished.main("left", "21121FDF6005BU")
    # #merge_monsters_result = MergeMonstersUnfinished.main("right", "RFCR10L1D7D")
    # if(merge_monsters_result):
    #     print("Successfully completed the Merge Monsters main function.")
    #     webhook.content = "Successfully completed the Merge Monsters main function."
    #     webhook.execute()

    # else:
    #     print("Failed to complete the Merge Monsters main function.")
    #     webhook.content = "Failed to complete the Merge Monsters main function."
    #     webhook.execute()

    BitcoinMiner.main(side, serial_number)
    #BitcoinMinerUnfinished.main("left", "21121FDF6005BU")
    #BitcoinMinerUnfinished.main("right", "RFCR10L1D7D")