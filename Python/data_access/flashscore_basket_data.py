"""

Automate scrapping from Flash Score
"""

import time
from typing import Dict

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

FLASHSCORE_URL = 'https://www.flashscore.com'
game = 'basketball'

# dictionary to hold all scraped data
all_leagues_data = {}
my_basketball_leagues = {}

# TODO - include this date in the logic - maybe read the last date from excel/database
last_cached_date = None


# TODO - important one for new browsers
def _remove_consent_form(browser: webdriver):
    # Reject all cookies - click button
    browser.find_element_by_css_selector(
        css_selector='.ot-sdk-columns.has-reject-all-button.ot-sdk-two').click()

    pass


def get_basketball_league_match_data(main_browser: webdriver, league_url: str) -> Dict:
    """
    Given the h_ref of a basketball league go to the page and get all the match data and return them in
    :param main_browser:
    :return: TODO
    """

    data_dict = {}

    time.sleep(3)

    # Open new browser to navigate to this league's page
    league_browser = webdriver.Firefox()

    league_browser.get(url=f'{league_url}')
    league_browser.maximize_window()
    time.sleep(5)

    _remove_consent_form(league_browser)

    # Go to the results tab
    league_browser.find_element_by_class_name('tabs__tab.results').click()

    time.sleep(2)

    all_matches = league_browser.find_elements_by_class_name('event__match.event__match--static.event__match--twoLine')
    for match in all_matches:

        home_team = match.find_element_by_class_name('event__participant.event__participant--home').text
        away_team = match.find_element_by_class_name('event__participant.event__participant--away').text

        match_name = home_team + "-" + away_team

        # start packing game data into dictionary
        data_dict[f'{match_name}'] = {}

        data_dict[f'{match_name}']['match_datetime'] = match.find_element_by_class_name('event__time').text

        data_dict[f'{match_name}']['home_team'] = home_team
        data_dict[f'{match_name}']['away_team'] = away_team

        data_dict[f'{match_name}']['home_total'] = \
            int(match.find_element_by_class_name('event__score.event__score--home').text)

        data_dict[f'{match_name}']['away_total'] = \
            int(match.find_element_by_class_name('event__score.event__score--away').text)

        print('now getting the quarter data')

        # now get the quarters' data
        for quarter in range(1, 5):
            data_dict[f'{match_name}'][f'home_q{quarter}'] = \
                int(match.find_element_by_class_name(f'event__part.event__part--home.event__part--{quarter}').text)

            data_dict[f'{match_name}'][f'away_q{quarter}'] = \
                int(match.find_element_by_class_name(f'event__part.event__part--away.event__part--{quarter}').text)

        # When all data is gathered, close the browser
        league_browser.close()

        print('closing the second browser')

        time.sleep(5)

        print('returning data from inner')

        # league_browser.switch_to.window(league_browser.window_handles[0])
    return data_dict


def main():
    browser = webdriver.Firefox()

    browser.get(url=f'{FLASHSCORE_URL}/{game}')

    browser.maximize_window()

    # previous_window = browser.window_handles[0]

    print('Primary browser title: ' + browser.title)

    time.sleep(5)

    _remove_consent_form(browser)

    # # Hide the consent banner
    # browser.execute_script(
    #     script="document.getElementById('onetrust-banner-sdk').style.display='none';")
    #
    # # Hide the placeholder box too - only interested in the first occurrence of the Placeholder class
    # browser.execute_script(
    #     script="document.getElementsByClassName('otPlaceHolder')[0].style.display='none';")

    left_menu_leagues_wrapper = browser.find_element_by_class_name(
        'menu.country-list.my-leagues.leftMenu.myTeamsWrapper')

    my_leagues_node = browser.find_element_by_id('my-leagues-list')
    my_leagues_list = my_leagues_node.find_elements_by_class_name('leftMenu__item')

    # Container of the leagues present to get data for
    for league in my_leagues_list:

        # ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, TimeoutException)
        # my_league_after_wait = WebDriverWait(browser, 5, ignored_exceptions=ignored_exceptions) \
        #     .until(expected_conditions.presence_of_element_located((By.ID, league)))

        league_h_ref = league.find_element_by_class_name('leftMenu__href')
        league_h_ref_attr = league_h_ref.get_attribute('href')

        league_title = league.get_attribute('title')
        print(f'Now checking {league_title}')

        # if we have not gathered this league's data let's do so now
        # while league not in my_basketball_leagues and league_h_ref_attr != '':
        if league_title not in my_basketball_leagues and league_h_ref_attr != '':
            print(f'Now getting {league_title} data.')
            # league_h_ref.click()
            # time.sleep(5)
            all_leagues_data[f'{league_title}'] = get_basketball_league_match_data(main_browser=browser, league_url=league_h_ref_attr)
            browser.switch_to.window(browser.window_handles[0])

            print(f'Got the {league_title} data')
            # Make sure the main browser is active
            browser.switch_to.window(browser.current_window_handle)

        continue

    # TODO test
    # TODO convert the dictionary to df and write to excel/database

    print("Done!")
    pass


# class BasketballScrapGameData:
# browser.find_elements()

# acb = browser.find_element_by_xpath(
#     xpath="//input[(@id='main') and (@class = 'menu country-list my-leagues leftMenu myTeamsWrapper')]")
#
# acb = browser.find_element_by_xpath(
#     '/html/body/div/')

# x = 2
# n = 5
# for i in range(0, n):

# try:
#     # pass pseudo element selector
#     browser.find_element_by_css_selector(
#         css_selector='.leftMenu__icon --star.leftMenu__item:nth-child(' + str(x) + ')').click()
#     # if the code finds the correct words we don't want to increment x
#     x += 0
#
# except NoSuchElementException:
#     try:
#         x = +1
#         browser.find_element_by_css_selector(
#             css_selector='.leftMenu__icon --star .leftMenu__item:nth-child(' + str(x) + ')').click()
#     except NoSuchElementException:
#         try:
#             x = +2
#             browser.find_element_by_css_selector(
#                 css_selector='.leftMenu__icon --star.leftMenu__item:nth-child(' + str(x) + ')').click()
#         except NoSuchElementException:
#             x = +3
#             browser.find_element_by_css_selector(
#                 css_selector='.leftMenu__icon --star.leftMenu__item:nth-child(' + str(x) + ')').click()

# time.sleep(5)
#
# window_after = browser.window_handles[1]
# browser.switch_to.window(window_name=window_after)
# print("Secondary browser title: " + browser.title)
#
# browser.close()
# browser.switch_to.window(window_name=previous_window)
#
# pass


if __name__ == '__main__':
    main()
