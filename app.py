import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

from streamlit import sidebar


df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')
import preprocessor,helper

df=preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympic Analysis')
st.sidebar.image('Olympic_rings_with_transparent_rims (1).svg')
user_menu=sidebar.radio(
    'Select An Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete wise Analysis' )
)




if user_menu=='Medal Tally':
    st.sidebar.header('Medal_tally')
    years,countries=helper.country_year_list(df)

    selected_year= st.sidebar.selectbox('Select year',years)
    selected_country = st.sidebar.selectbox('Select country', countries)

    medal_tally=helper.fetch(df,selected_year,selected_country)
    if selected_country=='overall'and selected_year=='overall':
        st.title('Overall Tally')
    if selected_year!='overall'and selected_country=='overall':
        st.title('Medal Tally in '+str(selected_year))
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country+'Overall Performance')
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country+' Performance in '+ str(selected_year)+' Olympics ')
    if medal_tally.empty:
       st.title('Did not participate')
    else:
     st.table(medal_tally)
if user_menu=="Overall Analysis":
    editions=df['Year'].unique().shape[0]-1
    cities =df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events =df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title("Top Statistic ")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Edition")
        st.title(editions)
    with col2:
        st.header("Host")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nation_over_time=helper.data_nation_over_time(df,'region')
    fig = px.line(nation_over_time, x='Year', y='region')
    st.title('Participating Nation Over The Year')
    st.plotly_chart(fig)

    Event_over_time = helper.data_nation_over_time(df,'Event')
    fig = px.line(Event_over_time, x='Year', y='Event' )
    st.title('Event  Over The Years')
    st.plotly_chart(fig)

    athlete_over_time = helper.data_nation_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Year', y='Name')
    st.title('Athletes  Over The Years')
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport)")
    fig,axx=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    axx=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')
    selected_sport=st.selectbox('Select sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-Wise Analysis':
      st.sidebar.title("Country-wise Analysis")
      country_list=df['region'].dropna().unique()
      country_list.sort()
      selected_country=st.sidebar.selectbox('Select a country',country_list)
      countrydf=helper.yearwise_medal_tally(df,selected_country)
      fig = px.line(countrydf, x='Year', y='Medal')
      st.title(selected_country+' Medal Tally over the Year')
      st.plotly_chart(fig)
# heatmap for country with  their sport
      st.title(selected_country + ' excels in their following sport ')
      pt=helper.country_event_heatmap(df,selected_country)
      fig, ax = plt.subplots(figsize=(20, 20))
      if not pt.empty:
          ax = sns.heatmap(pt, annot=True)
      else:
          st.write("No data available to display heatmap.")

      st.pyplot(fig)
 # top 10 athelets in country
      st.title("Top 10 Atletes of "+selected_country)
      top10df=helper.most_successful_countrywise(df,selected_country)
      st.table(top10df)

if user_menu=='Athlete wise Analysis':
    athelet_df = df.drop_duplicates(subset=["Name", 'region'])
    x1 = athelet_df['Age'].dropna()
    x2 = athelet_df[athelet_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelet_df[athelet_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelet_df[athelet_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Ager', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                              show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')

    selected_sport = st.selectbox('Select sport', sport_list)
    tmp_df=helper.weight_v_hight(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=tmp_df['Weight'], y=tmp_df['Height'], hue=tmp_df['Medal'], style=tmp_df['Sex'], s=60)
    st.title('Height vs Weight ')
    st.pyplot(fig)

    final=helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.title('Men vs Women')
    st.plotly_chart(fig)