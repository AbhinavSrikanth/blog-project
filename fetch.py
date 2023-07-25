import psycopg2

try:
    conn=psycopg2.connect("dbname='blog' user='ubuntu' password='Abhinav'")
except:
    print("unable to connect to the database.")
    
cur=conn.cursor()
try:
    cur.execute("SELECT * FROM trial")
    
    print(cur.fetchone())
   
except:
    print("failure")
