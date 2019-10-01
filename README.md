# GPIOGUI
A Python GUI for the Raspberry Pi GPIO pins

Import this to a Python program if you are using the GPIO pins. It will generate a GUI where you can see and change all pins' statuses. 

At the start of the program it sets all pins to GPIO.IN, so if you start it while pins are already in use it might mess you up.

You can set the rate the program scans the pins using the 'currentRefreshRate' parameter. By default it is set to scan every 100 ms.

Right now it only works with 'GPIO.setmode(GPIO.BOARD)'. 
