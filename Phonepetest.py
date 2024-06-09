#-----------------------------------------------------------------------------------------------------#
# Run in the below in the terminal 
#-----------------------------------------------------------------------------------------------------#
#pip install google-api-python-client 
#pip install isodate
#-----------------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------------#
# Importing required packages
#-----------------------------------------------------------------------------------------------------

import streamlit as st
#from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import json
import os
import mysql.connector as db 
from mysql.connector import Error 
import geojson 
#from urllib.request import urlopen
from datetime import datetime
import  streamlit_toggle as tog
import plotly.graph_objs as go

#-----------------------------------------------------------------------------------------------------#
# set logging details 
#-----------------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------------#
# Defining Database Connection 
#-----------------------------------------------------------------------------------------------------#
db_conn = db.connect (
    host = 'localhost', #server ip
    user = "Senthil",
    password = "Mysql2@24",
    database = "phonepe" ,
    connect_timeout=10000 
    )
curr = db_conn.cursor()

#-----------------------------------------------------------------------------------------------------#
## Code for Streamlit page      
#-----------------------------------------------------------------------------------------------------#

st.set_page_config(layout="wide")
st.header('Phone Pe Transaction Details', divider='rainbow', anchor='Phonepe', ) 
#st.title("Sample Application")
#def page_title (state_name):
#    st.title(f"Phone Pe Transaction Details: {state_name}")
# [theme]
# primaryColor="#F63366"
# backgroundColor="#FFFFFF"
# secondaryBackgroundColor="#F0F2F6"
# textColor="#262730"
# font="sans serif"

# Get the current year
current_year = datetime.today().year

# Create a list of years (for example, from 2000 to current year)
years = list(range(2018, current_year + 1))

#col1, col2 = st.columns(2)
# # Add a dropdown to the first column
# with col1:
#     data = st.selectbox(
#         'Select Data :',
#         ('Users', 'Transactions')
#     )
#     st.write('You selected:', data)
# with col2:
#     quarters = ['Q1', 'Q2', 'Q3', 'Q4']
#     year_quarter_options = [f"{quarter} {year} " for year in years for quarter in quarters]

#         # Create a selectbox with combined year and quarter options
#     selected_year_quarter = st.selectbox('Select Quarter & Year :', year_quarter_options)

