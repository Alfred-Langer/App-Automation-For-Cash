import NavigationFunctions as nf
import time


while True:
    print('Swiping up')
    nf.swipe(540,900,540,1500,500)
    time.sleep(0.5)
    print("Swiping down")
    nf.swipe(540,1500,540,900,500)
    time.sleep(0.5)
    nf.tap(287,1802,non_scale=True)
    time.sleep(0.5)