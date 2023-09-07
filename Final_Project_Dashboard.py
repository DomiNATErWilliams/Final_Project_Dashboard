# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 21:41:11 2023

@author: Nate
"""


import time  # to simulate a real time data, time loop

import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import altair as alt

df=pd.read_csv('Master_Sheet.csv')
df=df.sort_values('Year', ascending=True)

alt.data_transformers.disable_max_rows()


st.set_page_config(
    page_title="Sports History by City",
    page_icon="✅",
    layout="wide",
 )

st.title("An Analysis of Professional Sports Success in North American Cities")

tab1, tab2, tab3 = st.tabs(["Data Descriptions", "Animated Graphs", "Data"])


with tab1:
    st.header("Historical Sports Data")
    
 
    
    fig_col1, fig_col2, fig_col3 = st.columns(3)

##############################################################################
    with fig_col1:
        champs_df = (df
        .groupby(['City'], as_index = False)
        .agg(
            avg_wl = ('W-L%', 'mean'),
            champions_awarded = ('Champion', 'sum'),
            num_teams = ('Year', 'count')
            )
        )
    
     
    
        champs_df.rename(columns = {'avg_wl':'W-L%', 'champions_awarded':"Championships", 'num_teams':'Number of Teams'},
                   inplace = True)
        
        champs = champs_df[champs_df['Championships'] > 10]
        arcs=alt.Chart(champs).mark_arc().encode(
            theta="Championships",
            color= alt.Color("City").scale(scheme='tableau20'),
            tooltip=['City', 'Championships', 'Number of Teams'],
        ).properties(title = 'Number of Championships by City')
        
        st.write(arcs)
        
        
        
        
#################################################################################
    with fig_col2:
        
        teams = champs_df[champs_df['Number of Teams'] > 150]
        arcs2=alt.Chart(teams).mark_arc().encode(
            theta="Number of Teams",
            color= alt.Color("City").scale(scheme='category20b'),
            tooltip=['City', 'Number of Teams']
        ).properties(title = 'Number of Teams by City')
        
        st.write(arcs2)
##########################################################################################   
    with fig_col3:
        champs['Championships per Number of Seasons Played']=champs['Championships']/champs['Number of Teams']

        arcs3=alt.Chart(champs).mark_arc().encode(
            theta='Championships per Number of Seasons Played',
            color= alt.Color("City").scale(scheme='category20b'),
            tooltip=['City', 'Number of Teams', 'Number of Teams']
        ).properties(title = 'Championships Won per Total Number of Seasons Played')
        
        st.write(arcs3)
        
        
        
###########################################################################################
    st.write("##")
    city_df = (df
        .groupby(['Year', 'City'], as_index = False)
        .agg(
            avg_wl = ('W-L%', 'mean'),
            champions_awarded = ('Champion', 'sum'),
            num_teams = ('Year', 'count')
            )
        )
    
     
    
    city_df.rename(columns = {'avg_wl':'W-L%', 'champions_awarded':"Championships", 'num_teams':'Number of Teams'},
                   inplace = True) 
    
    select = alt.selection_point(
        fields=['City'],
        bind={
            'City': alt.binding_select(
                options= city_df['City'].unique(),
                name='City: '
            )     
        },
        value = 'Akron'
    )
    
     
    
    space = 'W-L%'
    points=alt.Chart(city_df).mark_point().encode(
        x = alt.X('Year:O', axis=alt.Axis(labelAngle=-45, labelOverlap = True)),
        y='W-L%:Q',
        color = alt.condition(alt.datum['W-L%'] > 0.5, 
                                alt.ColorValue('green'), 
                                alt.ColorValue('red')),
        tooltip=['Year', 'W-L%', 'Number of Teams'],
        size = alt.Size(
            "Number of Teams:N"),
    ).properties(width = 1400, height = 400, title = 'Historical Win Loss Percentage of Teams in a City'
    ).add_params(
        select
    ).transform_filter(
        select
    )
        
    st.write(points) 
        
###############################################################################################
    leagues_df = (df
        .groupby(['League', 'City'], as_index = False)
        .agg(
            avg_wl = ('W-L%', 'mean'),
            champions_awarded = ('Champion', 'sum'),
            num_teams = ('Year', 'count')
            )
        )
    
     
    
    leagues_df.rename(columns = {'avg_wl':'W-L%', 'champions_awarded':"Championships", 'num_teams':'Number of Teams'},
                   inplace = True)
    #leagues_df
    
    champs = leagues_df[leagues_df['Championships'] > 1]
    base = alt.Chart().mark_arc().encode(
        theta="Championships",
        color= alt.Color("City").scale(scheme='tableau20'),
        tooltip=['City', 'Championships', 'Number of Teams'],
    ).properties(width = 200, height = 200
    )
    
     
    
    arcs3=base.facet(
        data = champs,
        facet = alt.Facet('League:N'),
        columns = 5
    ).resolve_scale(color='independent').properties(title = 'Number of Championships by City'
    ).configure_title(fontSize=20, offset=5, orient='top', anchor='middle')
                                                    
    st.write(arcs3) 
#############################################################################################
    fig_col1, fig_col2, fig_col3, fig_col4, fig_col5 = st.columns(5)
    champs2_df = (df
    .groupby(['League', 'City'], as_index = False)
    .agg(
        avg_wl = ('W-L%', 'mean'),
        champions_awarded = ('Champion', 'sum'),
        num_teams = ('Year', 'count')
        )
    )

 

    champs2_df.rename(columns = {'avg_wl':'W-L%', 'champions_awarded':"Championships", 'num_teams':'Number of Seasons'},
                   inplace = True)
    champs2_df['Championships Per Season'] = champs2_df['Championships'] / champs2_df['Number of Seasons']

    
    with fig_col1:

        champ2 = champs2_df[(champs2_df['Championships Per Season'] > 0.03) & (champs2_df['League'] == 'MLB')]
        mlb=alt.Chart(champ2).mark_bar().encode(
            x=alt.X('City:N', sort=alt.SortField(field='Championships Per Season', order='descending')),
            y = alt.Y('Championships Per Season'),
            color= alt.Color("City").scale(scheme='tableau20'),
            tooltip=['City', 'Championships', 'Number of Seasons', 'Championships Per Season'],
        ).properties(title = 'MLB Number of Championships Per Season by City', width=400)
        
        st.write(mlb)
        
    with fig_col4:

        champ2 = champs2_df[(champs2_df['Championships Per Season'] > 0.05) & (champs2_df['League'] == 'NFL')]
        NFL=alt.Chart(champ2).mark_bar().encode(
            x=alt.X('City:N', sort=alt.SortField(field='Championships Per Season', order='descending')),
            y = alt.Y('Championships Per Season'),
            color= alt.Color("City").scale(scheme='tableau20'),
            tooltip=['City', 'Championships', 'Number of Seasons', 'Championships Per Season'],
        ).properties(title = 'NFL Number of Championships Per Season by City', width=400)
        
        st.write(NFL)
    
    with fig_col3:

        champ2 = champs2_df[(champs2_df['Championships Per Season'] > 0.03) & (champs2_df['League'] == 'NBA')]
        NBA=alt.Chart(champ2).mark_bar().encode(
            x=alt.X('City:N', sort=alt.SortField(field='Championships Per Season', order='descending')),
            y = alt.Y('Championships Per Season'),
            color= alt.Color("City").scale(scheme='tableau20'),
            tooltip=['City', 'Championships', 'Number of Seasons', 'Championships Per Season'],
        ).properties(title = 'NBA Number of Championships Per Season by City', width=400)
        
        st.write(NBA)
        
    with fig_col2:

        champ2 = champs2_df[(champs2_df['Championships Per Season'] > 0.05) & (champs2_df['League'] == 'MLS')]
        MLS=alt.Chart(champ2).mark_bar().encode(
            x=alt.X('City:N', sort=alt.SortField(field='Championships Per Season', order='descending')),
            y = alt.Y('Championships Per Season'),
            color= alt.Color("City").scale(scheme='tableau20'),
            tooltip=['City', 'Championships', 'Number of Seasons', 'Championships Per Season'],
        ).properties(title = 'MLS Number of Championships Per Season by City', width=400)
        
        st.write(MLS)
        
    with fig_col5:

        champ2 = champs2_df[(champs2_df['Championships Per Season'] > 0.05) & (champs2_df['League'] == 'NHL')]
        NHL=alt.Chart(champ2).mark_bar().encode(
            x=alt.X('City:N', sort=alt.SortField(field='Championships Per Season', order='descending')),
            y = alt.Y('Championships Per Season'),
            color= alt.Color("City").scale(scheme='tableau20'),
            tooltip=['City', 'Championships', 'Number of Seasons', 'Championships Per Season'],
        ).properties(title = 'NHL Number of Championships Per Season by City', width=400)
        
        st.write(NHL)
                                               
###############################################################################################
    
with tab2:
    st.header('Animated Charts')
    
    
    ####################################################################################
    df=df.query('Champion!=0')

    df=df.assign(
        Total_Championships=lambda x:
        x.groupby('City')
        ['Champion']
        .transform(lambda s: s.cumsum())
    )

    bars_championships=alt.Chart(df).mark_bar().encode(
        x=alt.X('City:N', title='City').sort('-y'),
        y=alt.Y('Champion:Q', title='Championships'),
        color=alt.Color('League:N').scale(scheme='tableau10'),
        tooltip=['Year','City','League','Tm']
    ).properties(width=1500, height=400, title='Number of Championships Won in each City')

    bars_year=alt.Chart(df).mark_bar().encode(
        x=alt.X('Year:N', title='Year', axis=alt.Axis(labelAngle=45, labelOverlap=True)),
        y=alt.Y('Champion:Q', title='Championships'),
        color=alt.Color('League:N').scale(scheme='tableau10'),
        tooltip=['Year','City','League','Tm']
    ).properties(width=1500, height=100, title='Number of Championships Played each Year')

    

    bars=alt.vconcat(bars_championships, bars_year)
    
    

    def plot_animation(df):
        bars_championships=alt.Chart(df).mark_bar().encode(
            x=alt.X('City:N', title='City').sort('-y'),
            y=alt.Y('Champion:Q', title='Championships'),
            color=alt.Color('League:N').scale(scheme='tableau10'),
            tooltip=['Year','City','League','Tm']
        ).properties(width=1500, height=400, title='Number of Championships won in each City')

        bars_year=alt.Chart(df).mark_bar().encode(
            x=alt.X('Year:N', title='Year', axis=alt.Axis(labelAngle=45, labelOverlap=True)),
            y=alt.Y('Champion:Q', title='Championships'),
            color=alt.Color('League:N').scale(scheme='tableau10'),
            tooltip=['Year','City','League','Tm']
        ).properties(width=1500, height=100, title='Number of Championships Played each Year')
        

        bars=alt.vconcat(bars_championships, bars_year)
        
        return bars

    N = df.shape[0] # number of elements in the dataframe
    burst = 1       # number of elements (months) to add to the plot
    size = burst     # size of the current dataset

    bar_plot = st.altair_chart(bars)
    start_btn = st.button('Start')

    if start_btn:
       for i in range(1,N):
          step_df = df.iloc[0:size]
          bars = plot_animation(step_df)
          bar_plot = bar_plot.altair_chart(bars)
          size = i + burst
          if size >= N: 
             size = N - 1
          time.sleep(0.1)
          
    
    
    
    
    
    
    df=df.assign(
        Total_Championships=lambda x:
        x.groupby('City')
        ['Champion']
        .transform(lambda s: s.cumsum())
    )

    df_best_10=df.groupby(['City']).agg(Total_Championships=('Champion','sum')).sort_values('Total_Championships', ascending=False).head(10)
    best_10=list(df_best_10.index)
    df=df[df['City'].isin(best_10)]

    nearest = alt.selection_point(nearest=True, on='mouseover',
                            fields=['Year'], empty=False)


    line=alt.Chart(df).mark_line(interpolate='basis').encode(
        x=alt.X('Year:N', title='Year', axis=alt.Axis(labelAngle=45, labelOverlap=True)),
        y=alt.Y('Total_Championships:Q', title='Championships'),
        color=alt.Color('City:N').scale(scheme='tableau10')
    )
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(df).mark_point().encode(
        x='Year:N',
        opacity=alt.value(0),
    ).add_params(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=5).encode(
        text=alt.condition(nearest, 'Total_Championships:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='Year:N',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    lines=alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=1500, height=500, title='Number of Championships Won in each City over Time'
    )


    def plot_animation(df):
       
        nearest = alt.selection_point(nearest=True, on='mouseover',
                            fields=['Year'], empty=False)


        line=alt.Chart(df).mark_line(interpolate='basis').encode(
            x=alt.X('Year:N', title='Year', axis=alt.Axis(labelAngle=45, labelOverlap=True)),
            y=alt.Y('Total_Championships:Q', title='Championships'),
            color=alt.Color('City:N').scale(scheme='tableau10')
        )
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(df).mark_point().encode(
            x='Year:N',
            opacity=alt.value(0),
        ).add_params(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=5).encode(
            text=alt.condition(nearest, 'Total_Championships:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x='Year:N',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        lines=alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=1500, height=500, title='Number of Championships Won in each City over Time'
        )


        return lines

    N = df.shape[0] # number of elements in the dataframe
    burst = 1       # number of elements (months) to add to the plot
    size = burst     # size of the current dataset

    line_plot = st.altair_chart(lines)
    start_btn2 = st.button('Start Line Graph')

    if start_btn2:
       for i in range(1,N):
          step_df = df.iloc[0:size]
          lines = plot_animation(step_df)
          line_plot = line_plot.altair_chart(lines)
          size = i + burst
          if size >= N: 
             size = N - 1
          time.sleep(0.1)
          
###########################################################################################

with tab3:
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        fig_col1.subheader('Master Dataframe of All Data')
        df=pd.read_csv('Master_Sheet.csv')
        df=df.sort_values('Year', ascending=True)
    
        alt.data_transformers.disable_max_rows()
        df=df.assign(
            Total_Championships=lambda x:
            x.groupby('City')
            ['Champion']
            .transform(lambda s: s.cumsum())
        )
        df=df.reset_index()
        df=df.drop(columns=['index']).sort_values('Year')
        st.dataframe(df, height=700)
        
        
    with fig_col2:
        fig_col2.subheader('Summary Statistics of Data')
        all_sports_df=pd.read_csv('Master_Sheet.csv')
        num_of_seasons_df=pd.DataFrame()
        num_of_seasons_df['League']=list(all_sports_df['League'].unique())
        num_of_seasons=[]
        first_season=[]
        most_recent_season=[]
        num_of_championships=[]
        num_of_teams=[]
        for league in list(all_sports_df['League'].unique()):
            num_of_seasons.append(len(all_sports_df[all_sports_df['League']==league]['Year'].unique()))
            first_season.append(min(all_sports_df[all_sports_df['League']==league]['Year'].unique()))
            most_recent_season.append(max(all_sports_df[all_sports_df['League']==league]['Year'].unique()))
            num_of_championships.append(all_sports_df[all_sports_df['League']==league]['Champion'].sum())
            num_of_teams.append(len(all_sports_df[all_sports_df['League']==league]['Tm'].unique()))
            
        num_of_seasons_df['Number of Seasons']=num_of_seasons
        num_of_seasons_df['First Season']=first_season
        num_of_seasons_df['Most Recent Season']=most_recent_season
        num_of_seasons_df['Championships Played']=num_of_championships
        num_of_seasons_df['Number of Teams']=num_of_teams
        num_of_seasons_df.set_index('League')
        st.dataframe(num_of_seasons_df)
    
        season=alt.Chart(num_of_seasons_df).mark_bar().encode(
            x=alt.X('League'),
            y=alt.Y('Number of Seasons'),
            color=alt.Color('League')
            
        ).properties(width=180)
        
        champ=alt.Chart(num_of_seasons_df).mark_bar().encode(
            x=alt.X('League'),
            y=alt.Y('Championships Played'),
            color=alt.Color('League')
            
        ).properties(width=180)
        
        team=alt.Chart(num_of_seasons_df).mark_bar().encode(
            x=alt.X('League'),
            y=alt.Y('Number of Teams'),
            color=alt.Color('League')
            
        ).properties(width=180)
        
        charts=alt.hconcat(season, champ, team)
        st.write(charts)