#         # Split the selected option into year and quarter
#     selected_quarter, selected_year  = selected_year_quarter.split()
#     st.write(f'Selected Quarter & Year: {selected_quarter} /{selected_year}' )  

  
with st.sidebar:
    st.sidebar.image('PhonePelogo.png', use_column_width=True)
   # opt = option_menu("Pick One", 
             #  ["Data","Plot", "EDA"]) 
    #-----------------------------------------------------------------------------------------------------#
    # Code List of SQL Queries 
    #-----------------------------------------------------------------------------------------------------#

    Q1 = "Q1 - List State wise Aggregated Transactions"
    Q2 = "Q2 - List State wise Aggregated Users"
    Q3 = "Q3 - List District wise Map Transactions"
    Q4 = "Q4 - List Tp 10 State Transactions"
    Q5 = "Q5 - List Top 10 District Transactions"

    option = st.selectbox(
        "Please select a Question to Plot the Map :)",
        (Q1,Q2,Q3,Q4,Q5))

    if option == Q1: 
        #curr.execute("select State, sum(Transacion_amount), sum(Transacion_count) from phonepe.aggr_st_trans group by State" ) 
        curr.execute("select State, CASE WHEN sum(Transacion_amount) >= 1000000000000 THEN CONCAT(ROUND(sum(Transacion_amount) / 1000000000000, 2), ' TN') WHEN sum(Transacion_amount) >= 1000000000 THEN CONCAT(ROUND(sum(Transacion_amount) / 1000000000, 2), ' BN') ELSE CONCAT(sum(Transacion_amount), ' Units') END AS formatted_Transacion_amount, CASE WHEN sum(Transacion_count) >= 1000000000000 THEN CONCAT(ROUND(sum(Transacion_count) / 1000000000000, 2), ' TN') WHEN sum(Transacion_count) >= 1000000000 THEN CONCAT(ROUND(sum(Transacion_count) / 1000000000, 2), ' BN') ELSE CONCAT(sum(Transacion_count), ' Units')	END AS formatted_Transacion_count from phonepe.aggr_st_trans group by State")
        dtls = curr.fetchall() 
        df = pd.DataFrame(dtls, columns= ['States', 'Total Transactions', 'Transacion_count'])
        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            #locationmode='country names',
            color='Total Transactions',
            hover_name='States',
            hover_data=['Transacion_count', 'States'],
            #range_color = (0,1,2),
            color_continuous_scale="rdylgn",
            scope='asia'
            #color_continuous_scale=px.colors.diverging.BrBG,
            #color_continuous_midpoint=0,
            #title='Sample Transaction Map'
            )

        fig.update_geos(fitbounds='locations', visible=False)
        #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
        fig.update_layout(title_text=f'Phone Pe Transaction Details - India', geo=dict(
        showframe=False,showcoastlines=False,), margin={"r":0,"t":0,"l":0,"b":0}, hovermode='x unified')

        #st.plotly_chart(fig,use_container_width=False)

    elif option == Q2:   
        curr.execute("select State, sum(No_of_reg_users), sum(Percentage_share) from phonepe.aggr_st_users group by State" ) 
        dtls = curr.fetchall() 
        df = pd.DataFrame(dtls, columns= ['States', 'No_of_Reg_Users', 'Percentage_share'])
        
        fig = px.choropleth_mapbox(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States', 
            #locationmode='country names',
            color='No_of_Reg_Users',
            hover_name='States',
            hover_data='Percentage_share',
            #range_color = (0, 12),
            color_continuous_scale="ylgnbu", 
            #color_continuous_scale=px.colors.sequential.Plasma,
            mapbox_style='carto-positron',
            center= {'lat':24, 'lon' :78},
            zoom=3, opacity=0.5
            )
        fig.update_layout(title_text=f'Phone Pe Transaction Details - India', geo=dict(
        showframe=False,showcoastlines=False,), width=1500, height=500, margin={"r":0,"t":0,"l":0,"b":0}, hovermode='x unified')
        fig.update_geos(fitbounds='locations', visible=False, projection_type="satellite")
        fig.update_traces(marker_line_width=1)
    elif option == Q3:    
        State_val = st.selectbox(
            'Select State :',
            ('Tamil Nadu', 'Kerala', 'Maharastra', 'Orissa')
        )
        st.write('You selected:', State_val) 
            
        #curr.execute("select REPLACE(District_name,'district','') as District_name , sum(Tot_No_of_Trans), sum(Tot_Trans_val) from phonepe.map_st_trans where state = 'Tamil Nadu' group by District_name order by District_name" ) 
        #dtls = curr.fetchall() 
        if State_val == 'Tamil Nadu':
            dtls = pd.read_csv("Dist_data_with_distID_TN.csv")
            #df = pd.DataFrame(dtls, columns= ['District_name', 'Tot_No_of_Trans', 'Tot_Trans_val', 'ID_2'])
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response) 
                features = dist_gj['features'][1]['properties']['NAME_2']
                id_2 = dist_gj['features'][1]['properties']['ID_2']
                state_name = dist_gj['features'][1]['properties']['NAME_1']
        elif State_val == 'Kerala':
            dtls = pd.read_csv("Dist_data_with_distID_KL.csv")
            #df = pd.DataFrame(dtls, columns= ['District_name', 'Tot_No_of_Trans', 'Tot_Trans_val', 'ID_2'])
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response) 
        elif State_val == 'Maharastra':
            dtls = pd.read_csv("Dist_data_with_distID_MH.csv")
            #df = pd.DataFrame(dtls, columns= ['District_name', 'Tot_No_of_Trans', 'Tot_Trans_val', 'ID_2'])
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response) 
        else: 
            dtls = pd.read_csv("Dist_data_with_distID_OR.csv")
            #df = pd.DataFrame(dtls, columns= ['District_name', 'Tot_No_of_Trans', 'Tot_Trans_val', 'ID_2'])
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response)    
             
        fig = px.choropleth(
            dtls,
            #geojson='india_district_tn.geojson',
            geojson= dist_gj,
            featureidkey='properties.ID_2',
            locations='ID_2',
            #locationmode='ISO-3',
            color='Tot_No_of_Trans', 
            color_continuous_scale="ylgnbu",
            #range_color=(-20,20),
            scope='asia',
            hover_name='District_name',
            hover_data='Tot_Trans_val',
            title= 'State_val'
            #labels={'Tot_No_of_Trans' : 'Tot_Trans_val'}
            #color_continuous_scale=px.colors.sequential.Plasma,
            #mapbox_style='carto-positron',
            #center= {'lat':24, 'lon' :78},
            #zoom=3, opacity=0.5
            )
        #page_title (state_name)
        fig.update_layout(title_text=f'District-Wise Transaction Details for : {State_val}',geo=dict(
        showframe=False,showcoastlines=False,), 
        margin={"r":0,"t":50,"l":0,"b":0}  # Adjust margins to fit the title nicely
        )
        fig.update_geos(fitbounds="locations", visible=False )   #, projection_type="satellite")
        fig.update_traces(marker_line_width=1)
    elif option == Q4:    
        curr.execute("select * from (select a.video_name as 'Video Name', count(b.comment_id) as 'Comment Count' from yth.videos a, yth.Comments b Where a.video_id = b.video_id group by b.video_id  UNION select c.video_name , c.comment_cnt from yth.videos c Where c.comment_cnt = 0) d order by 1") 
        dtls = curr.fetchall()
        df = pd.DataFrame(dtls, columns= ['Video Name', 'Comment Count'])
        st.table(df)
    else:    
        curr.execute("select a.chn_name as 'Channel Name', c.video_name as 'Video Name', c.comment_cnt as 'Comment Count' from yth.channels a, yth.playlists b, yth.videos c Where a.chn_id = b.chn_id and b.playlist_id = c.playlist_id order by c.comment_cnt desc limit 10") 
        dtls = curr.fetchall()
        df = pd.DataFrame(dtls, columns= ['Channel Name', 'Video Name','Comment Count'])
        st.table(df)
          

