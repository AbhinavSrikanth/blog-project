 #Author
CREATE TABLE author (id SERIAL PRIMARY KEY, name character varying(255), rating numeric);

#Blog
CREATE TABLE blog (id SERIAL PRIMARY KEY, name character varying(255), category character varying(15), author_id integer);

#Post
 CREATE TABLE post (id SERIAL PRIMARY KEY, genre character varying(255), formate character varying(5), like_count integer, blog_id integer);
 
 #Comment
 CREATE TABLE comment (id SERIAL PRIMARY KEY, c_type boolean, post_id integer);
