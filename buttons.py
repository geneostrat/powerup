import vlc
import RPi.GPIO as GPIO          #Import GPIO library
import time                      #Import time library
print('start')
GPIO.setmode(GPIO.BOARD)         #Set GPIO pin numbering
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors
while True:
    input_state = GPIO.input(37) #Read and store value of input to a variable
    if input_state == False:     #Check whether pin is grounded
       print('Button 2 Pressed')   #Print 'Button Pressed'
       time.sleep(0.3)           #Delay of 0.3s
    
    input_state = GPIO.input(35) #Read and store value of input to a variable
    if input_state == False:     #Check whether pin is grounded
       print('Button 1 Pressed')   #Print 'Button Pressed'
       time.sleep(0.3)           #Delay of 0.3s
    
    input_state = GPIO.input(33) #Read and store value of input to a variable
    if input_state == False:     #Check whether pin is grounded
       print('Button 4 Pressed')   #Print 'Button Pressed'
       time.sleep(0.3)           #Delay of 0.3s
       command = "/usr/bin/sudo /sbin/shutdown -h now"
       import subprocess
       process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
       output = process.communicate()[0]
       print(output)       
       
    
    input_state = GPIO.input(31) #Read and store value of input to a variable
    if input_state == False:     #Check whether pin is grounded
       print('Button 3 Pressed')   #Print 'Button Pressed'
       time.sleep(0.3)           #Delay of 0.3s
       media = vlc.MediaPlayer("./Videos/wserhwsrhwsrjerwsdj_13.mp4")
       media.play()