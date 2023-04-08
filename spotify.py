from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import credentials

class Spotify():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.headless = True


        self.driver = webdriver.Chrome(credentials.webdriverLocation)



        self.url = r'https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F'


    def login(self, Email, Password):
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.find_element(By.XPATH, "//input[@id='login-username']").send_keys(Email)
        self.driver.find_element(By.XPATH, "//input[@id='login-password']").send_keys(Password)
        self.driver.find_element(By.XPATH, "//button[@id='login-button']").click()

    def openTab(self):
        self.driver.execute_script('window.open("");')

    def openSpotify(self, link=None):
        if link == None:
            self.driver.execute_script('window.open("https://open.spotify.com/");')
        else:
            self.driver.execute_script(f'window.open("{link}")')


    def closeFirstTab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def closeReopen(self, link=None):
        self.openTab()
        self.closeFirstTab()
        self.openSpotify(link)
        self.closeFirstTab()
        print("ad skipped")

    def setVolume(self, volume):
        volumeXPATH = "//*[@id='main']/div/div[2]/div[2]/footer/div/div[3]/div/div[3]"
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, volumeXPATH)))
        action = ActionChains(self.driver)
        action.move_to_element(self.driver.find_element(By.XPATH, volumeXPATH)).move_by_offset(((int(volume)/100)*(62+27))-27, 0).click().perform()
        print("volume set to " + str(volume))

    def playPlaylist(self):
        buttonXPATH = "//button[@class='Button-sc-qlcn5g-0 jqMzOG']"
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, buttonXPATH)))
        self.driver.find_element(By.XPATH, buttonXPATH).click()
        print("playlist started")

    def playSong(self):
        self.driver.find_element(By.XPATH, "//button[@class='vnCew8qzJq3cVGlYFXRI']").click() #add wait till button is clickable just in case

    def skipSong(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]"))).click()
        print("song skipped")

    def spamSkip(self, stop):
        while True:
            try:
                self.skipSong()
            except:
                pass
            if stop():
                return

    def backSong(self):
        self.driver.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[2]").click()

    def enableShuffle(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='KVKoQ3u4JpKTvSSFtd6J']"))).click()
        print("shuffle enabled")

    def waitUntilAd(self, stop):
        print("WAITING FOR AD")
        for i in range(400):
            try:
                self.driver.find_element(By.XPATH, "//a[@data-testid='context-item-info-ad-subtitle']")
                print("found ad!")
                return True
            except:
                print("no ads")
                if stop():
                    print("STOPPED WATCHING FOR ADS")
                    return False
                else: sleep(5)


    def adWatch(self, stop, errors):
        while not stop():
            playlistURL = self.driver.current_url
            if playlistURL == "https://open.spotify.com/":
                print("ERROR. PLEASE SELECT A PLAYLIST BEFORE STARTING ADWATCH")
                errors[len(errors)] = [10, "ERROR: Please select a playlist before starting AdWatch"]
                return
            if self.waitUntilAd(stop):
                print("AD WATCHED")
                self.closeReopen(playlistURL)
                self.setVolume()
                self.playPlaylist()
                self.enableShuffle()
                sleep(1) # reduce this
                self.skipSong()


