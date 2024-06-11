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
import pandas as pd
import plotly.express as px
import json
import os
import mysql.connector as db 
import geojson 
from datetime import datetime
import  streamlit_toggle as tog
import plotly.graph_objs as go
import matplotlib.pyplot as plt 
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

# Get the current year
current_year = datetime.today().year-1

# Create a list of years (for example, from 2000 to current year)
years = list(range(2018, current_year + 1))

with st.sidebar:
    st.sidebar.image('PhonePelogo.png', use_column_width=True)
    #-----------------------------------------------------------------------------------------------------#
    # Code List of SQL Queries 
    #-----------------------------------------------------------------------------------------------------#

    Q1 = "Q1 - List State wise Aggregated Transactions"
    Q2 = "Q2 - List State wise Aggregated Users"
    Q3 = "Q3 - List District wise Map Transactions"
    Q4 = "Q4 - List Top 10 Users Districts-wise in each State "
    Q5 = "Q5 - State wise Aggregated Insurance Details"

    option = st.selectbox(
        "Please select a Question to Plot the Map :)",
        (Q1,Q2,Q3,Q4,Q5))

    if option == Q1: 
        #curr.execute("select State, sum(Transacion_amount), sum(Transacion_count) from phonepe.aggr_st_trans group by State" ) 
        curr.execute("select State, CASE WHEN sum(Transacion_amount) >= 1000000000000 THEN CONCAT(ROUND(sum(Transacion_amount) / 1000000000000, 2), ' TN') WHEN sum(Transacion_amount) >= 1000000000 THEN CONCAT(ROUND(sum(Transacion_amount) / 1000000000, 2), ' BN') ELSE CONCAT(sum(Transacion_amount), ' Units') END AS formatted_Transacion_amount, CASE WHEN sum(Transacion_count) >= 1000000000000 THEN CONCAT(ROUND(sum(Transacion_count) / 1000000000000, 2), ' TN') WHEN sum(Transacion_count) >= 1000000000 THEN CONCAT(ROUND(sum(Transacion_count) / 1000000000, 2), ' BN') ELSE CONCAT(sum(Transacion_count), ' Units')	END AS formatted_Transacion_count from phonepe.aggr_st_trans group by State")
        dtls = curr.fetchall() 
        df = pd.DataFrame(dtls, columns= ['States', 'Total Transaction Amount', 'Total Transacion Count'])
        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States',
            color='Total Transaction Amount',
            hover_name='States',
            hover_data=['Total Transacion Count', 'States'],
            color_continuous_scale="rdylgn",
            scope='asia'
            )

        fig.update_geos(fitbounds='locations', visible=False)
        fig.update_layout(title_text=f'Phone Pe Transaction Details - India', geo=dict(
        showframe=False,showcoastlines=False,),width=1500, height=500, margin={"r":0,"t":0,"l":0,"b":0}, hovermode='x unified')

    elif option == Q2:   
        curr.execute("select State, CASE WHEN sum(No_of_reg_users) >= 1000000000 THEN CONCAT(ROUND(sum(No_of_reg_users) / 1000000000, 2), ' BN') WHEN sum(No_of_reg_users) >= 1000000 THEN CONCAT(ROUND(sum(No_of_reg_users) / 1000000, 2), ' MN') ELSE CONCAT(sum(No_of_reg_users), ' Units') END AS formatted_No_of_reg_users, sum(round(Percentage_share,2)) from phonepe.aggr_st_users group by State" ) 
        dtls = curr.fetchall() 
        df = pd.DataFrame(dtls, columns= ['States', 'Total Registered Users', 'Total Percentage Share'])
        
        fig = px.choropleth_mapbox(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States', 
            color='Total Registered Users',
            hover_name='States',
            hover_data='Total Percentage Share',
            color_continuous_scale="ylgnbu", 
            mapbox_style='carto-positron',
            center= {'lat':24, 'lon' :78},
            zoom=3, opacity=0.5
            )
        fig.update_layout(title_text=f'Phone Pe Transaction Details - India', geo=dict(
        showframe=False,showcoastlines=False,), margin={"r":0,"t":0,"l":0,"b":0}, hovermode='x unified')
        fig.update_geos(fitbounds='locations', visible=False, projection_type="satellite")
        fig.update_traces(marker_line_width=1)
        
    elif option == Q3:    
        State_val = st.selectbox(
            'Select State :',
            ('Tamil Nadu', 'Kerala', 'Maharastra', 'Orissa')
        )
        st.write('You selected:', State_val) 
            
        if State_val == 'Tamil Nadu':
            dtls = pd.read_csv("Dist_data_with_distID_TN.csv")
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response) 
                features = dist_gj['features'][1]['properties']['NAME_2']
                id_2 = dist_gj['features'][1]['properties']['ID_2']
                state_name = dist_gj['features'][1]['properties']['NAME_1']
        elif State_val == 'Kerala':
            dtls = pd.read_csv("Dist_data_with_distID_KL.csv")
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response) 
        elif State_val == 'Maharastra':
            dtls = pd.read_csv("Dist_data_with_distID_MH.csv")
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response) 
        else: 
            dtls = pd.read_csv("Dist_data_with_distID_OR.csv")
            with open("india_district.geojson") as response:
                dist_gj = geojson.load(response)    
             
        fig = px.choropleth(
            dtls,
            geojson= dist_gj,
            featureidkey='properties.ID_2',
            locations='ID_2',
            color='Tot_No_of_Trans', 
            color_continuous_scale="ylgnbu",
            scope='asia',
            hover_name='District_name',
            hover_data='Tot_Trans_val',
            title= 'State_val'
            )
        fig.update_layout(title_text=f'District-Wise Transaction Details for : {State_val}',geo=dict(
        showframe=False,showcoastlines=False,), 
        margin={"r":0,"t":50,"l":0,"b":0}  # Adjust margins to fit the title nicely
        )
        fig.update_geos(fitbounds="locations", visible=False )   #, projection_type="satellite")
        fig.update_traces(marker_line_width=1)
        
    elif option == Q4:       
        with open("india_district.geojson") as response:
            dist_gj = geojson.load(response)
        
        dtls = pd.read_csv("Top_users_st_dist.csv")
        fig = px.choropleth_mapbox(
        dtls,
        geojson=dist_gj,
        featureidkey='properties.ID_2',
        locations='ID_2', 
        color='Total Reg Users',
        hover_name='District_name',
        color_continuous_scale="ylgnbu",
        mapbox_style='carto-positron',
        center= {'lat':24, 'lon' :78},
        zoom=3, opacity=0.75
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_traces(marker_line_width=1)
    else:    
        curr.execute("select State, sum(Tot_No_of_Insur), sum(Tot_Insur_value) from phonepe.map_st_insur group by State") 
        dtls = curr.fetchall()
        df = pd.DataFrame(dtls, columns= ['States', 'Total No of Insurance','Total Insurance Value'])
        
        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='States', 
            color='Total No of Insurance',
            hover_name='States',
            hover_data='Total Insurance Value',
            color_continuous_scale="ylgnbu", 
            )
        fig.update_layout(title_text=f'Phone Pe Transaction Details - India', geo=dict(
        showframe=False,showcoastlines=False,), width=1500, height=500, margin={"r":0,"t":0,"l":0,"b":0}, hovermode='x unified')
        fig.update_geos(fitbounds='locations', visible=False)
        fig.update_traces(marker_line_width=1)
          
