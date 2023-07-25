import psycopg2

try:
    conn=psycopg2.connect("dbname='blog' user='ubuntu' password='Abhinav'")
    print("connected to the database")
except:
    print("unable to connect to the database.")
