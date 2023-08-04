from database import Database
import bcrypt
from datetime import datetime
from flask import url_for,redirect


class Author:
    def __init__(self,id=None,name=None,email=None,password=None):
        self.id=id
        self.name=name
        self.email=email
        self.password=password

        
                
    def hash_password(self):
        if isinstance(self.password,bytes):
            self.password=self.password.decode('utf-8')
        salt=bcrypt.gensalt()
        self.password=bcrypt.hashpw(self.password.encode('utf-8'),salt)

    
    
    def save_data(self):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    with db.connection:
                        select_query="SELECT COUNT(*) FROM author WHERE id=%s"
                        cursor.execute(select_query,[self.id])
                        count=cursor.fetchone()[0]

                    if count>0:
                        raise ValueError("Author ID already exists in the table")
                    
                    self.hash_password()
                    current_time=datetime.now()
                    insert_query="INSERT INTO author(name,email,hashed_password,created_at,updated_at) VALUES (%s,%s,%s,%s,%s) RETURNING id"
                    cursor.execute(insert_query,[self.name,self.email,self.password,current_time,current_time])
                    author_id=cursor.fetchone()[0]
                    self.id=author_id
                    db.connection.commit()
                    print("Author data inserted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:db.close_connection()

    def update_data(self,**kwargs):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    update_query="UPDATE author SET"
                    update_values=[]

                    if "name" in kwargs and kwargs["name"] is not None:
                        update_query+=" name=%s,"
                        update_values.append(kwargs["name"])

                    if "email" in kwargs and kwargs["email"] is not None:
                            update_query+=" email=%s,"
                            update_values.append(kwargs["email"])
                            
                    if "password" in kwargs and kwargs["password"] is not None:
                        self.assword = kwargs["password"]
                        self.hash_password()
                        update_query += " hashed_password=%s,"
                        update_values.append(self.password)
                        
                    if not update_values:
                        raise ValueError("Nothing to update.Please provide valid update parameters.")
                        

                    update_query=update_query.rstrip(",") + " WHERE id = %s"
                    update_values.append(self.id)

                    cursor.execute(update_query,update_values)
                    db.connection.commit()
                    print("Author data updated successfully!")
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
                    delete_query="DELETE FROM author WHERE email= %s"
                    cursor.execute(delete_query,(email,))
                    db.connection.commit()
                    print("Author data deleted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:
                    db.close_connection()
    

    @staticmethod
    def get_one_by_email(email):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = f"SELECT id,name,email,hashed_password,created_at,updated_at FROM author WHERE email = '{email}'"
                    print(select_query)
                    cursor.execute(select_query)
                    author_data = cursor.fetchone()
                    print("Author data => ", author_data)
                    return author_data
            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()
                
                
                
    @staticmethod
    def get_one(author_id):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT * FROM author WHERE id = %s"
                    cursor.execute(select_query, [author_id])
                    author_data = cursor.fetchone()

                    if author_data:
                        author_dict = {
                            'id': author_data[0],
                            'name': author_data[1],
                            'email': author_data[2],
                            'created_at':author_data[3],
                            'updated_at':author_data[4]
                        }
                        return author_dict
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
                select_query="SELECT * FROM author"
                cursor.execute(select_query)
                all_authors_data=[{
                            'id': author_data[0],
                            'name': author_data[1],
                            'email': author_data[2],
                            'created_at':author_data[3],
                            'updated_at':author_data[4]
                        }
                        for author_data in cursor.fetchall()
                    ]
                return all_authors_data
            
            
    
            
        except Exception as e:
            print(f"Error:{e}")
            return None
        finally:
            db.close_connection()