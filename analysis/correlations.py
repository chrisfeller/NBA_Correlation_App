# Project: NBA Correlations App
# Description: Calculate correlations between statistics historically
# Data Sources: Basketball-Reference
# Last Updated: 9/10/2019

import pandas as pd


def season_lags(save=False):
    df = pd.read_csv('../app/data/Team_Stats.csv')
    shifted = df.groupby(['TEAM']).shift(-1)
    season_lag_df = df.join(shifted.rename(columns=lambda x: x+"_lag"))
    season_lag_df.dropna(inplace=True)
    if save:
        season_lag_df.to_csv('../app/data/Basketball_Reference_Season_Lags.csv',
                                    index=False)
    return season_lag_df

def calculate_correlations(save=False):
    # Read in Basketball-Reference tables
    bbref_team_data = pd.read_csv('../app/data/Team_Stats.csv')

    # Calculate pearson correlation
    pearson_corr = (bbref_team_data.corr(method='pearson')
                                   .reset_index())
    pearson_corr.rename(columns={pearson_corr.columns[0]: "STATISTIC" },
                        inplace=True)

    # Calculate spearman correlation
    spearman_corr = (bbref_team_data.corr(method='spearman')
                                    .reset_index())
    spearman_corr.rename(columns={spearman_corr.columns[0]: "STATISTIC" },
                        inplace=True)

    if save:
        pearson_corr.to_csv('../app/data/pearson_correlation.csv',
                            index=False)
        spearman_corr.to_csv('../app/data/spearman_correlation.csv',
                            index=False)
    return pearson_corr, spearman_corr

def season_correlations(save=False):
    # Read in Basketball-Reference tables
    bbref_team_data = pd.read_csv('../app/data/Team_Stats.csv')

    # Basketball-Reference Correlations by Season
    bbref_correlation_season_df = pd.DataFrame()
    # Loop through each season in basketball-reference tables replicating the same process as above
    for season in bbref_team_data['SEASON'].unique():
        pearson_corr_df = bbref_team_data[bbref_team_data['SEASON']==season].corr(method='pearson')
        pearson_corr_df = pearson_corr_df['NRTG'].reset_index()
        pearson_corr_df.columns = ['STATISTIC', 'PEARSON_CORRELATION']
        pearson_corr_df['PEARSON_CORRELATION_ABS'] = abs(pearson_corr_df['PEARSON_CORRELATION'])

        spearman_corr_df = bbref_team_data[bbref_team_data['SEASON']==season].corr(method='spearman')
        spearman_corr_df = spearman_corr_df['NRTG'].reset_index()
        spearman_corr_df.columns = ['STATISTIC', 'SPEARMAN_CORRELATION']
        spearman_corr_df['SPEARMAN_CORRELATION_ABS'] = abs(spearman_corr_df['SPEARMAN_CORRELATION'])

        correlation_df = pearson_corr_df.merge(spearman_corr_df, on=['STATISTIC'])
        correlation_df['SEASON'] = season
        correlation_df = correlation_df[~correlation_df['STATISTIC'].isin(['RANK'])]
        correlation_df.sort_values(by='PEARSON_CORRELATION_ABS', ascending=False, inplace=True)
        correlation_df['PEARSON_CORRELATION_RANK'] = range(1, 1+len(correlation_df))
        correlation_df.sort_values(by='SPEARMAN_CORRELATION_ABS', ascending=False, inplace=True)
        correlation_df['SPEARMAN_CORRELATION_RANK'] = range(1, 1+len(correlation_df))

        correlation_df['AVERAGE_RANK'] = (correlation_df[['PEARSON_CORRELATION_RANK',
                                                          'SPEARMAN_CORRELATION_RANK']]
                                                .mean(axis=1)
                                                .round(3))
        correlation_df.sort_values(by='AVERAGE_RANK', inplace=True)
        correlation_df = correlation_df[['SEASON', 'STATISTIC', 'PEARSON_CORRELATION',
                                        'PEARSON_CORRELATION_ABS', 'SPEARMAN_CORRELATION',
                                        'SPEARMAN_CORRELATION_ABS', 'PEARSON_CORRELATION_RANK',
                                        'SPEARMAN_CORRELATION_RANK', 'AVERAGE_RANK']]

        bbref_correlation_season_df = bbref_correlation_season_df.append(correlation_df, sort=False)
    bbref_correlation_season_df = bbref_correlation_season_df.sort_values(by=['SEASON', 'AVERAGE_RANK'], ascending=[False, True])\
                                                             .dropna()
    if save:
        bbref_correlation_season_df.to_csv('../app/data/Basketball_Reference_Season_Correlations.csv',
                                    index=False)
    return bbref_correlation_season_df


if __name__=='__main__':
    season_lags(save=True)
    calculate_correlations(save=True)
    season_correlations(save=True)
