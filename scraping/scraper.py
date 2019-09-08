# Project: NBA Correlations App
# Description: Scrape historical team statistics to power Shiny App
# Data Sources: Basketball-Reference
# Last Updated: 7/9/2019


import numpy as np
import pandas as pd
import requests
from time import sleep
from bs4 import BeautifulSoup as BS

def scrape_per_100_possessions(save=False):
    """
    Scrape Per 100 Possession table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.

    Returns:
        historical_per_100_possessions_df (DataFrame): Per 100 Possession table
        between 2004-2005 and 2018-2019 NBA seasons.
    """
    historical_per_100_possessions_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        season_per_100_df = pd.DataFrame()
        url = 'https://www.basketball-reference.com/leagues/NBA_{}.html#team-stats-per_poss::none'.format(season)
        html = requests.get(url).text
        soup = BS(html, 'html.parser')
        placeholders = soup.find_all('div', {'class': 'placeholder'})
        for x in placeholders:
            comment = ''.join(x.next_siblings)
            soup_comment = BS(comment, 'html.parser')
            tables = soup_comment.find_all('table', attrs={"id":"team-stats-per_poss"})
            for tag in tables:
                df = pd.read_html(tag.prettify())[0]
                season_per_100_df = season_per_100_df.append(df).reset_index()
                season_per_100_df.drop('index', axis=1, inplace=True)
                season_per_100_df.columns = ['RANK', 'TEAM', 'G', 'MP'] + \
                                            ['PER100_' + str(col) for col in \
                                            season_per_100_df.columns if col not in \
                                            ['Rk', 'Team', 'G', 'MP']]
        season_per_100_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        season_per_100_df['PLAYOFF_TEAM'] = np.where(season_per_100_df['TEAM'].str.find('*') > -1, 1, 0)
        season_per_100_df['TEAM'] = season_per_100_df['TEAM'].str.strip(' * ')
        historical_per_100_possessions_df = historical_per_100_possessions_df.append(season_per_100_df, sort=False)
    column_order = ['RANK', 'SEASON', 'TEAM', 'PLAYOFF_TEAM', 'G', 'MP', 'PER100_FG',
                    'PER100_FGA', 'PER100_FG%', 'PER100_3P', 'PER100_3PA',
                    'PER100_3P%', 'PER100_2P', 'PER100_2PA', 'PER100_2P%',
                    'PER100_FT', 'PER100_FTA', 'PER100_FT%', 'PER100_ORB',
                    'PER100_DRB', 'PER100_TRB', 'PER100_AST', 'PER100_STL',
                    'PER100_BLK', 'PER100_TOV', 'PER100_PF', 'PER100_PTS']
    historical_per_100_possessions_df = historical_per_100_possessions_df.reindex(columns=column_order)
    if save:
        parent_directory = '../app/data/'
        historical_per_100_possessions_df.to_csv(parent_directory +
                                                'Per_100_Poss.csv',
                                                index=False)
    else:
        pass
    return historical_per_100_possessions_df

