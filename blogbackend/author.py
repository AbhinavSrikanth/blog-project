from database import Database
import bcrypt
from datetime import datetime


class Author:
    def __init__(self,id,name,email,hashed_password,confirm_password):
        self.id=id
        self.name=name
        self.hashed_password=hashed_password
        self.email=email
        self.confirm_password=confirm_password
        
                
    def hash_password(self):
        self.hashed_password=bcrypt.hashpw(self.hashed_password.encode('utf-8'),bcrypt.gensalt())
    
    
    def save_data(self):
        db=Database()
        if db.connection:
            try:
                self.hash_password()
                with db.connection.cursor() as cursor:
                    select_query="SELECT COUNT(*) FROM author WHERE id=%s"
                    cursor.execute(select_query,[self.id])
                    count=cursor.fetchone()[0]

                    if count>0:
                        raise ValueError("Author ID already exists in the table")
                    insert_query="INSERT INTO author(name,email,hashed_password,created_at,updated_at) VALUES (%s,%s,%s,%s,%s) RETURNING id"
                    cursor.execute(insert_query,[self.name,self.email,self.hashed_password,current_time,current_time])
                    current_time=datetime.now()
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
                            
                    if "hashed_password" in kwargs and kwargs["hashed_password"] is not None:
                        self.hashed_password = kwargs["hashed_password"]
                        self.hash_password()
                        update_query += " hashed_password=%s,"
                        update_values.append(self.hashed_password)
                        
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
    def delete(author_id):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    delete_query="DELETE FROM author WHERE id= %s"
                    cursor.execute(delete_query,(author_id,))
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
                    select_query = "SELECT id,name,email,created_at,updated_at FROM author WHERE email = %s"
                    cursor.execute(select_query, [email])
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