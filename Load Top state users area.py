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

path="C:/Users/Viney Acsa Sam/OneDrive/Desktop/Visual Studio/Phonepe Pulse/pulse/data/top/user/country/india/state/"
Top_state_list=os.listdir(path)
Top_state_list

#----------------------------------------------------------------------------------------------------#
# #This is to extract the data's to create a dataframe
#----------------------------------------------------------------------------------------------------#

clm={'State':[], 'Year':[],'Quater':[], 'Pin_code':[], 'Area_Reg_users':[]  }

for i in Top_state_list:
    p_i=path+i+"/"
    Top_yr=os.listdir(p_i)
    for j in Top_yr:
        p_j=p_i+j+"/"
        Top_yr_list=os.listdir(p_j)
        for k in Top_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            if D['data']['pincodes'] is not None:
                for z in D['data']['pincodes']:
                    Pin_code=z['name']
                    print (Pin_code)
                    Area_Reg_users=z['registeredUsers']
                    print (Area_Reg_users)
                    clm['Pin_code'].append(Pin_code)
                    clm['Area_Reg_users'].append(Area_Reg_users)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
            else:
                print(k,"No data available in json.")
#Succesfully created a dataframe
Top_Users=pd.DataFrame(clm)

#----------------------------------------------------------------------------------------------------#
# #This is to insert data from the dataframe to the database table 
#----------------------------------------------------------------------------------------------------#

for index, row in Top_Users.iterrows():
     State = row["State"]
     Year = row["Year"]
     Quater = row["Quater"]
     Pin_code = row["Pin_code"]
     Area_Reg_users = row["Area_Reg_users"]
     
     print("State :" , State)
     print("Year :" , Year)
     print("Quater :" , Quater)
     print("Pin_code :" , Pin_code)
     print("Area_Reg_users :", Area_Reg_users)
     print  (index,"Insert iteration" ) 

     Top_users_sql = """INSERT INTO phonepe.top_st_users_area (State, Year, Quater, Pin_code, Area_Reg_users ) VALUES ( %s, %s, %s, %s, %s)"""
     Top_users_val = (State,Year, Quater, Pin_code, Area_Reg_users) 
     curr.execute(Top_users_sql, Top_users_val) 

print  ("Insert completed" ) 
db_conn.commit()
print  ("Commit completed" )
curr.close()
db_conn.close() 