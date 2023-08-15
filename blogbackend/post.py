from database import Database
class Post:
    def __init__(self,id,file_type,file_path,like_count,posted_at,comments,post_title,blog_id,text_content):
        self.id=id
        self.file_path=file_path
        self.file_type=file_type
        self.like_count=like_count
        self.blog_id=blog_id
        self.posted_at=posted_at
        self.comments=comments
        self.post_title=post_title
        self.text_content=text_content

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
                    insert_query="INSERT INTO post(id,file_type,file_path,like_count,blog_id,posted_at,comments,text_content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(insert_query,[self.id,self.file_type,self.file_path,self.like_count,self.blog_id,self.posted_at,self.comments,self.text_content])
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
                            'like_count': post_data[1],
                            'posted_at':post_data[2],
                            'blog_id': post_data[3],
                            'comments':post_data[4],
                            'post_title':post_data[5],
                            'text_content':post_data[6],
                            'file_type':post_data[7],
                            'file_path':post_data[8]
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