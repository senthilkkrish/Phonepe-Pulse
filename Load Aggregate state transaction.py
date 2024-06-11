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

path="C:/Users/Viney Acsa Sam/OneDrive/Desktop/Visual Studio/Phonepe Pulse/pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list

#----------------------------------------------------------------------------------------------------#
# #This is to extract the data's to create a dataframe
#----------------------------------------------------------------------------------------------------#

clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']: 
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Transacion_type'].append(Name)
              clm['Transacion_count'].append(count)
              clm['Transacion_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Trans=pd.DataFrame(clm)

#----------------------------------------------------------------------------------------------------#
# #This is to insert data from the dataframe to the database table 
#----------------------------------------------------------------------------------------------------#

for index, row in Agg_Trans.iterrows():
      State = row["State"]
      Year = row["Year"]
      Quater = row["Quater"]
      Trans_typ = row["Transacion_type"]
      Trans_cnt = row["Transacion_count"]
      Trans_amt = row["Transacion_amount"]
      
      print("State :" , row["State"])
      print("Year :" , row["Year"])
      print("Quater :" , row["Quater"])
      print("Transacion_type :" , row["Transacion_type"])
      print("Transacion_count :", row["Transacion_count"])
      print("Transacion_amount :" ,row["Transacion_amount"])
      print  ("Insert iteration :" ) 

      Agrr_trans_sql = """INSERT INTO phonepe.aggr_st_trans (State, Year, Quater, Transacion_type, Transacion_count, Transacion_amount ) VALUES (%s, %s, %s, %s, %s, %s)"""
      Agrr_trans_val = (State,Year, Quater, Trans_typ, Trans_cnt, Trans_amt) 
      curr.execute(Agrr_trans_sql, Agrr_trans_val) 

print  ("Insert completed" ) 
db_conn.commit()
print  ("Commit completed" )
curr.close()
db_conn.close() 