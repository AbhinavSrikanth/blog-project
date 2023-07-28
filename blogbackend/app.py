from flask import Flask,jsonify,request,render_template
import bcrypt
import hashlib
from author import Author
from blog import Blog
from post import Post
from comment import Comment

app=Flask(__name__)

#getoneauthor
@app.route('/author/<int:id>', methods=['GET'])
def get_author(id):
    author_id = id
    print("Author Id is present in the request", author_id)
    author_data = Author.get_one(author_id)
    if author_data:
        return jsonify(author_data)
    else:
        return jsonify({"message": "Author not found."}), 404


#getallauthors
@app.route('/author',methods=['GET'])   
def get_all_authors():
        all_authors_data=Author.get_all()
        if all_authors_data:
            return jsonify(all_authors_data)
        else:
            return jsonify({"message":"No authors found"}),404

#postauthor
@app.route('/author',methods=['POST'])
def create_author():
    data=request.get_json()
    try:
        author=Author(data.get("id"),data.get("name"),data.get("email"),data.get("created_at"),data.get("updated_at"))
        author.save_data()
        return jsonify({"message":"Author created successfully"})
    except ValueError as e:
        return jsonify({"error":str(e)}),400
        
#putauthor
@app.route('/author/<id>',methods=['PUT'])
def update_author(id):
    data=request.get_json()
    try:
        author=Author.get_one(id)
        if not author:
            return jsonify({"error": "Author not found"}), 404
        
        author_instance = Author(author["id"], author["name"], author["email"],data.get("created_at"),data.get("updated_at"))

        author_instance.update_data(**data)

        return jsonify({"message":"Author updated successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400


#deleteauthor
@app.route('/author/<id>',methods=['DELETE'])
def delete_author(id):
    try:
        author=Author.get_one(id)   
        if not author:
            return jsonify({"error":"Author not found"}),404
        Author.delete(id)

        return jsonify({"message":"Author deleted successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400
    
    
    
    
#registernewuser
@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    try:
        name=data.get("name")
        email=data.get("email")
        password=data.get("password")
        confirm_password=data.get("confirm_password")
        existing_author=Author.get_one_by_email(email)
        
        if password!=confirm_password:
            return jsonify({"error":"Password do not match"}),400
        if existing_author:
            return jsonify({"error":"Email already registered with a different account"}),400
        hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        
        author=Author(name=name,email=email,hashed_password=hashed_password)
        author.save_data()
        
        return jsonify({"message":"Account created successfully"})

    except Exception as e:
        return jsonify({"error":str(e)}),400
    
    
#getoneblog
@app.route('/blog/<id>', methods=['GET'])
def get_blog(id):
    blog_id = id
    print("Blog Id is present in the request", blog_id)
    blog_data = Blog.get_one(blog_id)
    if blog_data:
        return jsonify(blog_data)
    else:
        return jsonify({"message": "Blog not found."}), 404


#getallblogs
@app.route('/blog',methods=['GET'])   
def get_all_blogs():
        all_blogs_data=Blog.get_all()
        if all_blogs_data:
            return jsonify(all_blogs_data)
        else:
            return jsonify({"message":"No blogs found"}),404

#postblog
@app.route('/blog',methods=['POST'])
def create_blog():
    data=request.get_json()
    try:
        blog=Blog(data.get("id"),data.get("name"),data.get("category"),data.get("author_id"))
        blog.save_data()
        return jsonify({"message":"Blog created successfully"})
    except ValueError as e:
        return jsonify({"error":str(e)}),400
        
#putblog
@app.route('/blog/<id>',methods=['PUT'])
def update_blog(id):
    data=request.get_json()
    try:
        blog=Blog.get_one(id)
        if not blog:
            return jsonify({"error": "Blog not found"}), 404
        
        blog_instance = Blog(blog["id"], blog["name"], blog["category"], blog["author_id"])

        blog_instance.update_data(**data)

        return jsonify({"message":"Blog updated successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400


#deleteblog
@app.route('/blog/<id>',methods=['DELETE'])
def delete_blog(id):
    try:
        blog=Blog.get_one(id)   
        if not blog:
            return jsonify({"error":"blog not found"}),404
        Blog.delete(id)

        return jsonify({"message":"blog deleted successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400






#getonepost
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post_id = id
    print("Post Id is present in the request", post_id)
    post_data = Post.get_one(post_id)
    if post_data:
        return jsonify(post_data)
    else:
        return jsonify({"message": "Post not found."}), 404


#getallposts
@app.route('/post',methods=['GET'])   
def get_all_posts():
        all_posts_data=Post.get_all()
        if all_posts_data:
            return jsonify(all_posts_data)
        else:
            return jsonify({"message":"No blogs found"}),404

#postpost
@app.route('/post',methods=['POST'])
def create_post():
    data=request.get_json()
    try:
        post=Post(data.get("id"),data.get("genre"),data.get("formate"),data.get("like_count"),data.get("blog_id"))
        post.save_data()
        return jsonify({"message":"Post created successfully"})
    except ValueError as e:
        return jsonify({"error":str(e)}),400
        
#putpost
@app.route('/post/<id>',methods=['PUT'])
def update_post(id):
    data=request.get_json()
    try:
        post=Post.get_one(id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        post_instance = Post(post["id"], post["genre"], post["formate"], post["like_count"],post["blog_id"])

        post_instance.update_data(**data)

        return jsonify({"message":"Post updated successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400


#deletepost
@app.route('/post/<id>',methods=['DELETE'])
def delete_post(id):
    try:
        post=Post.get_one(id)   
        if not post:
            return jsonify({"error":"post not found"}),404
        Post.delete(id)

        return jsonify({"message":"post deleted successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400






#getonecomment
@app.route('/comment/<id>', methods=['GET'])
def get_comment(id):
    comment_id = id
    print("Comment Id is present in the request", comment_id)
    comment_data = Comment.get_one(comment_id)
    if comment_data:
        return jsonify(comment_data)
    else:
        return jsonify({"message": "Blog not found."}), 404


#getallcomments
@app.route('/comment',methods=['GET'])   
def get_all_comments():
        all_comments_data=Comment.get_all()
        if all_comments_data:
            return jsonify(all_comments_data)
        else:
            return jsonify({"message":"No comments found"}),404

#postcomment
@app.route('/comment',methods=['POST'])
def create_comment():
    data=request.get_json()
    try:
        blog=Comment(data.get("id"),data.get("c_type"),data.get("post_id"))
        blog.save_data()
        return jsonify({"message":"Comment created successfully"})
    except ValueError as e:
        return jsonify({"error":str(e)}),400
        
#putcomment
@app.route('/comment/<id>',methods=['PUT'])
def update_comment(id):
    data=request.get_json()
    try:
        comment=Comment.get_one(id)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        comment_instance = Comment(comment["id"], comment["c_type"], comment["post_id"])

        comment_instance.update_data(**data)

        return jsonify({"message":"Comment updated successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400


#deletecomment
@app.route('/comment/<id>',methods=['DELETE'])
def delete_comment(id):
    try:
        comment=Comment.get_one(id)   
        if not comment:
            return jsonify({"error":"comment not found"}),404
        Comment.delete(id)

        return jsonify({"message":"comment deleted successfully"})
    
    except Exception as e:
        return jsonify({"error":str(e)}),400

if __name__=='__main__':
    app.run(debug=True)