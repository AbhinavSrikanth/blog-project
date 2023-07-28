from database import Database
from constant import UPDATE_DATA_QUERY

if __name__=="__main__":
    try:
        db=Database()
        post_id=1004
        new_like_count=858

        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    cursor.execute(UPDATE_DATA_QUERY,(new_like_count,post_id))
                    db.connection.commit()
                    print("Query executed successfully")
            except Exception as e:
                print(f"Error:{e}")
    except Exception as e:
        print(f"Error:{e}")