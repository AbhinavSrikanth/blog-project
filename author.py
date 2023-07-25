from database import Database


class Author:
    def __init__(self,id,name,rating):
        self.id=id
        self.name=name
        self.rating=rating

    def save_data(self):
        db=Database()
        if db.connection:
            try:
                with db.connection.cursor() as cursor:
                    select_query="SELECT COUNT(*) FROM author WHERE id=%s"
                    cursor.execute(select_query,[self.id])
                    count=cursor.fetchone()[0]

                    if count>0:
                        raise ValueError("Author ID already exists in the table")
                    insert_query="INSERT INTO author(id,name,rating) VALUES (%s,%s,%s)"
                    cursor.execute(insert_query,[self.id,self.name,self.rating])
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

                    if "rating" in kwargs and kwargs["rating"] is not None:
                            update_query+=" rating=%s,"
                            update_values.append(kwargs["rating"])

                    if not update_values:
                        raise ValueError("Nothing to update.Please provide either 'name' or 'rating'.")
                        

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
                            'rating': author_data[2]
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
                all_authors_data=cursor.fetchall()
                return all_authors_data
            
        except Exception as e:
            print(f"Error:{e}")
            return None
        finally:
            db.close_connection()