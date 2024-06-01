import time
time.sleep(0.1) # Wait for USB to become ready

from MusicController import *


print("Hello, Pi Pico!")

piano = MusicController()

piano.testDisplay()

piano.testLightstrip()

MusicController().run()
