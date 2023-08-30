import vlc
import time
#import keyboard 

# https://www.geeksforgeeks.org/vlc-module-in-python-an-introduction/

media_player = vlc.MediaPlayer()

# toggling full screen
#media_player.toggle_fullscreen()

for i in range (1,10):
    # media object
    media = vlc.Media("./Videos/dirty-deeds.mp4") #wserhwsrhwsrjerwsdj_13.mp4")
     
    # setting media to the media player
    media_player.set_media(media)
 
    # start playing video
    media_player.play()    
    # wait so the video can be played for 5 seconds
    # irrespective for length of video
    #time.sleep(5)
    for k in range (1,15):
        print('hi')
        time.sleep(0.3) 
    

    media = vlc.Media("./Videos/backinblack.mp4") #wserhwsrhwsrjerwsdj_13.mp4")
    media_player.set_media(media)
    media_player.play()
    time.sleep(5)

    media = vlc.Media("./Videos/wserhwsrhwsrjerwsdj_13.mp4")
    media_player.set_media(media)
    media_player.play()
    time.sleep(35)

    print('loop: ',i)

exit()


# creating vlc media player object
#media = vlc.MediaPlayer("./Videos/dirty-deeds.mp4") #wserhwsrhwsrjerwsdj_13.mp4")
 
# start playing video
#media.play()

'''

    # creating a vlc instance
    vlc_instance = vlc.Instance()
     
    # creating a media player
    player = vlc_instance.media_player_new()
     
    # creating a media
    media = vlc_instance.media_new(source)
     
    # setting media to the player
    player.set_media(media)
     
    # play the video
    player.play()
     
    # wait time
    time.sleep(0.5)
'''
