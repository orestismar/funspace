# -*- coding: utf-8 -*-
"""
Functionality to scrape basketball data from the web.

:Author: Orestis Maroulis
:Created: 15/10/2021
:Copyright: 2021, Orestis Maroulis, All rights reserved.
"""

import os
import time
from typing import Dict, List, Optional, Tuple

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from betting.websites import SportsDataSites
from directories import PYTHON_FUNPLACE, _C_DIR
from logs import get_stream_and_file_logger

logger = get_stream_and_file_logger(name=__name__)

FLASHSCORE_URL = SportsDataSites.flashscore_main.value
game = 'basketball'


def get_credentials(website: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Reads C:\\credentials.txt and extracts the username and pssword.
    The txt file's format is "website usrname pssword"

    :param website: the main/landing url of the website we want to scrape
    :return:
    """
    username, password = None, None

    filepath = os.path.join(_C_DIR, 'credentials.txt')
    with open(filepath) as file:
        lines = file.readlines()
        lines = [line.split() for line in lines]

    for credentials in lines:
        if credentials[0] == website:
            username = credentials[1]
            password = credentials[2]

            break

    return username, password


# TODO more stuff
#  1. top 3 player stats
#  2. get player statistics overall
#  3. point-by-point match history
#  4. standings overall, home, away
#  5. H2H

# TODO - how to store this data?


def login_to_flashscore(browser: webdriver):
    try:

        # get credentials from file
        email, password = get_credentials(FLASHSCORE_URL)

        browser.find_element_by_id('signIn').click()
        login_details_window = browser.window_handles[-1]

        browser.switch_to.window(login_details_window)

        browser.find_element_by_id('email').send_keys(email)
        browser.find_element_by_id('passwd').send_keys(password)

        time.sleep(3)
        # submit the form / click
        browser.find_element_by_id('login').click()

        time.sleep(5)

        # TODO  Now there is one important thing  that is missing here.How do we  know if we are logged in? try a couple
        #  of things:
        #  - Check for an error message (like “Wrong password”)
        #  - Check for one element on the page that is only displayed once logged in. So, we're going to check for the
        #  logout button. The logout button has the ID “logout”

    except Exception:  # TODO do this properly
        raise Exception

    pass


def remove_flashscore_consent_form(browser: webdriver):
    # Reject all cookies - click button
    browser.find_element_by_css_selector(
        css_selector='.ot-sdk-columns.has-reject-all-button.ot-sdk-two').click()

    pass


def unpack_nested_dict_to_df(nested_dict: Dict) -> pd.DataFrame:
    """
    Currently used in FlashScore scrapping.
    Unpacks nested dictionaries (3 levels+) to a single dataframe using the first two
    level dict keys for the frame's index.
    :return: dataframe with nested dict keys as columns
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


def get_flashscore_basket_data(league_list: List[str]) -> (pd.DataFrame, pd.DataFrame):
    """
    Gets the specified leagues data from flashscore.com/basketball#.

    :param league_list: the leagues whose data we want scraped.
    :return: tuple of two dataframes, first one with the match data, second with the missing match data
    """

    # dictionary to hold all scraped data
    all_leagues_data = {}
    my_basketball_leagues = []  # this is currently configurable in flashscores
    missing_games = {}

    browser = webdriver.Firefox()

    browser.get(url=f'{FLASHSCORE_URL}/{game}')

    browser.maximize_window()

    logger.info(f'Primary browser title: {browser.title}')

    time.sleep(5)

    remove_flashscore_consent_form(browser)

    main_page = browser.window_handles[0]

    # login to flashscore to get my leagues and other user config
    login_to_flashscore(browser=browser)

    browser.switch_to.window(main_page)

    # # Hide the consent banner
    # browser.execute_script(
    #     script="document.getElementById('onetrust-banner-sdk').style.display='none';")
    #
    # # Hide the placeholder box too - only interested in the first occurrence of the Placeholder class
    # browser.execute_script(
    #     script="document.getElementsByClassName('otPlaceHolder')[0].style.display='none';")

    my_leagues_node = browser.find_element_by_id('my-leagues-list')
    my_leagues_list = my_leagues_node.find_elements_by_class_name('leftMenu__item')

    # Loop over all the leagues and store their h refs
    leagues_refs = {}
    # Container of the leagues present to get data for
    for league in my_leagues_list:
        time.sleep(3)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        league_h_ref = WebDriverWait(league, 2, ignored_exceptions=ignored_exceptions) \
            .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'leftMenu__href')))

        # league_h_ref = league.find_element_by_class_name('leftMenu__href')
        league_h_ref_attr = league_h_ref.get_attribute('href')

        league_title = league.get_attribute('title')

        if league_h_ref_attr != '':
            leagues_refs[f'{league_title}'] = league_h_ref_attr

    # Now get each league's data
    for league_title, league_h_ref in leagues_refs.items():
        # only get data if the league is in the ask list
        if league_title in league_list:
            logger.info(f'Now checking {league_title}')

            # if we have not gathered this league's data let's do so now
            if league_title not in my_basketball_leagues:
                logger.info(f'Now getting {league_title} data.')

                all_leagues_data[f'{league_title}'], missing_league_games = get_flashscore_basketball_league_data(
                    main_browser=browser,
                    league_url=league_h_ref)

                missing_games[f'{league_title}'] = missing_league_games
                # When all data is gathered, close the previous tab and switch to main
                browser.close()
                browser.switch_to.window(main_page)

                my_basketball_leagues.append(league_title)
                logger.info(f'Got the {league_title} data')

                # After we've got all the league matches, cache yesterday's date as last date
                # I choose yesterday's date because at the time of
                _cache_last_date(
                    league_date_tuple=(f'Flashscore, {league_title}', pd.Timestamp.today() - pd.Timedelta('1d')))

                time.sleep(3)

            continue

    # Done gathering data, close the browser
    browser.close()

    leagues_df_data = unpack_nested_dict_to_df(nested_dict=all_leagues_data)
    all_leagues_missing_games = pd.Series(missing_games)

    return leagues_df_data, all_leagues_missing_games


