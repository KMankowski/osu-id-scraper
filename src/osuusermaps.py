import osuuserid as idscraper
import sys
import time
from selenium import webdriver

# Setup browser.
PATH = '/Users/owner/Desktop/chromedriver'
browser = webdriver.Chrome(PATH)

# Get 'Osu!' username to find the beatmaps for.
osuUserName = input('Please enter an Osu! username to get their beatmaps: ')

# Get the 'Osu!' ID of the user requested. Program exits if not found.
osuUserAndID = idscraper.getID(osuUserName, browser)
if osuUserAndID == None:
    print("Sorry, we couldn't find that user!")
    sys.exit()
else:
    osuID = osuUserAndID[1]

# Get the beatmap information of the user. #
browser.get('https://osu.ppy.sh/users/' + osuID)
beatmaps = browser.find_elements_by_css_selector(
    "[data-page-id='beatmaps']")[1]

# Show all maps. IF AN EXCEPTION IS THROWN, CHECK THAT SELENIUM (ie. '.click()') IS NOT OUTPACING 'time.sleep()'.
showmoreButtons = beatmaps.find_elements_by_class_name('show-more-link')
while len(showmoreButtons) > 0:
    for showmoreButton in showmoreButtons:
        showmoreButton.click()
        time.sleep(.3)
    showmoreButtons = beatmaps.find_elements_by_class_name('show-more-link')


rankedAndApprovesMaps = ''
lovedMaps = ''
pendingMaps = ''
graveyardedMaps = ''

browser.quit()
sys.exit()
