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

clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Dist_Reg_users':[], 'Pin_code':[], 'Area_Reg_users':[]  }

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
            if D['data']['districts'] is not None:
                for z in D['data']['districts']:
                    Dist_name=z[1]['name']
                    print (Dist_name)
                    Dist_Reg_users=z[1]['registeredUsers']
                    print (Dist_Reg_users)
                    clm['Dist_Reg_users'].append(Dist_Reg_users)
                    clm['District_name'].append(Dist_name)
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
     District_name = row["District_name"]
     Registered_users = row["Registered_users"]
     
     print("State :" , State)
     print("Year :" , Year)
     print("Quater :" , Quater)
     print("District_name :" , District_name)
     print("Registered_users :", Registered_users)
     print  (index,"Insert iteration" ) 

     Top_users_sql = """INSERT INTO phonepe.top_st_users (State, Year, Quater, District_name, Registered_users ) VALUES ( %s, %s, %s, %s, %s)"""
     Top_users_val = (State,Year, Quater, District_name, Registered_users) 
     curr.execute(Top_users_sql, Top_users_val) 

print  ("Insert completed" ) 
db_conn.commit()
print  ("Commit completed" )
curr.close()
db_conn.close() 