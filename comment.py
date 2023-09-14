from flask_sqlalchemy import SQLAlchemy
from database import Database
from datetime import datetime
db = SQLAlchemy()

class Comment:
    def __init__(self,id=None,commentedat=None,post_id=None,author_id=None,comment=None):
        self.id=id
        self.commentedat=commentedat
        self.post_id=post_id
        self.comment=comment
        self.author_id=author_id


    def save_data(self):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    current_time=datetime.now()
                    print(f"post_id: {self.post_id}")
                    print(f"comment: {self.comment}")
                    insert_query="INSERT INTO comment(commentedat,post_id,author_id,comment) VALUES (%s,%s,%s,%s) RETURNING id"
                    cursor.execute(insert_query,[
                        current_time,
                        self.post_id,
                        self.author_id,
                        self.comment
                    ])
                    print()
                    comment_id=cursor.fetchone()[0]
                    self.id=comment_id
                    db.connection.commit()
                    print("Comment data inserted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:db.close_connection()



    def update_data(self,**kwargs):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    update_query="UPDATE comment SET"
                    update_values={}

                    if "c_type" in kwargs and kwargs["c_type"] is not None:
                        update_query+=" c_type=%(c_type)s,"
                        update_values["c_type"]=kwargs["c_type"]

                    if "post_id" in kwargs and kwargs["post_id"] is not None:
                            update_query+=" post_id=%(post_id)s,"
                            update_values["post_id"]=kwargs["post_id"]


                    if not update_values:
                        raise ValueError("Nothing to update.Please provide either 'c_type' or 'post_id'.")
                        

                    update_query=update_query.rstrip(",") + " WHERE id = %(id)s"
                    update_values["id"]=self.id

                    cursor.execute(update_query,update_values)
                    db.connection.commit()
                    print("Comment data updated successfully!")
            except Exception as e:
                print(f"Error:{e}")
            
            finally:
                db.close_connection()


    @staticmethod
    def delete(post_id):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    delete_query="DELETE FROM comment WHERE id= %s"
                    cursor.execute(delete_query,(post_id,))
                    db.connection.commit()
                    print("Comment data deleted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:
                    db.close_connection()
    



    @staticmethod
    def get_one(comment_id):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT * FROM comment WHERE id = %s"
                    cursor.execute(select_query, [comment_id])
                    comment_data = cursor.fetchone()

                    if comment_data:
                        comment_dict = {
                            'id': comment_data[0],
                            'c_type':comment_data[1],
                            'post_id': comment_data[2]
                        }
                        return comment_dict
                    else:
                        return None

            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()

    @staticmethod
    def get_all():
        db=Database()
        try:
            with db.connection.cursor() as cursor:
                select_query="SELECT * FROM comment"
                cursor.execute(select_query)
                all_posts_data=cursor.fetchall()
                return all_posts_data
            
        except Exception as e:
            print(f"Error:{e}")
            return None
        finally:
            db.close_connection()
            
    def get_comments_by_post_id(self,post_id):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    print('Entered comment fetching function')
                    select_query="SELECT comment FROM comment WHERE post_id = %s"
                    cursor.execute(select_query,(post_id,))
                    comment_data=cursor.fetchall()
                    if comment_data is None:
                        print("Be the first to comment on this topic.")
                    return comment_data
            except Exception as e:
                print(f"Error:{e}")
                
                
        def get_commentid_by_post_id(self,post_id):
            db=Database()
            if db.connection:
                try:
                    with db.connection.cursor() as cursor:
                        print('Entered comment fetching function')
                        select_query="SELECT id FROM comment WHERE post_id = %s"
                        cursor.execute(select_query,(post_id,))
                        comment_data=cursor.fetchall()
                        if comment_data is None:
                            print("Be the first to comment on this topic.")
                        return comment_data
                except Exception as e:
                    print(f"Error:{e}")