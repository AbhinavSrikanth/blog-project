 #Author
CREATE TABLE author (id SERIAL PRIMARY KEY, name character varying(255),email VARChar(255),hashed_password VARCHAR(255) NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

#Blog
CREATE TABLE blog (id SERIAL PRIMARY KEY, category character varying(25), author_id integer);

#Post
CREATE TABLE post (id SERIAL PRIMARY KEY, genre character varying(255), formate character varying(5), like_count integer, posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, blog_id integer);
 
 #Comment
CREATE TABLE comment (id SERIAL PRIMARY KEY, commented_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,post_id integer);