st.plotly_chart(fig,use_container_width=False)
#fig.show()

#-----------------------------------------------------------------------------------------------------#
## Code st.toggle key and st.container in Streamlit page      
##-----------------------------------------------------------------------------------------------------#

on = st.toggle(label='View Districtwise', label_visibility= 'visible',help='To switch beteen Aggregated-View and Districtwise-View')
if on:
    View = "District"
    table_name = 'phonepe.map_st_trans'
    st.write('District-View Chosen')
          
else:
    View = 'Aggregated'
    table_name = 'phonepe.aggr_st_trans' 
    st.write('Aggregated-View Chosen (default)')

col1,col2 = st.columns(2)
with col1:
    Data = st.selectbox(
        "Select Data : ", ('User','Transaction')
    )
    if Data == "Transaction":
        st.write("Selected : ", Data) 
        with col2:
            quarters = ['Q1', 'Q2', 'Q3', 'Q4']
            year_quarter_options = [f"{quarter} {year} " for year in years for quarter in quarters]

            # Create a selectbox with combined year and quarter options
            selected_year_quarter = st.selectbox('Select Quarter & Year :', year_quarter_options)

            # Split the selected option into year and quarter
            selected_quarter, selected_year  = selected_year_quarter.split()
            st.write(f'Selected Quarter & Year: {selected_quarter} /{selected_year}' )  
    else:
        st.write("Selected : ", Data) 

