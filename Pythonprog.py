from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os
import pandas as pd #it use to convert sql data to HTML
import mysql.connector

load_dotenv()

vault_url = os.environ["AZURE_VAULT_URL"]

secret_name = "secretpas"

# create a credential 
credentials =DefaultAzureCredential()
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