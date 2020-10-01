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
        time.sleep(1)
    showmoreButtons = beatmaps.find_elements_by_class_name('show-more-link')

# This is going to drive me crazy, but I can't think of a better solution at the moment.
# In the beatmap section of the users page, 'osu-layout__col-container' only exists for
# a category of map that has *at least one beatmap present*. As a result, this extra logic
# needs to be added to determine which beatmap section found corresponds to ranked, loved, etc...
# If a better solution is available, a contribution would be very much appreciated!
beatmapSections = beatmaps.find_elements_by_class_name(
    'osu-layout__col-container')


# Currently, this method should be unable to be called with len(beatmapSections) == 0,
# but this could change with future updates. Handling for such an occurrence should be implemented if so.
def hasFavorites(beatmapSections):
    # Get first beatmap listed on user page.
    return osuID != beatmapSections[0].find_element_by_css_selector("a[data-user-id]").get_attribute('href').split('/')[4]


# Split this function up into two chained functions (notice the replicated code inside of each 'if' statement).
# WILL NOT FIND FAVORITES AT THE MOMENT.
# With the current setup, beatmapSections should never be able to have a size of 0,
# but this could change with future updates. Handling for such an occurrence should be implemented if so.
def getMapsInSection(beatmapSectionToFind, beatmapSections, userHasFavorites):
    for index in range(userHasFavorites, len(beatmapSections)):
        sectionStatus = beatmapSections[index].find_element_by_class_name(
            'beatmapset-status').text
        if ((beatmapSectionToFind == 'RANKED AND APPROVED') and (sectionStatus == 'APPROVED' or sectionStatus == 'RANKED')) or beatmapSectionToFind == sectionStatus:
            beatmapDivsInSection = beatmapSections[index].find_elements_by_class_name(
                'osu-layout__col--sm-6')
            mapTagsInSection = []
            for beatmapDiv in beatmapDivsInSection:
                mapTagsInSection.append(
                    beatmapDiv.find_element_by_class_name('beatmapset-panel__header'))
            mapIDsInSection = []
            for beatmap in mapTagsInSection:
                mapIDsInSection.append(
                    int(beatmap.get_attribute('href').split('/')[4]))
            return mapIDsInSection
    return []


if len(beatmapSections) == 5:
    rankedAndApprovedMapIDs = beatmapSections[1].find_elements_by_tag_name('a')
    lovedMapIDs = beatmapSections[2].find_elements_by_tag_name('a')
    pendingMapIDs = beatmapSections[3].find_elements_by_tag_name('a')
    graveyardMapIDs = beatmapSections[4].find_elements_by_tag_name('a')
elif len(beatmapSections) == 0:
    rankedAndApprovedMapIDs = []
    lovedMapIDs = []
    pendingMapIDs = []
    graveyardMapIDs = []
else:
    ifUserHasFavorites = hasFavorites(beatmapSections)
    rankedAndApprovedMapIDs = getMapsInSection(
        'RANKED AND APPROVED', beatmapSections, ifUserHasFavorites)
    lovedMapIDs = getMapsInSection(
        'LOVED', beatmapSections, ifUserHasFavorites)
    pendingMapIDs = getMapsInSection(
        'PENDING', beatmapSections, ifUserHasFavorites)
    graveyardMapIDs = getMapsInSection(
        'GRAVEYARD', beatmapSections, ifUserHasFavorites)

mapIDCollection = (rankedAndApprovedMapIDs, lovedMapIDs,
                   pendingMapIDs, graveyardMapIDs)

print(mapIDCollection)

browser.quit()
sys.exit()
