from database import Database
class Post:
    def __init__(self,id=None,like_count=None,blogname=None,blog_id=None,posted_at=None,title=None,email=None,content=None):
        self.id=id
        self.like_count=like_count
        self.posted_at=posted_at
        self.blogname=blogname
        self.title=title
        self.blog_id=blog_id
        self.content=content

    def save_data(self):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_blog_id_query = "SELECT id FROM blog WHERE name = %s;"
                    cursor.execute(select_blog_id_query, [self.blogname])
                    blog_id = cursor.fetchone()
                    if blog_id:
                        insert_query = """
                            INSERT INTO post (like_count, posted_at, title, blogname, content)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING id;
                        """
                        cursor.execute(insert_query, (self.like_count, self.posted_at, self.title, self.blogname, self.content))
                        post_id = cursor.fetchone()[0]
                        self.id = post_id
                        db.connection.commit()
                        print("Post data inserted successfully!")
                    else:
                        print("Blog with the specified blogname does not exist")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                db.close_connection()

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
            
            
            
    def get_id_by_name(self,blogname):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = f"SELECT name,email,category FROM blog WHERE blogname = %s"
                    print(select_query)
                    cursor.execute(select_query,(blogname,))
                    blog_data = cursor.fetchone()
                    if blog_data is None:
                        print("Blog not found in the database.")
                    return blog_data
            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()
                
                
                