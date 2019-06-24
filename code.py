from stravalib.client import Client
import mysql.connector
from datetime import datetime

client = Client()
code = '' #Code obtained after authorization
client_id = 12345 #Client ID
client_secret = '' #Client secret

access_token = client.exchange_code_for_token(client_id=client_id,
                        client_secret=client_secret,
                        code=code)

client = Client(access_token=access_token)

activities = client.get_activities()

mydb = mysql.connector.connect(
    host = 'localhost',
    user = '',
    passwd = '',
    database = '',
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

list_of_id = []

for activity in activities:
    list_of_id.append(activity.id)

for _id_ in list_of_id:
    activity_current = client.get_activity(_id_)
    info = {}
    info['Activity_ID'] = _id_
    t = activity_current.start_date_local
    info['Date'] = t.strftime('%m/%d/%Y')
    info['Start_time'] = t.strftime('%H:%M')
    td = activity_current.elapsed_time.total_seconds()
    info['Elapsed_time'] = td
    info['Distance'] = activity_current.distance.__str__()
    info['Cadence'] = activity_current.average_cadence.__str__()
    info['Actvity'] = activity_current.type.__str__()
    info['Average_speed'] = activity_current.average_speed.__str__()
    #Enter the table name in the place of TableName 
    sql = "INSERT INTO TableName (Activity_ID, Date, Start_time, Elapsed_time, Distance, Cadence, Activity, Average_speed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (info['Activity_ID'],info['Date'],info['Start_time'],info['Elapsed_time'],info['Distance'],info['Cadence'],info['Actvity'],info['Average_speed'])
    mycursor.execute(sql, val)
    mydb.commit()

    

# ===================Authorization Code======================
    
    #VERY IMPORTANT AUTHORIZATION 
    # Line 1
    # from stravalib.client import Client
    # client_id = 
    # client = Client()
    # url = client.authorization_url(client_id=client_id,
    #                                redirect_uri='http://127.0.0.1:8000/authorization',
    #                                scope='view_private')
    # print(url)