def scrape_opponent_per_100_possessions(save=False):
    """
    Scrape Opponent Per 100 Possession table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.

    Returns:
        historical_opponent_per_100_df (DataFrame): Opponent Per 100 Possession
        table between 2004-2005 and 2018-2019 NBA seasons.
    """
    historical_opponent_per_100_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        season_opponent_per_100_df = pd.DataFrame()
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}.html#opponent-stats-per_poss::none'.format(season)
        html = requests.get(url).text
        soup = BS(html, 'html.parser')
        placeholders = soup.find_all('div', {'class': 'placeholder'})
        for x in placeholders:
            comment = ''.join(x.next_siblings)
            soup_comment = BS(comment, 'html.parser')
            tables = soup_comment.find_all('table', attrs={"id":"opponent-stats-per_poss"})
            for tag in tables:
                df = pd.read_html(tag.prettify())[0]
                season_opponent_per_100_df = season_opponent_per_100_df.append(df).reset_index()
                season_opponent_per_100_df.drop('index', axis=1, inplace=True)
                season_opponent_per_100_df.columns = ['RANK', 'TEAM', 'G', 'MP'] + \
                                                    ['OPP_PER100_' + str(col) for \
                                                    col in season_opponent_per_100_df.columns \
                                                    if col not in ['Rk', 'Team', 'G', 'MP']]
        season_opponent_per_100_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        season_opponent_per_100_df['PLAYOFF_TEAM'] = np.where(season_opponent_per_100_df['TEAM'].str.find('*') > -1, 1, 0)
        season_opponent_per_100_df['TEAM'] = season_opponent_per_100_df['TEAM'].str.strip(' * ')
        historical_opponent_per_100_df = historical_opponent_per_100_df.append(season_opponent_per_100_df, sort=False)
    column_order = ['RANK', 'SEASON', 'TEAM', 'PLAYOFF_TEAM', 'G', 'MP',
                    'OPP_PER100_FG', 'OPP_PER100_FGA', 'OPP_PER100_FG%',
                    'OPP_PER100_3P', 'OPP_PER100_3PA', 'OPP_PER100_3P%',
                    'OPP_PER100_2P', 'OPP_PER100_2PA', 'OPP_PER100_2P%',
                    'OPP_PER100_FT', 'OPP_PER100_FTA', 'OPP_PER100_FT%',
                    'OPP_PER100_ORB', 'OPP_PER100_DRB', 'OPP_PER100_TRB',
                    'OPP_PER100_AST', 'OPP_PER100_STL', 'OPP_PER100_BLK',
                    'OPP_PER100_TOV', 'OPP_PER100_PF', 'OPP_PER100_PTS']
    historical_opponent_per_100_df = historical_opponent_per_100_df.reindex(columns=column_order)
    if save:
        parent_directory = '../app/data/'
        historical_opponent_per_100_df.to_csv(parent_directory +
                                            'Opponent_Per_100_Poss.csv',
                                            index=False)
    else:
        pass
    return historical_opponent_per_100_df

def scrape_team_shooting(save=False):
    """
    Scrape Team Shooting table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.

    Returns:
        historical_team_shooting_df (DataFrame): Team Shooting table between
        2004-2005 and 2018-2019 NBA seasons.
        league_average_team_shooting_df (DataFrame): League Average Team Shooting
        between 2004-2005 and 2018-2019 seasons.
    """
    historical_team_shooting_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        season_team_shooting_df = pd.DataFrame()
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}.html#team_shooting::none'.format(season)
        html = requests.get(url).text
        soup = BS(html, 'html.parser')
        placeholders = soup.find_all('div', {'class': 'placeholder'})
        for x in placeholders:
            comment = ''.join(x.next_siblings)
            soup_comment = BS(comment, 'html.parser')
            tables = soup_comment.find_all('table', attrs={"id":"team_shooting"})
            for tag in tables:
                df = pd.read_html(tag.prettify())[0]
                season_team_shooting_df = season_team_shooting_df.append(df).reset_index()
                season_team_shooting_df.columns = season_team_shooting_df.columns.get_level_values(1)
                season_team_shooting_df.drop('', axis=1, inplace=True)
                season_team_shooting_df.columns = ['RANK', 'TEAM', 'G', 'MP',
                                                   'FG%', 'AVERAGE_DISTANCE',
                                                   '%FGA_2P', '%FGA_0-3',
                                                   '%FGA_3-10', '%FGA_10-16',
                                                   'FGA_16-3PT', '%FGA_3P',
                                                   'FG%_2P', 'FG%_0-3', 'FG%_3-10',
                                                   'FG%_10-16', 'FG%_16-3PT',
                                                   'FG%_3P', '%ASTD_2P', '%FGA_DUNKS',
                                                   'DUNKS_MADE', '%FGA_LAYUPS',
                                                   'LAYUPS_MADE', '%ASTD_3P',
                                                   '%FGA3P_CORNER', 'FG%3_CORNER',
                                                   'HEAVE_ATTEMPTS', 'HEAVE_MAKES']
        season_team_shooting_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        season_team_shooting_df['PLAYOFF_TEAM'] = np.where(season_team_shooting_df['TEAM'].str.find('*') > -1, 1, 0)
        season_team_shooting_df['TEAM'] = season_team_shooting_df['TEAM'].str.strip(' * ')
        season_team_shooting_df = season_team_shooting_df[season_team_shooting_df['TEAM']!='League Average']
        historical_team_shooting_df = historical_team_shooting_df.append(season_team_shooting_df, sort=False)
    column_order = ['RANK', 'SEASON', 'TEAM', 'PLAYOFF_TEAM', 'G', 'MP', 'FG%',
                    'AVERAGE_DISTANCE', '%FGA_2P', '%FGA_0-3', '%FGA_3-10',
                    '%FGA_10-16', 'FGA_16-3PT', '%FGA_3P', 'FG%_2P', 'FG%_0-3',
                    'FG%_3-10', 'FG%_10-16', 'FG%_16-3PT', 'FG%_3P',
                    '%ASTD_2P', '%FGA_DUNKS', 'DUNKS_MADE', '%FGA_LAYUPS',
                    'LAYUPS_MADE', '%ASTD_3P', '%FGA3P_CORNER', 'FG%3_CORNER',
                    'HEAVE_ATTEMPTS', 'HEAVE_MAKES']
    historical_team_shooting_df = historical_team_shooting_df.reindex(columns=column_order)
    if save:
        parent_directory = '../app/data/'
        historical_team_shooting_df.to_csv(parent_directory +
                                          'Team_Shooting.csv',
                                          index=False)
    else:
        pass
    return historical_team_shooting_df