def get_flashscore_basketball_league_data(main_browser: webdriver, league_url: str) -> Dict:
    """
    Given the h_ref of a basketball league go to the page and get all the match data and return them in
    :param league_url: the url of the basketball league whose data we want to download
    :param main_browser: the webdriver instance used in the calling process
    :return:
    """

    data_dict = {}
    missing_games = []

    # Open a new tab
    main_browser.execute_script("window.open('');")
    time.sleep(1)

    league_window = main_browser.window_handles[1]

    main_browser.switch_to.window(league_window)
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

        logger.info(f'Getting {match_name} data')

        # Open new window for the specific game
        match.click()
        match_window = main_browser.window_handles[-1]

        try:
            main_browser.switch_to_window(match_window)
            main_browser.maximize_window()

            data_dict[f'{match_name}']: Dict = \
                get_flashscore_basketball_match_data(main_browser=main_browser)
        except NoSuchElementException:
            logger.warning(f'Could not get data for {match_name} - please investigate')
            missing_games.append(match_name)

        main_browser.close()
        main_browser.switch_to.window(league_window)

    # TODO covert the missing games to a dataframe before returning
    return data_dict, missing_games


def get_flashscore_basketball_match_data(main_browser: webdriver) -> Dict:
    """
    Opens the specific match page and extracts all relevant information from there to store in a dict.
    :param main_browser: the webdriver instance of the caller process
    :return: a dictionary with the collected match data
    """

    # Construct new dict to store and return data and get the match datetime
    game_dict = {'Datetime': main_browser.find_element_by_class_name('duelParticipant__startTime').text}

    # Get the total and quarters data

    for side in ['home', 'away']:

        time.sleep(4)
        game_dict[f'{side} total'] = int(
            main_browser.find_element_by_class_name(f'smh__part.smh__score.smh__{side}.smh__part--current').text)

        for quarter in range(1, 6):
            if main_browser.find_element_by_class_name(f'smh__part.smh__{side}.smh__part--{quarter}').text:
                game_dict[f'{side} Q{quarter}'] = int(
                    main_browser.find_element_by_class_name(f'smh__part.smh__{side}.smh__part--{quarter}').text)

    # click the statistics tab
    # < a class ="tabs__tab" href="#match-summary/match-statistics" > Statistics < / a >
    statistics_href = '#match-summary/match-statistics'
    # Find the Statistics tab
    main_browser.find_element_by_xpath(f'//a[@href="{statistics_href}"]').click()

    # all the stats are under the statRow class
    stat_categories = main_browser.find_elements_by_class_name('statRow')
    for category in stat_categories:
        category_name = category.find_element_by_class_name('statCategoryName').text
        game_dict[f'home {category_name}'] = category.find_element_by_class_name('statHomeValue').text
        game_dict[f'away {category_name}'] = category.find_element_by_class_name('statAwayValue').text

        time.sleep(2)

    # click the player statistics tab
    # < a class ="tabs__tab selected" href="#match-summary/player-statistics" aria-current="page" >
    # Player Statistics < / a >
    player_stats_href = '#match-summary/player-statistics'
    main_browser.find_element_by_xpath(f'//a[@href="{player_stats_href}"]').click()

    # get the player stats

    logger.info('Returning data from inner')

    return game_dict


def _cache_last_date(league_date_tuple: tuple) -> None:
    """
    Check the file in which we cache the last dates per league exists.
    If not, create one and write and save the date. If it already exists, just update it with the next.
    If the entry exists, overwrite it otherwise create a new one.
    """

    cache_filepath = os.path.join(PYTHON_FUNPLACE, 'betting',
                                  'basketball', 'data', 'last_match_dates.txt')
    if not os.path.isfile(cache_filepath):
        # if file does not exist, create it
        file = open(cache_filepath, 'x')
        file.write(f'{league_date_tuple[0]}:{league_date_tuple[1]}\n')
        file.close()
        logger.info('Create cache file with new values')

    else:
        file = open(cache_filepath, 'a')
        file.write(f'{league_date_tuple[0]}:{league_date_tuple[1]}\n')
        file.close()
        logger.info('Updated cache file with new values')

    pass


def find_and_get_missing_match_data():
    # TODO we need a way to gauge whether for each round we've got the complete list of games. If not, we should
    #  somehow make sure to log this, infer the missing ones and find an efficient way to get this data at a later stage

    pass
