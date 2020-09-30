''' This script takes input in the form of an 'Osu!' UserName, 
    utilizes Selenium to scrape Google for search results 
    containing 'osu.ppy.sh' that may be the user page for the requested user.
    If the correct user page is found, the ID of the user is ouput.
    
    Note. 'osu.ppy.sh' was not scraped directly as a user must be
           logged in to do so. '''

# TODO Refactor the code into understandable and clear functions.

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup webdriver ('PATH' is dependent on local machine).
PATH = '/Users/owner/Desktop/chromedriver'
browser = webdriver.Chrome(PATH)

# UserName for which the 'Osu!' ID will be found.
userToFind = input('Please enter an Osu! user to get their ID: ')

# Gets the Google search results for '<UserName> Osu!'.
browser.get('https://www.google.com')
searchbar = browser.find_element_by_name('q')
searchbar.send_keys(userToFind + ' Osu!')
searchbar.send_keys(Keys.RETURN)

# Parses out the actual content of the search results on Google,
# ensuring that the page is given proper time to load before searching.
try:
    searchcontent = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'rso'))
    )
except:
    print('Driver could not find Google searchcontent in time (load speed took too long).')
    browser.quit()

# A list of the search results on the first page given by Google.
searchResults = searchcontent.find_elements_by_class_name('g')

# Loops through each search result to check if it contains the page of the requested user.
for searchResult in searchResults:
    urlTag = searchResult.find_element_by_tag_name('a')
    urlString = urlTag.get_attribute('href')
    if urlString.startswith('https://osu.ppy.sh/users/'):
        browser.execute_script("window.open('');")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(urlString)
        userName = browser.find_element_by_class_name(
            'profile-info__name').find_element_by_tag_name('span').text
        isCorrectUser = ''
        while isCorrectUser != 'y' and isCorrectUser != 'n':
            isCorrectUser = input(
                'Is ' + userName + ' the user you were looking for? (y/n)')
        if isCorrectUser == 'y':
            urlSlices = browser.current_url.split('/')
            userID = urlSlices[len(urlSlices)-1]
            print('The user ID of ' + userName + ' is ' + userID)
            browser.quit()
            sys.exit()
        elif isCorrectUser == 'n':
            print("Okay, we'll look for another!")
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

print("Sorry, we couldn't find that Osu! user.")

# Clean up.
browser.quit()
sys.exit()
