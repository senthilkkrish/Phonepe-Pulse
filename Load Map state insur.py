#-----------------------------------------------------------------------------------------------------#
# Importing required packages
#-----------------------------------------------------------------------------------------------------#

import pandas as pd
import json
import os
import mysql.connector as db

#-----------------------------------------------------------------------------------------------------#
# Define Database Connection
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
# Declare the path for data source
#-----------------------------------------------------------------------------------------------------#

path="C:/Users/Viney Acsa Sam/OneDrive/Desktop/Visual Studio/Phonepe Pulse/pulse/data/map/insurance/hover/country/india/state/"
Map_state_list=os.listdir(path)
Map_state_list

#----------------------------------------------------------------------------------------------------#
# #This is to extract the data's to create a dataframe
#----------------------------------------------------------------------------------------------------#

clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Tot_No_of_Insur':[], 'Tot_Insur_value':[]}

for i in Map_state_list:
    p_i=path+i+"/"
    Map_yr=os.listdir(p_i)
    for j in Map_yr:
        p_j=p_i+j+"/"
        Map_yr_list=os.listdir(p_j)
        for k in Map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            if D['data']['hoverDataList'] is not None:
                for z in D['data']['hoverDataList']:
                    Dist_name=z['name']
                    Tot_No_of_Insur=z['metric'][0]['count']
                    Tot_Insur_value=z['metric'][0]['amount']
                    clm['District_name'].append(Dist_name)
                    clm['Tot_No_of_Insur'].append(Tot_No_of_Insur)
                    clm['Tot_Insur_value'].append(Tot_Insur_value)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                else:
                    print(k,"No data available in json.")
#Succesfully created a dataframe
Map_Insur=pd.DataFrame(clm)

#----------------------------------------------------------------------------------------------------#
# #This is to insert data from the dataframe to the database table 
#----------------------------------------------------------------------------------------------------#

for index, row in Map_Insur.iterrows():
      State = row["State"]
      Year = row["Year"]
      Quater = row["Quater"]
      District_name = row["District_name"]
      Tot_No_of_Insur = row["Tot_No_of_Insur"]
      Tot_Insur_value = row["Tot_Insur_value"]
      
      print("State :" , State)
      print("Year :" , Year)
      print("Quater :" , Quater)
      print("District_name :" , District_name)
      print("Tot_No_of_Insur :", Tot_No_of_Insur)
      print("Tot_Insur_value :" , Tot_Insur_value)
      print  (index,"Insert iteration" ) 

      Map_Insur_sql = """INSERT INTO phonepe.map_st_insur (State, Year, Quater, District_name, Tot_No_of_Insur, Tot_Insur_value ) VALUES (%s, %s, %s, %s, %s, %s)"""
      Map_Insur_val = (State,Year, Quater, District_name, Tot_No_of_Insur, Tot_Insur_value) 
      curr.execute(Map_Insur_sql, Map_Insur_val) 

print  ("Insert completed" ) 
db_conn.commit()
print  ("Commit completed" )
curr.close()
db_conn.close() 