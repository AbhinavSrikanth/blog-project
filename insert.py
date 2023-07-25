import psycopg2

try:
    conn=psycopg2.connect("dbname='blog' user='ubuntu' password='Abhinav'")
except:
    print("unable to connect to the database.")
    
cur=conn.cursor()
try:
    cur.execute("INSERT INTO trial(trial,trial1) VALUES(%s,%s)",("abhi","sri"))

    
    conn.commit();
    
    print("OK")
   
except:
    print("failure")
