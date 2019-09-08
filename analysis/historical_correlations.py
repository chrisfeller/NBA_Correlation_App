# Project: NBA Correlations App
# Description: Calculate correlations between statistics historically
# Data Sources: Basketball-Reference
# Last Updated: 7/9/2019

import pandas as pd

def all_time_correlations(save=False):
    # Read in Basketball-Reference tables
    bbref_team_data = pd.read_csv('../app/data/Team_Stats.csv')

    # Basketball-Reference All-Time Correlations
    # Calculate pearson correlation of all numerical metrics in basketball-reference tables
    pearson_corr_df = bbref_team_data.corr(method='pearson')
    # Select only correlations with W/L%
    pearson_corr_df = pearson_corr_df['W/L%'].reset_index()
    pearson_corr_df.columns = ['STATISTIC', 'PEARSON_CORRELATION']
    # Calculate absolute value of pearson correlation to create rank order of metrics
    pearson_corr_df['PEARSON_CORRELATION_ABS'] = abs(pearson_corr_df['PEARSON_CORRELATION'])

    # Calcuklate spearman correlation of all numberical metrics in basketball-reference tables
    spearman_corr_df = bbref_team_data.corr(method='spearman')
    # Select only correlations with W/L%
    spearman_corr_df = spearman_corr_df['W/L%'].reset_index()
    spearman_corr_df.columns = ['STATISTIC', 'SPEARMAN_CORRELATION']
    # Calculate absolute value of spearman correlation to create rank order of metrics
    spearman_corr_df['SPEARMAN_CORRELATION_ABS'] = abs(spearman_corr_df['SPEARMAN_CORRELATION'])

    # Join pearson and spearman correlations
    bbref_correlation_df = (pearson_corr_df.merge(spearman_corr_df, on='STATISTIC')
                                          .sort_values(by='PEARSON_CORRELATION_ABS', ascending=False)
                                          .dropna()
                                          .round(3))
    # Remove irrelivent metric RANK and W/L% as that will always have a perfect correlation with itself
    bbref_correlation_df = bbref_correlation_df[~bbref_correlation_df['STATISTIC'].isin(['RANK', 'W/L%'])]
    # Create rank of relationship strength based on absolute value of pearson correlation
    bbref_correlation_df['PEARSON_CORRELATION_RANK'] = range(1, 1+len(bbref_correlation_df))
    bbref_correlation_df.sort_values(by='SPEARMAN_CORRELATION_ABS', ascending=False, inplace=True)
    # Create rank of relationship strength based on absolute value of spearman correlation
    bbref_correlation_df['SPEARMAN_CORRELATION_RANK'] = range(1, 1+len(bbref_correlation_df))
    # Create an average rank based on r-quared and correlation ranks
    bbref_correlation_df['AVERAGE_RANK'] = (bbref_correlation_df[['PEARSON_CORRELATION_RANK',
                                                                  'SPEARMAN_CORRELATION_RANK']]
                                            .mean(axis=1)
                                            .round(1))
    bbref_correlation_df.sort_values(by='AVERAGE_RANK', inplace=True)
    bbref_correlation_df = bbref_correlation_df[['STATISTIC', 'PEARSON_CORRELATION',
                                                'PEARSON_CORRELATION_ABS', 'SPEARMAN_CORRELATION',
                                                'SPEARMAN_CORRELATION_ABS', 'PEARSON_CORRELATION_RANK',
                                                'SPEARMAN_CORRELATION_RANK', 'AVERAGE_RANK']]
    if save:
        bbref_correlation_df.to_csv('../app/data/Basketball_Reference_Total_Correlations.csv',
                                    index=False)
    return bbref_correlation_df

def season_correlations(save=False):
    # Read in Basketball-Reference tables
    bbref_team_data = pd.read_csv('../app/data/Team_Stats.csv')

    # Basketball-Reference Correlations by Season
    bbref_correlation_season_df = pd.DataFrame()
    # Loop through each season in basketball-reference tables replicating the same process as above
    for season in bbref_team_data['SEASON'].unique():
        pearson_corr_df = bbref_team_data[bbref_team_data['SEASON']==season].corr(method='pearson')
        pearson_corr_df = pearson_corr_df['W/L%'].reset_index()
        pearson_corr_df.columns = ['STATISTIC', 'PEARSON_CORRELATION']
        pearson_corr_df['PEARSON_CORRELATION_ABS'] = abs(pearson_corr_df['PEARSON_CORRELATION'])

        spearman_corr_df = bbref_team_data[bbref_team_data['SEASON']==season].corr(method='spearman')
        spearman_corr_df = spearman_corr_df['W/L%'].reset_index()
        spearman_corr_df.columns = ['STATISTIC', 'SPEARMAN_CORRELATION']
        spearman_corr_df['SPEARMAN_CORRELATION_ABS'] = abs(spearman_corr_df['SPEARMAN_CORRELATION'])

        correlation_df = pearson_corr_df.merge(spearman_corr_df, on=['STATISTIC'])
        correlation_df['SEASON'] = season
        correlation_df = correlation_df[~correlation_df['STATISTIC'].isin(['RANK', 'W/L%'])]
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
    all_time_correlations(save=True)
    season_correlations(save=True)
