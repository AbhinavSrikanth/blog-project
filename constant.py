DB_NAME='blog'
DB_USER='whirldata'
DB_PASSWORD='Whirldata@123'
DB_HOST='localhost'
DB_PORT='5432'

CREATE_TABLE_QUERY="""
CREATE TABLE IF NOT EXISTS your_table_name (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INTEGER
)
"""

INSERT_DATA_QUERY="""
INSERT INTO author (id,name,rating)
VALUES (%s,%s, %s)
"""

UPDATE_DATA_QUERY = """
UPDATE post
SET like_count = %s
WHERE id= %s
"""

DELETE_DATA_QUERY = """
DELETE FROM table_name
WHERE column_name = %s
"""

TRUNCATE_TABLE_QUERY = "TRUNCATE TABLE table_name"