import numpy as np


def fetch(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_df
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    return x
def medal_Tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['Total']=medal_tally['Total'].astype('int')

    return medal_tally
def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return year,country

def data_nation_over_time(df,col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time.rename(columns={'count':col},inplace=True)
    return nation_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x
def yearwise_medal_tally(df,country):
    tmp = df.dropna(subset=['Medal'])
    tmp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    newdf = tmp[tmp['region'] == country]
    finaldf = newdf.groupby('Year').count()['Medal'].reset_index()
    return finaldf
def country_event_heatmap(df,country):
    tmp = df.dropna(subset=['Medal'])
    tmp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    newdf = tmp[tmp['region'] == country]
    pt=newdf.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x
def weight_v_hight(df,sport):
    athelet_df=df.drop_duplicates(subset=['Name','region'])
    athelet_df['Medal'].fillna('No Medal', inplace=True)
    if sport!='overall':
     tmp_df = athelet_df[athelet_df['Sport'] == sport]
     return tmp_df
    else :
       return athelet_df
def men_vs_women(df):
    athelet_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athelet_df[athelet_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athelet_df[athelet_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()


    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final