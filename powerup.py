# https://www.makeuseof.com/how-to-run-a-raspberry-pi-program-script-at-startup/
import vlc
import RPi.GPIO as GPIO          #Import GPIO library
import time                      #Import time library
import time
import subprocess
import os

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Globals
powerupAttract   = ["powerup.mp4", "qrcode.mp4"]
setlist          = []
selectSongIdx    = 0
currentVideoName = "powerup.mp4"
disp             = None
draw             = None
image            = None
width            = None
height           = None
font             = None
fontSmall        = None
top              = None
bottom           = None
x                = None
media_player = vlc.MediaPlayer()

def attractMode():
    print("attract")

def prevSong():
    global selectSongIdx
    selectSongIdx -= 1
    if selectSongIdx < 0:
       selectSongIdx = len(setlist)-1
       
def nextSong():
    global selectSongIdx
    selectSongIdx += 1
    if selectSongIdx == len(setlist):
       selectSongIdx = 0

def readSetList():
       global selectSongIdx
       global setlist
       with open("setlist.txt","r") as setlistFile:
              setlist = setlistFile.read().splitlines()

def readSPowerUp():
       global powerupAttract
       with open("powerup.txt","r") as powerup:
              powerupAttract = powerup.read().splitlines()

def readSongMetaData(song):
       song = '/'+song
       path = os.path.join(song, "meta.txt")
       with open(path,"r") as metad:
              songmetadata = metad.read().splitlines()

def listSongDirectory(song):
       path = os.path.join('./Videos/songs/', song)
       path = path.strip()
       files = os.listdir(path)
       sortedfiles = sorted(files)
       return sortedfiles
       
def getSongLength(file):
       parts = file.split('_')
       return parts[1]
         
def selectSong():
       global selectSongIdx
       song = setlist[selectSongIdx].strip()
       
       if song == 'SHUTDOWN':
              command = "/usr/bin/sudo /sbin/shutdown -h now"
              import subprocess
              process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
              output = process.communicate()[0]
              print(output)       
       
       videos = listSongDirectory(song)
       print(videos)
       for video in videos:
              length = getSongLength(video)
              retCode = playVideo(video, song, length)

def playVideo(video, song, length):
       filespec = os.path.join('./Videos/songs/', song, video)
       print(filespec)
       media = vlc.Media(filespec) 
       media_player.set_media(media)
       media_player.play()       
       for k in range (1,int(length)*3):
              time.sleep(0.3)        
              input_state = GPIO.input(19) #Read and store value of input to a variable - NEXT
              if input_state == False:     #Check whether pin is grounded              
                     break
              input_state = GPIO.input(26) #Read and store value of input to a variable - PREV
              if input_state == False:     #Check whether pin is grounded              
                     break
              

def updateDisplay():
       global selectSongIdx
       global currentVideoName
       global draw
       global disp
       global image
       global width
       global height
       global font
       global fontSmall
       global top
       global bottom
       global x
       
       # Draw a black filled box to clear the image.
       draw.rectangle((0, 0, width, height), outline=0, fill=0)

       draw.text((x, top + 0), "> " + setlist[selectSongIdx].replace(".mp4",""), font=fontSmall, fill=255)
       draw.text((x, top + 12), currentVideoName.replace(".mp4",""), font=font, fill=255)

       # Display image.
       disp.image(image)
       disp.show()
       

def main():
       global draw
       global disp
       global image
       global width
       global height
       global font
       global fontSmall
       global top
       global bottom
       global x
       global setlist;
       
       print('powerup - start!')
       readSetList()
       print(setlist)
       
       # Create the I2C interface.
       i2c = busio.I2C(SCL, SDA)
       
       # Create the SSD1306 OLED class.
       # The first two parameters are the pixel width and pixel height.  Change these
       # to the right size for your display!
       disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

       # Clear display.
       disp.fill(0)
       disp.show()       

       # Create blank image for drawing.
       # Make sure to create image with mode '1' for 1-bit color.
       width = disp.width
       height = disp.height
       image = Image.new("1", (width, height))

       # Get drawing object to draw on image.
       draw = ImageDraw.Draw(image)

       # Draw a black filled box to clear the image.
       draw.rectangle((0, 0, width, height), outline=0, fill=0)

       # Draw some shapes.
       # First define some constants to allow easy resizing of shapes.
       padding = -2
       top = padding
       bottom = height - padding
       # Move left to right keeping track of the current x position for drawing shapes.
       x = 0

       # Load default font.
       #font = ImageFont.load_default()

       # Alternatively load a TTF font.  Make sure the .ttf font file is in the
       # same directory as the python script!
       # Some other nice fonts to try: http://www.dafont.com/bitmap.php
       font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
       fontSmall = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)

       updateDisplay()
       
       #GPIO.setmode(GPIO.BOARD)         #Set GPIO pin numbering - its already in BCM mode
       GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors 37
       GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors 35
       GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors 33
       GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors 31

       GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors - shutdown 36
       while True:
           
           # 1 - NEXT
           input_state = GPIO.input(19) #Read and store value of input to a variable
           if input_state == False:     #Check whether pin is grounded
              print('Button 1 Pressed - NEXT')   #Print 'Button Pressed'
              nextSong()
              updateDisplay()
              time.sleep(0.3)           #Delay of 0.3s
           
           # 2 - PREVIOUS
           input_state = GPIO.input(26) #Read and store value of input to a variable
           if input_state == False:     #Check whether pin is grounded
              print('Button 2 Pressed - PREV')   #Print 'Button Pressed'
              prevSong()
              updateDisplay()
              time.sleep(0.3)           #Delay of 0.3s

           # 3 - SELECT
           input_state = GPIO.input(6) #Read and store value of input to a variable
           if input_state == False:     #Check whether pin is grounded
              print('Button 3 Pressed - SELECT')   #Print 'Button Pressed'
              selectSong()
              time.sleep(0.3)           #Delay of 0.3s
              #media = vlc.MediaPlayer("./Videos/wserhwsrhwsrjerwsdj_13.mp4")
              #media.play()
           
           # 4 - POWERUP
           input_state = GPIO.input(13) #Read and store value of input to a variable
           if input_state == False:     #Check whether pin is grounded
              print('Button 4 Pressed')   #Print 'Button Pressed'
              time.sleep(0.3)           #Delay of 0.3s
              command = "/usr/bin/sudo /sbin/shutdown -h now"
              import subprocess
              process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
              output = process.communicate()[0]
              print(output)       
              
           


if __name__=="__main__":
    main()
