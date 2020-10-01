import osuuserid as idscraper
import sys
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

print(osuID)


# Get the beatmap information of the user.
browser.get('https://osu.ppy.sh/users/' + osuID)
beatmaps = browser.find_element_by_css_selector("[data-page-id='beatmaps']")

# Show all maps
showMoreButtons = beatmaps.find_elements_by_class_name('show-more-link')
print(len(showMoreButtons))


rankedAndApprovesMaps = ''
lovedMaps = ''
pendingMaps = ''
graveyardedMaps = ''

browser.quit()
sys.exit()
