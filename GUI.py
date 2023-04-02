import PySimpleGUI as sg
import threading
import spotify
import credentials

def checkAdWatchOnce():
    for threads in threading.enumerate():
        if threads.name == "adWatch":
            # print("ad is being watched")
            return True
    # print("no ad is being watched")
    return False

def checkAdWatchProcess(ad_watch, window):
    while True:
        ad_watch.append(checkAdWatchOnce())
        if ad_watch[1] != ad_watch[0]:
            print("AD WATCH CHANGED")
            if ad_watch[1]:
                window["-ENABLED-"].update("Ad Watch Enabled")
                window['-AD-'].update(button_color = "Red")
            else:
                window["-ENABLED-"].update("")
                window["-AD-"].update(button_color = "Green")
            
        ad_watch.pop(0)

def main():
    music = spotify.Spotify()
    print(music)

    music.login(credentials.username, credentials.password)
    music.setVolume()

    sg.theme = "DarkTeal"
    # sg.set_global_icon() # TODO: eventually
    sg.set_options(font="Helvetica", margins=(10, 10))

    layout = [[sg.Text(size=(15, 1), key="-ENABLED-")],
               [sg.Button('Play/Pause', button_color="Green", key='-PLAY-'), sg.Button('AdWatch', button_color="Green", key='-AD-')]]
    
    window = sg.Window("Spotify", layout, finalize=True)

    ad_watch_enabled = False

    ads = [False]
    ad_watch_watcher = threading.Thread(target=checkAdWatchProcess, args=(ads, window), name="adWatchWatch", daemon=True)
    ad_watch_watcher.start()
    
    while True: # event loop
        event, values = window.read()

        print(event, values) # DEBUGGING

        if event == sg.WIN_CLOSED:
            break
        if event == '-AD-':
            print(f"ad_watch_enabled: {ad_watch_enabled}, ad_watch[0]: {ads[0]}")
            if ads[0] == False: # enable ad watch
                tmp = threading.Thread(target=music.adWatch, args=(lambda: not ad_watch_enabled,), name="adWatch")
                tmp.start()
                ad_watch_enabled = True
            else: # disable ad watch
                ad_watch_enabled = False
        if event == '-PLAY-':
            music.playSong()
        
        

    window.close()



if __name__ == '__main__':
    main()
    

    