def scrape_opponent_shooting(save=False):
    """
    Scrape Opponent Team Shooting table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.

    Returns:
        historical_opponent_shooting_df (DataFrame): Opponent Team Shooting
        table between 2004-2005 and 2018-2019 NBA seasons.
    """
    historical_opponent_shooting_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        season_opponent_shooting_df = pd.DataFrame()
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}.html#opponent_shooting::none'.format(season)
        html = requests.get(url).text
        soup = BS(html, 'html.parser')
        placeholders = soup.find_all('div', {'class': 'placeholder'})
        for x in placeholders:
            comment = ''.join(x.next_siblings)
            soup_comment = BS(comment, 'html.parser')
            tables = soup_comment.find_all('table', attrs={"id":"opponent_shooting"})
            for tag in tables:
                df = pd.read_html(tag.prettify())[0]
                season_opponent_shooting_df = season_opponent_shooting_df.append(df).reset_index()
                season_opponent_shooting_df.columns = season_opponent_shooting_df.columns.get_level_values(1)
                season_opponent_shooting_df.drop('', axis=1, inplace=True)
                season_opponent_shooting_df.columns = ['RANK', 'TEAM', 'G', 'MP',
                                                       'OPP_FG%', 'OPP_AVERAGE_DISTANCE',
                                                       'OPP_%FGA_2P', 'OPP_%FGA_0-3',
                                                       'OPP_%FGA_3-10', 'OPP_%FGA_10-16',
                                                       'OPP_FGA_16-3PT', 'OPP_%FGA_3P',
                                                       'OPP_FG%_2P', 'OPP_FG%_0-3',
                                                       'OPP_FG%_3-10', 'OPP_FG%_10-16',
                                                       'OPP_FG%_16-3PT', 'OPP_FG%_3P',
                                                       'OPP_%ASTD_2P', 'OPP_%FGA_DUNKS',
                                                       'OPP_DUNKS_MADE', 'OPP_%FGA_LAYUPS',
                                                       'OPP_LAYUPS_MADE', 'OPP_%ASTD_3P',
                                                       'OPP_%FGA3P_CORNER', 'OPP_FG%3_CORNER']
        season_opponent_shooting_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        season_opponent_shooting_df['PLAYOFF_TEAM'] = np.where(season_opponent_shooting_df['TEAM'].str.find('*') > -1, 1, 0)
        season_opponent_shooting_df['TEAM'] = season_opponent_shooting_df['TEAM'].str.strip(' * ')
        season_opponent_shooting_df = season_opponent_shooting_df[season_opponent_shooting_df['TEAM']!='League Average']
        historical_opponent_shooting_df = historical_opponent_shooting_df.append(season_opponent_shooting_df, sort=False)
    column_order = ['RANK', 'SEASON', 'TEAM', 'PLAYOFF_TEAM', 'G', 'MP', 'OPP_FG%',
                    'OPP_AVERAGE_DISTANCE', 'OPP_%FGA_2P', 'OPP_%FGA_0-3',
                    'OPP_%FGA_3-10', 'OPP_%FGA_10-16', 'OPP_FGA_16-3PT',
                    'OPP_%FGA_3P', 'OPP_FG%_2P', 'OPP_FG%_0-3', 'OPP_FG%_3-10',
                    'OPP_FG%_10-16', 'OPP_FG%_16-3PT', 'OPP_FG%_3P',
                    'OPP_%ASTD_2P', 'OPP_%FGA_DUNKS', 'OPP_DUNKS_MADE',
                    'OPP_%FGA_LAYUPS', 'OPP_LAYUPS_MADE', 'OPP_%ASTD_3P',
                    'OPP_%FGA3P_CORNER', 'OPP_FG%3_CORNER']
    historical_opponent_shooting_df = historical_opponent_shooting_df.reindex(columns=column_order)
    if save:
        parent_directory = '../app/data/'
        historical_opponent_shooting_df.to_csv(parent_directory +
                                              'Opponent_Shooting.csv',
                                              index=False)
    else:
        pass
    return historical_opponent_shooting_df