st.plotly_chart(fig,use_container_width=False) 
#fig.show() 

#-----------------------------------------------------------------------------------------------------#
## Code st.toggle key and drop down columns in Streamlit page      
##-----------------------------------------------------------------------------------------------------#

on = st.toggle(label='View Districtwise', label_visibility= 'visible',help='To switch beteen Aggregated-View and Districtwise-View')
#if option == Q3 or Q4:
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
        "Select Data : ", ('Transaction', 'User')
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
        with col2:
            State_val_top = st.selectbox(
                'Select State :', 
                ('All States','Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh',
                'Chhattisgarh','Dadra and Nagar Haveli','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh',
                'Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep','Madhya Pradesh',
                'Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab',
                'Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand',
                'West Bengal')
            )
        st.write('You selected:', State_val_top) 

#-----------------------------------------------------------------------------------------------------#
## Code st.container in Streamlit page      
#-----------------------------------------------------------------------------------------------------#
with st.container(border=True,height=400):
    if View == "Aggregated": 
        if Data == "Transaction":   
            Quater_val = selected_quarter[1]
            Agg_Tran_sql = """select State, sum(Transacion_amount), sum(Transacion_count) from phonepe.aggr_st_trans Where Quater = %s and Year = %s group by State"""
            curr.execute(Agg_Tran_sql,(Quater_val, selected_year )) 
            dtls = curr.fetchall() 
            df = pd.DataFrame(dtls, columns= ["State", "Tot_Trans_val", "Tot_No_of_Trans"])
            
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
                title='Combined Bar and Line Chart with Dots : Aggregated Transaction',
                xaxis_title='Category',
                yaxis_title='Values',
                barmode='group'
            )

            # Display the plot in Streamlit
            st.plotly_chart(fig)
            
        else:
            #curr.execute("select State, sum(No_of_reg_users), sum(Percentage_share) from phonepe.aggr_st_users group by State")
            curr.execute("select State, Brand_name, sum(No_of_reg_users), sum(Percentage_share) from phonepe.aggr_st_users group by brand_name, State")
            dtls = curr.fetchall() 
            df = pd.DataFrame(dtls, columns= ["State","Brand_name","Tot_No_of_Users", "Tot_Percent_share"])
            
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
                title='Group Chart : Brand-wise Registered Users in Each State',
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
            Quater_val = selected_quarter[1]   
            Map_Tran_sql = """select District_name, sum(Tot_No_of_Trans), sum(Tot_Trans_val) from phonepe.map_st_trans Where state = %s and Quater = %s and Year = %s group by District_name"""
            curr.execute(Map_Tran_sql, (State_val, Quater_val, selected_year)) 
            dtls = curr.fetchall() 
            df = pd.DataFrame(dtls, columns= ["District_name","Tot_No_of_Trans", "Tot_Trans_val"])
            
            # Create bar traces for each group
            trace1 = go.Bar(
                x=df['District_name'],
                y=df['Tot_No_of_Trans'],
                name='Group 1',
                marker=dict(color='rgba(55, 83, 109, 0.7)')
            )

            # Combine the traces
            data = [trace1] #, trace2]

            # Define the layout
            layout = go.Layout(
                title='Grouped Bar Chart : District-Wise Transaction',
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
                title='Grouped Bar Chart : District-Wise Transaction Value',
                xaxis=dict(title='District_name'),
                yaxis=dict(title='Transaction Value'),
                barmode='group'  # Group bars side by side
            )

            # Create the figure
            fig = go.Figure(data=data, layout=layout)

            # Display the plot in Streamlit
            st.plotly_chart(fig)
            
        else:
            
            if State_val_top == 'All States':
                curr.execute("select State, District_name, sum(Registered_users) from phonepe.top_st_users group by District_name, state")
                dtls = curr.fetchall() 
                df = pd.DataFrame(dtls, columns= ["State","District_name","Registered_users"])
                
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
            
            else: 
                Top_area_sql = """select state, pin_code, sum(area_reg_users) from phonepe.top_st_users_area where state = %s group by pin_code, state"""
                curr.execute(Top_area_sql, (State_val_top,))
                dtls = curr.fetchall() 
                df = pd.DataFrame(dtls, columns= ["State","Pin_code","Area_Reg_users"])
                #st.write(df)
                
                #Pie chart 
                fig = px.pie(df, values='Area_Reg_users', names='Pin_code', title='Pie Chart : Top 10 User Pin codes')

                # Display the plot in Streamlit
                st.plotly_chart(fig)
                
#-----------------------------------------------------------------------------------------------------#
# Close DB Connection
#-----------------------------------------------------------------------------------------------------

curr.close()
db_conn.close() 