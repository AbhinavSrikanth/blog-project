from database import Database
class Post:
    def __init__(self,id,genre,formate,like_count,blog_id):
        self.id=id
        self.genre=genre
        self.formate=formate
        self.like_count=like_count
        self.blog_id=blog_id

    def save_data(self):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query="SELECT COUNT(*) FROM post WHERE id=%s"
                    cursor.execute(select_query,[self.id])
                    count=cursor.fetchone()[0]

                    if count>0:
                        raise ValueError("Post ID already exists in the table")
                    insert_query="INSERT INTO post(id,genre,formate,like_count,blog_id) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(insert_query,[self.id,self.genre,self.formate,self.like_count,self.blog_id])
                    db.connection.commit()
                    print("Post data inserted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:db.close_connection()

    def update_data(self,**kwargs):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    update_query="UPDATE post SET"
                    update_values=[]

                    if "genre" in kwargs and kwargs["genre"] is not None:
                        update_query+=" genre=%s,"
                        update_values.append(kwargs["genre"])

                    if "formate" in kwargs and kwargs["formate"] is not None:
                            update_query+=" formate=%s,"
                            update_values.append(kwargs["formate"])

                    if "like_count" in kwargs and kwargs["like_count"] is not None:
                            update_query+=" like_count=%s,"
                            update_values.append(kwargs["like_count"])

                    if not update_values:
                        raise ValueError("Nothing to update.Please provide either 'name' or 'category'.")
                        

                    update_query=update_query.rstrip(",") + " WHERE id = %s"
                    update_values.append(self.id)

                    cursor.execute(update_query,update_values)
                    db.connection.commit()
                    print("Post data updated successfully!")
            except Exception as e:
                print(f"Error:{e}")
            
            finally:
                db.close_connection()


    @staticmethod
    def delete(blog_id):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    delete_query="DELETE FROM post WHERE id= %s"
                    cursor.execute(delete_query,(blog_id,))
                    db.connection.commit()
                    print("Post data deleted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:
                    db.close_connection()
    



    @staticmethod
    def get_one(post_id):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT * FROM post WHERE id = %s"
                    cursor.execute(select_query, [post_id])
                    post_data = cursor.fetchone()

                    if post_data:
                        post_dict = {
                            'id': post_data[0],
                            'genre': post_data[1],
                            'formate': post_data[2],
                            'like_count': post_data[3],
                            'blog_id': post_data[4]
                        }
                        return post_dict
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
                select_query="SELECT * FROM post"
                cursor.execute(select_query)
                all_posts_data=cursor.fetchall()
                return all_posts_data
            
        except Exception as e:
            print(f"Error:{e}")
            return None
        finally:
            db.close_connection()