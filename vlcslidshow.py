import vlc
import time

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
player.set_fullscreen(True)
Media = vlc_instance.media_new( "for-those-about-to-rock.jpg" )
player.set_media(Media)
player.play()
time.sleep(5)
Media = vlc_instance.media_new( "dirty-deeds.jpg" )
player.set_media(Media)
player.play()
time.sleep(5)
exit()