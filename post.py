from database import Database
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post:
    def __init__(self,id=None,like_count=None,email=None,blogname=None,blog_id=None,posted_at=None,title=None,content=None, cover_image=None):
        self.id=id
        self.like_count=like_count
        self.posted_at=posted_at
        self.blogname=blogname
        self.title=title
        self.email=email
        self.blog_id=blog_id
        self.content=content
        self.cover_image=cover_image

    def save_data(self,image_data):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                        current_time=datetime.now()
                        insert_query = """INSERT INTO post (title, email, blogname, content, blog_id, like_count, posted_at, cover_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
                        cursor.execute(insert_query, [
                        self.title,
                        self.email,
                        self.blogname,
                        self.content,
                        self.blog_id,
                        0,
                        current_time,
                        image_data
                    ])
                        post_id = cursor.fetchone()[0]
                        self.id = post_id
                        db.connection.commit()
                        print("Post data inserted successfully!")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                db.close_connection()



    def get_random_posts_from_database(self):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    random_post_query = "SELECT id, title, cover_image FROM post ORDER BY RANDOM() LIMIT 2"
                    cursor.execute(random_post_query)
                    random_posts = cursor.fetchall()
                    posts_data=[{"id":id,"title":title,"cover_image":cover_image} for (id,title,cover_image) in random_posts if cover_image is not None]
                    return posts_data
            except Exception as e:
                print(f"Error fetching random posts:{e}")
            finally:
                db.close_connection()

    def get_post_by_id(self,id):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    get_post_query = "SELECT title, cover_image, content FROM post WHERE id = %s;"
                    cursor.execute(get_post_query, (id,))
                    post_data = cursor.fetchone()
                    if post_data:
                        post = {
                            "title": post_data[0],
                            "cover_image": post_data[1],
                            "content": post_data[2],
                        }
                        return post
                    else:
                        return None
            except Exception as e:
                print(f"Error fetching post by id: {e}")
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
        