def scrape_miscellaneous_stats(save=False):
    """
    Scrape Miscellaneous Stats table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.

    Returns:
        historical_misc_stats_df (DataFrame): Miscellaneous Stats table between
        2004-2005 and 2018-2019 NBA seasons.
        league_average_misc_stats_df  (DataFrame): League Average Miscellaneous
        Stats between 2004-2005 and 2018-2019 season.
    """
    historical_misc_stats_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        season_misc_stats_df = pd.DataFrame()
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}.html#misc_stats::none'.format(season)
        html = requests.get(url).text
        soup = BS(html, 'html.parser')
        placeholders = soup.find_all('div', {'class': 'placeholder'})
        for x in placeholders:
            comment = ''.join(x.next_siblings)
            soup_comment = BS(comment, 'html.parser')
            tables = soup_comment.find_all('table', attrs={"id":"misc_stats"})
            for tag in tables:
                df = pd.read_html(tag.prettify())[0]
                season_misc_stats_df = season_misc_stats_df.append(df).reset_index()
                season_misc_stats_df.columns = season_misc_stats_df.columns.get_level_values(1)
                season_misc_stats_df.drop('', axis=1, inplace=True)
                season_misc_stats_df.columns = ['RANK', 'TEAM', 'AVERAGE_AGE',
                                                'W', 'L', 'PW', 'PL', 'MOV',
                                                'SOS', 'SRS', 'ORTG', 'DRTG',
                                                'NRTG', 'PACE', 'FT_RATE',
                                                '3PA_RATE', 'TS%', 'OFFENSIVE_EFG%',
                                                'OFFENSIVE_TOV%', 'OFFENSIVE_ORB%',
                                                'OFFENSIVE_FT/FGA', 'DEFENSIVE_eFG%',
                                                'DEFENSIVE_TOV%', 'DEFENSIVE_DRB%',
                                                'DEFENSIVE_FT/FGA', 'ARENA',
                                                'TOTAL_ATTENDANCE', 'ATTENDANCE/G']
        season_misc_stats_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        season_misc_stats_df['PLAYOFF_TEAM'] = np.where(season_misc_stats_df['TEAM'].str.find('*') > -1, 1, 0)
        season_misc_stats_df['TEAM'] = season_misc_stats_df['TEAM'].str.strip(' * ')
        season_misc_stats_df['W/L%'] = season_misc_stats_df['W']/(season_misc_stats_df['W'] + season_misc_stats_df['L'])
        season_misc_stats_df = season_misc_stats_df[season_misc_stats_df['TEAM']!='League Average']
        historical_misc_stats_df = historical_misc_stats_df.append(season_misc_stats_df, sort=False)
    column_order = ['RANK', 'SEASON', 'TEAM', 'PLAYOFF_TEAM', 'AVERAGE_AGE',
                    'W', 'L', 'W/L%', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORTG',
                    'DRTG', 'NRTG', 'PACE', 'FT_RATE', '3PA_RATE', 'TS%',
                    'OFFENSIVE_EFG%', 'OFFENSIVE_TOV%', 'OFFENSIVE_ORB%',
                    'OFFENSIVE_FT/FGA', 'DEFENSIVE_eFG%', 'DEFENSIVE_TOV%',
                    'DEFENSIVE_DRB%', 'DEFENSIVE_FT/FGA', 'ARENA',
                    'TOTAL_ATTENDANCE', 'ATTENDANCE/G']
    historical_misc_stats_df = historical_misc_stats_df.reindex(columns=column_order)
    if save:
        parent_directory = '../app/data/'
        historical_misc_stats_df.to_csv(parent_directory +
                                        'Miscellaneous_Stats.csv',
                                        index=False)
    else:
        pass
    return historical_misc_stats_df

