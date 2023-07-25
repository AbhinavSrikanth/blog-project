from database import Database
class Blog:
    def __init__(self,id,name,category,author_id):
        self.id=id
        self.name=name
        self.category=category
        self.author_id=author_id

    
    def save_data(self):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query="SELECT COUNT(*) FROM blog WHERE id=%s"
                    cursor.execute(select_query,[self.id])
                    count=cursor.fetchone()[0]

                    if count>0:
                        raise ValueError("Blog ID already exists in the table")
                    insert_query="INSERT INTO blog(id,name,category,author_id) VALUES (%s,%s,%s,%s)"
                    cursor.execute(insert_query,[self.id,self.name,self.category,self.author_id])
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
    def delete(blog_id):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    delete_query="DELETE FROM blog WHERE id= %s"
                    cursor.execute(delete_query,(blog_id,))
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
                            'author_id': blog_data[3]
                        }
                        return blog_dict
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
                select_query="SELECT * FROM blog"
                cursor.execute(select_query)
                all_blogs_data=cursor.fetchall()
                return all_blogs_data
            
        except Exception as e:
            print(f"Error:{e}")
            return None
        finally:
            db.close_connection()