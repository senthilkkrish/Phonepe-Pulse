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

path="C:/Users/Viney Acsa Sam/OneDrive/Desktop/Visual Studio/Phonepe Pulse/pulse/data/map/transaction/hover/country/india/state/"
Map_state_list=os.listdir(path)
Map_state_list

#----------------------------------------------------------------------------------------------------#
# #This is to extract the data's to create a dataframe
#----------------------------------------------------------------------------------------------------#

clm={'State':[], 'Year':[],'Quater':[],'District Name':[], 'Total No of Transaction':[], 'Total Transaciton value':[]}

for i in Map_state_list:
    p_i=path+i+"/"
    Map_yr=os.listdir(p_i)
    #print(Map_yr)
    #print  (i)
    for j in Map_yr:
        p_j=p_i+j+"/"
        Map_yr_list=os.listdir(p_j)
        # print(Map_yr_list)
        # print  (j)
        for k in Map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            if D['data']['hoverDataList'] is not None:
              for z in D['data']['hoverDataList']: 
                Dist_name=z['name']
                Tot_trans=z['metric'][0]['count']
                Tot_trans_val=z['metric'][0]['amount']
                clm['District Name'].append(Dist_name)
                clm['Total No of Transaction'].append(Tot_trans)
                clm['Total Transaciton value'].append(Tot_trans_val)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quater'].append(int(k.strip('.json')))
            else:
                print(k,"No data available in json.")
#Succesfully created a dataframe
Map_Trans=pd.DataFrame(clm)
#----------------------------------------------------------------------------------------------------#
# #This is to insert data from the dataframe to the database table 
#----------------------------------------------------------------------------------------------------#

for index, row in Map_Trans.iterrows():
      State = row["State"]
      Year = row["Year"]
      Quater = row["Quater"]
      Dist_name = row["District Name"]
      Tot_trans = row["Total No of Transaction"]
      Tot_trans_val = row["Total Transaciton value"]
      
      print("State :" , State)
      print("Year :" , Year)
      print("Quater :" , Quater)
      print("District Name :" , Dist_name)
      print("Total No of Transaction :", Tot_trans)
      print("Total Transaciton value :" , Tot_trans_val)
      print  (index, "Insert iteration :" ) 

      Map_trans_sql = """INSERT INTO phonepe.map_st_trans (State, Year, Quater, District_name, Tot_No_of_Trans, Tot_Trans_val ) VALUES (%s, %s, %s, %s, %s, %s)"""
      Map_trans_val = (State,Year, Quater, Dist_name, Tot_trans, Tot_trans_val) 
      curr.execute(Map_trans_sql, Map_trans_val) 

print  ("Insert completed" ) 
db_conn.commit()
print  ("Commit completed" )
curr.close()
db_conn.close() 