def scrape_team_ratings(save=False):
    """
    Scrape Team Ratings table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.

    Returns:
        historical_team_ratings_df (DataFrame): Team Ratings table between
        2004-2005 and 2018-2019 NBA seasons.
    """
    historical_team_ratings_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}_ratings.html#ratings::14'.format(season)
        season_team_ratings_df = pd.read_html(url)[0]
        season_team_ratings_df.columns = season_team_ratings_df.columns.get_level_values(1)
        season_team_ratings_df.columns = ['RANK', 'TEAM', 'CONFERENCE', 'DIVISION',
                                          'W', 'L', 'W/L%', 'MOV', 'ORTG', 'DRTG',
                                          'NRTG', 'ADJUSTED_MOV', 'ADJUSTED_ORTG',
                                          'ADJUSTED_DRTG', 'ADJUSTED_NRTG']
        season_team_ratings_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        historical_team_ratings_df = historical_team_ratings_df.append(season_team_ratings_df, sort=False)
    column_order = ['RANK', 'TEAM', 'SEASON', 'CONFERENCE', 'DIVISION', 'W', 'L',
                    'W/L%', 'MOV', 'ORTG', 'DRTG', 'NRTG', 'ADJUSTED_MOV',
                    'ADJUSTED_ORTG', 'ADJUSTED_DRTG', 'ADJUSTED_NRTG']
    historical_team_ratings_df = historical_team_ratings_df.reindex(columns=column_order)
    if save:
        parent_directory = '../app/data/'
        historical_team_ratings_df.to_csv(parent_directory +
                                              'Team_Ratings.csv',
                                              index=False)

    else:
        pass
    return historical_team_ratings_df

def create_team_base_table(save=False):
    """
    Combine Team Ratings, Miscellaneous Stats, Per 100 Possessions,
    Opponnent Per 100 Possessions, Team Shooting, and Opponent Shooting
    DataFrames to create comprehensive base table for team stats.

    Args:
        None

    Returns:
        team_stats_df (DataFrame): Team statistics for seasons between
        2004-2005 and 2018-2019 seasons
    """
    parent_directory = '../app/data/'

    team_ratings_df = pd.read_csv(parent_directory + 'Team_Ratings.csv')
    misc_stats_df = pd.read_csv(parent_directory + 'Miscellaneous_Stats.csv')
    per_100_possessions_df = pd.read_csv(parent_directory + 'Per_100_Poss.csv')
    opponent_per_100_possessions_df = pd.read_csv(parent_directory + 'Opponent_Per_100_Poss.csv')
    team_shooting_df = pd.read_csv(parent_directory + 'Team_Shooting.csv')
    opponent_shooting_df = pd.read_csv(parent_directory + 'Opponent_Shooting.csv')

    team_stats_df = team_ratings_df.merge(misc_stats_df,
                                    on=['TEAM', 'SEASON'],
                                    how='left',
                                    suffixes=('', '_duplicate'))
    team_stats_df.drop([col for col in team_stats_df.columns if '_duplicate' in col],
                        axis=1,
                        inplace=True)
    team_stats_df = team_stats_df.merge(per_100_possessions_df,
                                    on=['TEAM', 'SEASON'],
                                    how='left',
                                    suffixes=('', '_duplicate'))
    team_stats_df.drop([col for col in team_stats_df.columns if '_duplicate' in col],
                        axis=1,
                        inplace=True)
    team_stats_df = team_stats_df.merge(opponent_per_100_possessions_df,
                                    on=['TEAM', 'SEASON'],
                                    how='left',
                                    suffixes=('', '_duplicate'))
    team_stats_df.drop([col for col in team_stats_df.columns if '_duplicate' in col],
                        axis=1,
                        inplace=True)
    team_stats_df = team_stats_df.merge(team_shooting_df,
                                    on=['TEAM', 'SEASON'],
                                    how='left',
                                    suffixes=('', '_duplicate'))
    team_stats_df.drop([col for col in team_stats_df.columns if '_duplicate' in col],
                        axis=1,
                        inplace=True)
    team_stats_df = team_stats_df.merge(opponent_shooting_df,
                                    on=['TEAM', 'SEASON'],
                                    how='left',
                                    suffixes=('', '_duplicate'))
    team_stats_df.drop([col for col in team_stats_df.columns if '_duplicate' in col],
                        axis=1,
                        inplace=True)

    if save:
        parent_directory = '../app/data/'
        team_stats_df.to_csv(parent_directory +
                              'Team_Stats.csv',
                              index=False)
    else:
        pass
    return team_stats_df

if __name__=='__main__':
    # Scrape Basketball-Reference Tables
    scrape_per_100_possessions(save=True)
    scrape_opponent_per_100_possessions(save=True)
    scrape_team_shooting(save=True)
    scrape_opponent_shooting(save=True)
    scrape_miscellaneous_stats(save=True)
    scrape_team_ratings(save=True)

    # Join dataframes
    create_team_base_table(save=True)
