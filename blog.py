from flask_sqlalchemy import SQLAlchemy
from database import Database
db = SQLAlchemy()
class Blog:
    def __init__(self,id=None,name=None,category=None,author_id=None,email=None,):
        self.id=id
        self.name=name
        self.category=category
        self.author_id=author_id
        self.email=email
    
    
    def save_data(self):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    insert_query="""INSERT INTO blog(name,email,category,author_id) VALUES (%s,%s,%s,%s) RETURNING id;"""
                    cursor.execute(insert_query,[self.name,self.email,self.category,self.author_id])
                    blog_id=cursor.fetchone()[0]
                    self.id=blog_id
                    db.connection.commit()
                    print("Blog data inserted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:db.close_connection()


    def update_data(self,**kwargs):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    update_query="UPDATE blog SET"
                    update_values=[]

                    if "name" in kwargs and kwargs["name"] is not None:
                        update_query+=" name=%s,"
                        update_values.append(kwargs["name"])

                    if "category" in kwargs and kwargs["category"] is not None:
                            update_query+=" category=%s,"
                            update_values.append(kwargs["category"])

                    if not update_values:
                        raise ValueError("Nothing to update.Please provide either 'name' or 'category'.")
                        

                    update_query=update_query.rstrip(",") + " WHERE id = %s"
                    update_values.append(self.id)

                    cursor.execute(update_query,update_values)
                    db.connection.commit()
                    print("Blog data updated successfully!")
            except Exception as e:
                print(f"Error:{e}")
            
            finally:
                db.close_connection()


    @staticmethod
    def delete(email):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    delete_query="DELETE FROM blog WHERE email= %s"
                    cursor.execute(delete_query,(email,))
                    db.connection.commit()
                    print("Blog data deleted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:
                    db.close_connection()
    



    @staticmethod
    def get_one(blog_id):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT * FROM blog WHERE id = %s"
                    cursor.execute(select_query, [blog_id])
                    blog_data = cursor.fetchone()

                    if blog_data:
                        blog_dict = {
                            'id': blog_data[0],
                            'name': blog_data[1],
                            'category': blog_data[2],
                            'author_id': blog_data[3],
                            'email':blog_data[4]
                        }
                        return blog_dict
                    else:
                        return None

            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()
                


    def get_id_by_blogname(self,name):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT id FROM blog WHERE name = %s"
                    cursor.execute(select_query,(name,))
                    print(select_query)
                    blog_data = cursor.fetchone()
                    if blog_data is None:
                        print("Blog not found in the database.")
                    return blog_data[0]
            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()
                
    def get_name_from_email(self,email):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT name FROM blog WHERE email = %s"
                    cursor.execute(select_query,(email,))
                    author_data = cursor.fetchone()
                    if author_data is None:
                        print("Blog not found in the database.")
                    return author_data[0]
            except Exception as e:
                print(f"Error: {e}")
                
                
    @staticmethod
    def get_all():
        db=Database()
        try:
            with db.connection.cursor() as cursor:
                select_query="SELECT * FROM blog"
                cursor.execute(select_query)
                all_blogs_data=cursor.fetchall()
                return all_blogs_data
            
        except Exception as e:
            print(f"Error:{e}")
            return None
        finally:
            db.close_connection()
            
            
    def get_one_by_name(self, email):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT * FROM blog WHERE name = %s"
                    cursor.execute(select_query, (email,))
                    blog_data = cursor.fetchone()
                    if blog_data is None:
                        print("Blog not found in the database.")
                    return blog_data  # This line should be part of the try block
            except Exception as e:
                print(f"Error: {e}")
            finally:
                db.close_connection()
