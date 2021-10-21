import time
from typing import Dict

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

FLASHSCORE_URL = 'https://www.flashscore.com'
game = 'basketball'


def remove_flashscore_consent_form(browser: webdriver):
    # Reject all cookies - click button
    browser.find_element_by_css_selector(
        css_selector='.ot-sdk-columns.has-reject-all-button.ot-sdk-two').click()

    pass


def unpack_nested_dict_to_df(nested_dict: Dict) -> pd.DataFrame:
    """
    TODO
    :return:
    """
    # this results in df having an index of type tuple with (league, home team - away team)
    df = pd.DataFrame.from_dict(
        {(first_level_key, second_level_key): nested_dict[first_level_key][second_level_key]
         for first_level_key in nested_dict.keys()
         for second_level_key in nested_dict[first_level_key].keys()},
        orient='index').reset_index()

    df.rename(columns={'level_0': 'League', 'level_1': 'Teams'}, inplace=True)
    df.set_index('Teams', inplace=True)

    return df


def get_flashscore_basket_data():
    """
    TODO
    :return:
    """

    # dictionary to hold all scraped data
    all_leagues_data = {}
    my_basketball_leagues = {}  # this is currently configurable in flashscores

    browser = webdriver.Firefox()

    browser.get(url=f'{FLASHSCORE_URL}/{game}')

    browser.maximize_window()

    print('Primary browser title: ' + browser.title)

    time.sleep(5)

    remove_flashscore_consent_form(browser)

    # # Hide the consent banner
    # browser.execute_script(
    #     script="document.getElementById('onetrust-banner-sdk').style.display='none';")
    #
    # # Hide the placeholder box too - only interested in the first occurrence of the Placeholder class
    # browser.execute_script(
    #     script="document.getElementsByClassName('otPlaceHolder')[0].style.display='none';")

    my_leagues_node = browser.find_element_by_id('my-leagues-list')
    my_leagues_list = my_leagues_node.find_elements_by_class_name('leftMenu__item')

    main_page = browser.window_handles[0]

    # Container of the leagues present to get data for
    for league in my_leagues_list:

        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        league_h_ref = WebDriverWait(league, 2, ignored_exceptions=ignored_exceptions) \
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'leftMenu__href')))

        # league_h_ref = league.find_element_by_class_name('leftMenu__href')
        league_h_ref_attr = league_h_ref.get_attribute('href')

        league_title = league.get_attribute('title')
        print(f'Now checking {league_title}')

        # if we have not gathered this league's data let's do so now
        if league_title not in my_basketball_leagues and league_h_ref_attr != '':
            print(f'Now getting {league_title} data.')

            all_leagues_data[f'{league_title}'] = get_basketball_league_match_data(main_browser=browser,
                                                                                   league_url=league_h_ref_attr)
            # When all data is gathered, close the previous tab and switch to main
            browser.close()
            browser.switch_to.window(main_page)

            print(f'Got the {league_title} data')

            time.sleep(3)

        continue

    leagues_df_data = unpack_nested_dict_to_df()

    return leagues_df_data


def get_basketball_league_match_data(main_browser: webdriver, league_url: str) -> Dict:
    """
    Given the h_ref of a basketball league go to the page and get all the match data and return them in
    :param league_url:
    :param main_browser:
    :return: TODO
    """

    data_dict = {}

    # Open a new tab
    main_browser.execute_script("window.open('');")
    time.sleep(1)
    main_browser.switch_to.window(main_browser.window_handles[1])
    time.sleep(1)
    main_browser.get(url=f'{league_url}')

    time.sleep(2)

    # _remove_consent_form(main_browser)

    # Go to the results tab
    main_browser.find_element_by_class_name('tabs__tab.results').click()

    time.sleep(2)

    all_matches = main_browser.find_elements_by_class_name(
        'event__match.event__match--static.event__match--twoLine')
    for match in all_matches:

        home_team = match.find_element_by_class_name('event__participant.event__participant--home').text
        away_team = match.find_element_by_class_name('event__participant.event__participant--away').text

        match_name = home_team + "-" + away_team

        # TODO replace with logger
        print(f'Getting {match_name} data')
        # start packing game data into dictionary
        data_dict[f'{match_name}'] = {}

        data_dict[f'{match_name}']['match_datetime'] = match.find_element_by_class_name('event__time').text

        data_dict[f'{match_name}']['home_team'] = home_team
        data_dict[f'{match_name}']['away_team'] = away_team

        data_dict[f'{match_name}']['home_total'] = \
            int(match.find_element_by_class_name('event__score.event__score--home').text)

        data_dict[f'{match_name}']['away_total'] = \
            int(match.find_element_by_class_name('event__score.event__score--away').text)

        # now get the quarters' data
        for quarter in range(1, 5):
            data_dict[f'{match_name}'][f'home_q{quarter}'] = \
                int(match.find_element_by_class_name(f'event__part.event__part--home.event__part--{quarter}').text)

            data_dict[f'{match_name}'][f'away_q{quarter}'] = \
                int(match.find_element_by_class_name(f'event__part.event__part--away.event__part--{quarter}').text)

        time.sleep(2)

        print('returning data from inner')

    return data_dict
