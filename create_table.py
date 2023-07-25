import psycopg2

try:
    conn=psycopg2.connect("dbname='blog' user='ubuntu' password='Abhinav'")
except:
    print("unable to connect to the database.")
    
cur=conn.cursor()
try:
    cur.execute("""
    CREATE TABLE trial(
        trial varchar(20),
        trial1 varchar(20)
    );
    """)
    
    conn.commit();
    
    print("table 'trial' created")
   
except:
    print("failure")
