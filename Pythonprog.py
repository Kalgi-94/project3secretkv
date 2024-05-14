from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os
import pandas as pd #it use to convert sql data to HTML
import mysql.connector

load_dotenv()
client_id = 36a482f0-ad1d-415c-aa8e-2780a41a0c10
tenant_id = 50910f11-83a2-4159-bd1b-f0aa1521666e
client_secret =IbZ8Q~mKtZt1Yz.a9gU2M9Lk~IiaEZHAi95mqcXU
vault_url = https://keyvalueproj3.vault.azure.net/

secret_name = "dbString"

# create a credential 
credentials = ClientSecretCredential(
    client_id = client_id, 
    client_secret= client_secret,
    tenant_id= tenant_id
)
# create a secret client object
secret_client = SecretClient(vault_url= vault_url, credential= credentials)

# retrieve the secret value from key vault
secret = secret_client.get_secret(secret_name)

strvalue=secret.value

# connection string
mydb=mysql.connector.connect(host="localhost",port=3306,user="root",password=str(strvalue),database="project3db")

sql="SELECT * FROM Employee;"
mycursor=mydb.cursor()
mycursor.execute(sql)
myresult=mycursor.fetchall()

# create an html with pandas
df=pd.DataFrame()
for x in myresult:
    df2=pd.DataFrame(list(x)).T
    df=pd.concat([df,df2])

df.to_html('templates/sql-data.html')
