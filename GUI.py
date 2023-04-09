import PySimpleGUI as sg
import threading
import spotify
import credentials
from queue import Queue
from time import sleep



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

def checkError(errors):
    for i in errors.values():
        if i[0] > 0:
            i[0] -= 0.5
            return i
    return None

def checkAndDisplayError(errors, window): # TODO: error with threading

    while True:
        
        if checkError(errors) != None:
            window["-ERROR-"].update(checkError(errors)[1])
        else: 
            window["-ERROR-"].update("")

        sleep(1)


def main():
    music = spotify.Spotify()

    music.login(credentials.username, credentials.password)
    sg.theme = "DarkTeal"
    # sg.set_global_icon() # TODO: eventually
    sg.set_options(font="Helvetica", margins=(10, 10))

    layout = [[sg.Text(size=(15, 1), key="-ENABLED-")],
               [sg.Button('Play/Pause', button_color="Green", key='-PLAY-'), sg.Button('AdWatch', button_color="Green", key='-AD-'), sg.Button("Spam (DEBUG)", button_color="Green", key='-SPAM-')],
               [sg.Button("-", key="-MINUS-", button_color="Green"), sg.Text("50", key="-VOLUME-"), sg.Button("+", key="-PLUS-", button_color="Green")],
               [sg.Text(key="-ERROR-", text_color=("Red"))]]
    
    window = sg.Window("Spotify", layout, finalize=True)

    ad_watch_enabled = False
    spamming = False

    volume = 50
    music.setVolume(volume)

    ads = [False]
    ad_watch_watcher = threading.Thread(target=checkAdWatchProcess, args=(ads, window), name="adWatchWatch", daemon=True)
    ad_watch_watcher.start()

    errors = {} # TODO: turn into a QUEUE
    error_checker = threading.Thread(target=checkAndDisplayError, args=(errors, window), name="ErrorChecker", daemon=True)
    error_checker.start()
    
    while True: # event loop
        event, values = window.read()

        print(event, values) # DEBUGGING

        if event == sg.WIN_CLOSED:
            break
        if event == '-AD-':
            print(f"ad_watch_enabled: {ad_watch_enabled}, ad_watch[0]: {ads[0]}")
            if ads[0] == False: # enable ad watch
                tmp = threading.Thread(target=music.adWatch, args=(lambda: not ad_watch_enabled, errors, volume), name="adWatch", daemon=True)
                tmp.start()
                ad_watch_enabled = True
            else: # disable ad watch
                errors[len(errors)] = [5, "Disabling Ad Watch"]
                ad_watch_enabled = False
        if event == '-PLAY-':
            music.playSong()
        if event == '-SPAM-':
            if spamming == False:
                tmp = threading.Thread(target=music.spamSkip, args=(lambda: not spamming,), daemon=True, name="SPAM!")
                tmp.start()
                spamming = True
            else:
                spamming = False
        if event == "-MINUS-":
            if volume > 0:
                volume -= 10
                setVolume = threading.Thread(target=music.setVolume, args=(volume,), name="SetVolume", daemon=True)
                setVolume.start()
                window["-VOLUME-"].update(str(volume))
            else:
                errors[len(errors)] = [2, "ERROR: Volume out of bounds"]
        if event == "-PLUS-":
            if volume < 100:
                volume += 10
                setVolume = threading.Thread(target=music.setVolume, args=(volume,), name="SetVolume", daemon=True)
                setVolume.start()
                window["-VOLUME-"].update(str(volume))
            else:
                errors[len(errors)] = [2, "ERROR: Volume out of bounds"]
                
        
        

    window.close()



if __name__ == '__main__':
    main()
    

    


