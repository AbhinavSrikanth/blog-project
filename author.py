from database import Database
import bcrypt,binascii,traceback
from datetime import datetime
from flask import url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from database import Database
db = SQLAlchemy()

class Author:
    def __init__(self,id=None,name=None,email=None,password=None,created_at=None,updated_at=None):
        self.id=id
        self.name=name
        self.email=email
        self.password=password
        self.created_at=created_at
        self.updated_at=updated_at
        

    def save_data(self):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    with db.connection:
                        select_query="SELECT COUNT(*) FROM blog WHERE id=%s"
                        cursor.execute(select_query,[self.id])
                        result=cursor.fetchone()
                        if result is None:
                            raise ValueError("Fetch result is None")
                        count = result[0]

                    if count>0:
                        raise ValueError("Author ID already exists in the table")
                    
                    current_time=datetime.now()
                    insert_query="INSERT INTO author(name,email,hashed_password,created_at,updated_at) VALUES (%s,%s,%s,%s,%s) RETURNING id"
                    cursor.execute(insert_query,[self.name,self.email,self.password,current_time,current_time])
                    author_id=cursor.fetchone()[0]
                    self.id=author_id
                    db.connection.commit()
                    print("Author data inserted successfully!")
            except Exception as e:
                error_message=f"Error:{e}\n"
                error_message+=f"Traceback:\n{traceback.format_exc()}"
                print(error_message)
            finally:
                db.close_connection()
            
    def get_credentials_by_email(self,email):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT email,hashed_password FROM author WHERE email = %s"
                    print(f"Executing query: {select_query}")
                    cursor.execute(select_query,(email,))
                    print("Query executed successfully")
            except Exception as e:
                print(f"Error: fetching credentials:{e}")
            finally:
                db.close_connection()
            
                        
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
                        self.password = kwargs["password"]
                        self.hashed_password()
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
                    cursor.execute(delete_query,[email])
                    db.connection.commit()
                    print("Author data deleted successfully!")
            except Exception as e:
                print(f"Error:{e}")
            finally:
                    db.close_connection()
    
    def get_name_from_email(self,email):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT name FROM author WHERE email = %s"
                    cursor.execute(select_query,(email,))
                    author_data = cursor.fetchone()
                    if author_data is None:
                        print("Email not found in the database.")
                    return author_data[0]
            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()

    def get_one_by_email(self,email):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT email,hashed_password FROM author WHERE email = %s"
                    cursor.execute(select_query,(email,))
                    author_data = cursor.fetchone()
                    if author_data is None:
                        print("Email not found in the database.")
                    return author_data
            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()
                
    def get_id_by_email(self,email):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT id FROM author WHERE email = %s"
                    cursor.execute(select_query,(email,))
                    author_data = cursor.fetchone()
                    if author_data is None:
                        print("Author not found in the database.")
                    return author_data
            except Exception as e:
                print(f"Error: {e}")

            finally:
                db.close_connection()
                    


    def authenticate(self, email, password):
        db = Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query = "SELECT hashed_password FROM author WHERE email=%s"
                    cursor.execute(select_query, [email])
                    user_data = cursor.fetchone()
                    if user_data:
                        hashed_password_bytes = bytes.fromhex(user_data[0][2:])
                        
                        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes):
                            print("Password Match!")
                            return True
                        else:
                            print("Password Mismatch!")
                    else:
                        print("Email Not Found")
                    return False

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