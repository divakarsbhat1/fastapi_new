import mysql.connector
import time
from .config_env import settings
# Database Connection

while(1):
    try:
        connection=mysql.connector.connect(host=settings.host,user=settings.user,password=settings.password,database=settings.database)
        cursor=connection.cursor()
        if cursor!=None:
            break
    except Exception as Error:
        print("Connection to Database Failed")
        print("The Error is: ",Error)
        time.sleep(2)