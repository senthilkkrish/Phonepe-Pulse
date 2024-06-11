#-----------------------------------------------------------------------------------------------------#
# Importing required packages
#-----------------------------------------------------------------------------------------------------

import pandas as pd
import json
import os
import mysql.connector as db

#-----------------------------------------------------------------------------------------------------#
# Define Database Connection
#-----------------------------------------------------------------------------------------------------

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
import os
path="C:/Users/Viney Acsa Sam/OneDrive/Desktop/Visual Studio/Phonepe Pulse/pulse/data/aggregated/user/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list

#----------------------------------------------------------------------------------------------------#
# #This is to extract the data's to create a dataframe
#----------------------------------------------------------------------------------------------------#

clm={'State':[], 'Year':[],'Quater':[],'Brand_name':[], 'No_of_registered_users':[], 'Percentage_of_share':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    #print(Agg_yr)
    #print  (i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
       # print(Agg_yr_list)
       # print  (j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            if D['data']['usersByDevice'] is not None:
               # print  (k)
                for z in D['data']['usersByDevice']:
                    brand_name=z['brand']
                    No_reg_users=z['count']
                    per_share=z['percentage']
                  #  print (brand_name)
                  #  print (No_reg_users)
                  #  print (per_share)
                    clm['Brand_name'].append(brand_name)
                    clm['No_of_registered_users'].append(No_reg_users)
                    clm['Percentage_of_share'].append(per_share)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                else:
                    print(k,"No data available in json.")
#Succesfully created a dataframe
Agg_Users=pd.DataFrame(clm)

#----------------------------------------------------------------------------------------------------#
# #This is to insert data from the dataframe to the database table 
#----------------------------------------------------------------------------------------------------#

for index, row in Agg_Users.iterrows():
      State = row["State"]
      Year = row["Year"]
      Quater = row["Quater"]
      brand_name = row["Brand_name"]
      No_reg_users = row["No_of_registered_users"]
      per_share = row["Percentage_of_share"]
      
      print("State :" , State)
      print("Year :" , Year)
      print("Quater :" , Quater)
      print("Brand_name :" , brand_name)
      print("No_of_registered_users :", No_reg_users)
      print("Percentage_of_share :" ,per_share)
      print  (index,"Insert iteration" ) 

      Agrr_users_sql = """INSERT INTO phonepe.aggr_st_users (State, Year, Quater, Brand_name, No_of_reg_users, Percentage_share ) VALUES (%s, %s, %s, %s, %s, %s)"""
      Agrr_users_val = (State,Year, Quater, brand_name, No_reg_users, per_share) 
      curr.execute(Agrr_users_sql, Agrr_users_val) 

print  ("Insert completed" ) 
db_conn.commit()
print  ("Commit completed" )
curr.close()
db_conn.close() 