 #Author
CREATE TABLE author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    hashed_password VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

#Blog
CREATE TABLE blog (              
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    author_id INT,
    email VARCHAR(255),
    FOREIGN KEY (author_id) REFERENCES author(id)
);


#Post
CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    like_count INT,
    blogname VARCHAR(255),
    blog_id INT REFERENCES blog(id),
    posted_at TIMESTAMP,
    title VARCHAR(255),
    email VARCHAR(255),
    content TEXT
);


 #Comment
CREATE TABLE comment (
    id SERIAL PRIMARY KEY, 
    commentedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    post_id INT REFERENCES post(id)
);