with st.container(border=True,height=400):
    if View == "Aggregated": 
        if Data == "Transaction":
            st.write("Aggregated Transaction")     
            Quater_val = selected_quarter[1]
            Agg_Tran_sql = """select State, sum(Transacion_amount), sum(Transacion_count) from phonepe.aggr_st_trans Where Quater = %s and Year = %s group by State"""
            curr.execute(Agg_Tran_sql,(Quater_val, selected_year )) 
            dtls = curr.fetchall() 
            df = pd.DataFrame(dtls, columns= ["State", "Tot_Trans_val", "Tot_No_of_Trans"])
            #st.write(df)
            #st.bar_chart(df, x='State' , y='Tot_No_of_Trans') 
            # # Create the plot
            # fig = go.Figure()
            # fig.add_trace(go.Scatter(x= df['State'], y= df["Tot_Trans_val"], mode='lines+text', name='Data Points'))

            # # Customize the layout
            # fig.update_layout( title='Line Chart with Dots', xaxis_title='State', 
            #                   yaxis_title='"Tot_Trans_val"')
            # # Display the plot in Streamlit
            # st.plotly_chart(fig)
            
            # Create the bar chart
            bar_trace = go.Bar(
                x=df['State'],
                y=df["Tot_Trans_val"],
                name='Bar Chart',
                marker=dict(color='rgba(200, 83, 109, 0.7)')
            )

            # Create the line chart with dots
            line_trace = go.Scatter(
                x=df['State'],
                y=df["Tot_Trans_val"],
                mode='lines+markers',
                name='Line Chart with Dots',
                marker=dict(color='rgba(55, 82, 193, .9)')
            )

            # Combine the bar and line charts
            fig = go.Figure(data=[bar_trace, line_trace])

            # Customize the layout
            fig.update_layout(
                title='Combined Bar and Line Chart with Dots',
                xaxis_title='Category',
                yaxis_title='Values',
                barmode='group'
            )

            # Display the plot in Streamlit
            st.plotly_chart(fig)
            
            
            
        else:
            st.write("Aggregated User")
            #curr.execute("select State, sum(No_of_reg_users), sum(Percentage_share) from phonepe.aggr_st_users group by State")
            curr.execute("select State, Brand_name, sum(No_of_reg_users), sum(Percentage_share) from phonepe.aggr_st_users group by brand_name, State")
            dtls = curr.fetchall() 
            df = pd.DataFrame(dtls, columns= ["State","Brand_name","Tot_No_of_Users", "Tot_Percent_share"])
            #st.write(df)
            #st.bar_chart(df, x='State' , y='Tot_No_of_Users') 
            
            # # Create bar traces for each group
            # trace1 = go.Bar(
            #     x=df['State'],
            #     y=df['Tot_No_of_Users'],
            #     name='Group 1',
            #     marker=dict(color='rgba(55, 83, 109, 0.7)')
            # )

            # trace2 = go.Bar(
            #     x=df['State'],
            #     y=df['Tot_Percent_share'],
            #     name='Group 2',
            #     marker=dict(color='rgba(26, 118, 255, 0.7)')
            # )

            # # Combine the traces
            # data = [trace1, trace2]

            # # Define the layout
            # layout = go.Layout(
            #     title='Grouped Bar Chart',
            #     xaxis=dict(title='State'),
            #     yaxis=dict(title='Total Users & Percent Share'),
            #     barmode='group'  # Group bars side by side
            # )

            # # Create the figure
            # fig = go.Figure(data=data, layout=layout)

            # # Display the plot in Streamlit
            # st.plotly_chart(fig)
            
            # Pivot the DataFrame to get the data in the correct format for plotting
            pivot_df = df.pivot(index='State', columns='Brand_name', values='Tot_No_of_Users')

            # Create bar traces for each brand
            traces = []
            for brand in pivot_df.columns:
                traces.append(
                    go.Bar(
                        x=pivot_df.index,
                        y=pivot_df[brand],
                        name=brand
                    )
                )

            # Define the layout
            layout = go.Layout(
                title='Brand-wise Registered Users in Each State',
                xaxis=dict(title='State'),
                yaxis=dict(title='Registered Users'),
                barmode='group'  # Group bars side by side
            )

            # Create the figure
            fig = go.Figure(data=traces, layout=layout)

            # Display the plot in Streamlit
            st.plotly_chart(fig)

            
    else:
        if Data == "Transaction":
            st.write("District Transaction")  
            Quater_val = selected_quarter[1]   
            Map_Tran_sql = """select District_name, sum(Tot_No_of_Trans), sum(Tot_Trans_val) from phonepe.map_st_trans Where state = %s and Quater = %s and Year = %s group by District_name"""
            curr.execute(Map_Tran_sql, (State_val, Quater_val, selected_year)) 
            dtls = curr.fetchall() 
            df = pd.DataFrame(dtls, columns= ["District_name","Tot_No_of_Trans", "Tot_Trans_val"])
            #st.write(df)
            #st.line_chart(df, x='District_name' , y='Tot_No_of_Trans') 
            
            # Create bar traces for each group
            trace1 = go.Bar(
                x=df['District_name'],
                y=df['Tot_No_of_Trans'],
                name='Group 1',
                marker=dict(color='rgba(55, 83, 109, 0.7)')
            )

            # trace2 = go.Bar(
            #     x=df['District_name'],
            #     y=df['Tot_Trans_val'],
            #     name='Group 2',
            #     marker=dict(color='rgba(26, 118, 255, 0.7)')
            # )

            # Combine the traces
            data = [trace1] #, trace2]

            # Define the layout
            layout = go.Layout(
                title='Grouped Bar Chart',
                xaxis=dict(title='District_name'),
                yaxis=dict(title='Total Transaction'),
                barmode='group'  # Group bars side by side
            )

            # Create the figure
            fig = go.Figure(data=data, layout=layout)

            # Display the plot in Streamlit
            st.plotly_chart(fig)

            trace2 = go.Bar(
                x=df['District_name'],
                y=df['Tot_Trans_val'],
                name='Group 2',
                marker=dict(color='rgba(26, 118, 255, 0.7)')
            )

            # Combine the traces
            data = [trace2]

            # Define the layout
            layout = go.Layout(
                title='Grouped Bar Chart',
                xaxis=dict(title='District_name'),
                yaxis=dict(title='Transaction Value'),
                barmode='group'  # Group bars side by side
            )

            # Create the figure
            fig = go.Figure(data=data, layout=layout)

            # Display the plot in Streamlit
            st.plotly_chart(fig)
            
        else:
            st.write("District User")
            #Top_Users_sql = """select State, District_name, sum(Registered_users) from phonepe.top_st_users Where state = %s group by District_name"""
            #curr.execute(Top_Users_sql, ([State_val]))
            curr.execute("select State, District_name, sum(Registered_users) from phonepe.top_st_users group by District_name, state")
            dtls = curr.fetchall() 
            df = pd.DataFrame(dtls, columns= ["State","District_name","Registered_users"])
            #st.write(df)
            
            # Pivot the DataFrame to get the data in the correct format for plotting
            pivot_df = df.pivot(index='State', columns='District_name', values='Registered_users')

            # Create bar traces for each brand
            traces = []
            for Dist in pivot_df.columns:
                traces.append(
                    go.Bar(
                        x=pivot_df.index,
                        y=pivot_df[Dist],
                        name=Dist
                    )
                )

            # Define the layout
            layout = go.Layout(
                title='District-wise Registered Users in Each State',
                xaxis=dict(title='State'),
                yaxis=dict(title='Registered Users'),
                barmode='stack'  # Stack bars on top of each other
            )

            # Create the figure
            fig = go.Figure(data=traces, layout=layout)

            # Display the plot in Streamlit
            st.plotly_chart(fig) 
        
    #st.write(df) 
    #contain_dtls = pd.read_csv("Dist_data _with_distID.csv") 
# You can call any Streamlit command, including custom components:
    #st.bar_chart(np.random.randn(50, 3))
    #st.bar_chart(df, x='District_name' , y='Tot_No_of_Trans') 
    #st.line_chart(df, x='District_name' , y='Tot_No_of_Trans') 
    #st.line_chart(df)
#st.write("This is outside the container", 'State')

curr.close()
db_conn.close() 