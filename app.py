from flask import Flask,jsonify,request,render_template,redirect,session,Blueprint,url_for,flash,abort
from flask_session import Session
import os,logging, hashlib,base64
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import LoginManager,current_user,UserMixin,login_required
from collections import namedtuple
from database import Database
from author import Author
from blog import Blog
from post import Post
from comment import Comment
from flask_cors import CORS
from random import sample


UPLOAD_FOLDER='uploads'
ALLOWED_EXTENSIONS={'jpg','jpeg','png','pdf'}
template_dir=os.path.abspath('templates')
app=Flask(__name__,static_url_path='/static',template_folder=template_dir,static_folder='static')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
CORS(app,supports_credentials=True,origins=['*'])
app.config['SESSION_TYPE']='filesystem'
app.config['JWT_SECRET_KEY']='whirldata@123'
Session(app)
auth=Blueprint('auth',__name__)
logging.basicConfig(level=logging.DEBUG)
# app.jinja_loader = template_loader
app.secret_key='whirldata@123'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://whirldata:Whirldata@123@localhost/blog"
db=SQLAlchemy(app)
# login_manager=LoginManager()
# login_manager.init_app(app)
# login_manager.login_view="login"




@app.route('/')
def index():
    return render_template('login.html')


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

login_manager = LoginManager(app)
login_manager.login_view = 'login'


users = {1: User(1)}

@login_manager.user_loader
def load_user(user_id):
    print("login manager")
    return users.get(int(user_id))


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
    
    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, hashed_password):
    return hash_password(input_password) == hashed_password

#renderaccountcreation
@app.route('/accountcreation', methods=['GET'])
def account_creation_page():
    return render_template('accountcreation.html')
    
#registernewuser
@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    try:
        name=data.get("name")
        email=data.get("email")
        password=data.get("password")

        existing_author = Author().get_one_by_email(email=email)

        if existing_author:
            return jsonify({"error": "Email already registered with a different account"}), 400
        hashed_pw=hash_password(password) 
        author = Author(name=name, email=email, password=hashed_pw)
        author.authenticate(email=email,password=password)  
        author.save_data()
        return jsonify({"message": "Account created successfully"})
    except Exception as e:
        return jsonify({"error":str(e)}),400


# @app.before_request
# def disable_csrf_for_register():
#     if request.path=='/register':
#         return    
    
def authenticate_user(email,password):
    db=Database()
    connection=db.connect()
    cursor=connection.cursor()
    query="SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query,(email,password))
    user=cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        user_data={
            'id':user[0],
            'email':user[1]
        }
        return user_data
    else:
        return None
                   
    
#loginrendering
@app.route('/login_land', methods=['GET'])   
def login_page():
    return render_template('login.html')               


@app.route('/login_auth', methods=['GET','POST'])
def login():
    data=request.get_json()
    try:
        email = data.get("email")
        password = data.get("password")
        user_credentials = Author().get_one_by_email(email)
        
        if user_credentials and verify_password(password,user_credentials[1]):
            session['email']=email
            name=user_credentials[1]
            session['name']=name
            return jsonify({"message": "Login successful."})
        else:
            return jsonify({"error": "Invalid credentials."}), 401 
    except Exception as e:
        logging.exception(e)
        return "An error occurred", 500



@app.route('/home_land', methods=['GET'])   
def home_page():
    return render_template('home.html')
    
@app.route('/home' , methods=['GET'])
def home():
    try:
        email=session.get('email')

        logging.debug("Session User Email: %s",email)

        if email:
            user_details = Author().get_name_from_email(email)
            name=user_details

            return render_template('home.html',username=name)
        else:
            return redirect(url_for('login_auth'))
    except Exception as e:
        logging.error("Error fetching random post:%s",e)
        return jsonify({"error":"Internal Server Error"}),500


#renderblogcreation
@app.route('/createblog', methods=['GET'])
def blog_creation_page():
    return render_template('blog.html')

#createnewblogblog
@app.route('/blog',methods=['POST'])
def create_blog():
    data=request.form()
    try:
        name=data.get("name")
        email=session.get("email")
        category=data.get("category")
        existing_blog=Blog().get_one_by_name(name)
        if existing_blog:
           return jsonify({"error": "Sorry! This Blog Name is already taken, try with a different name"}), 400
        author_id=Author().get_id_by_email(email)
        blog = Blog(name=name, email=email, category=category,author_id=author_id)
        blog.save_data()
        return jsonify({"message": "Blog created successfully"})
    except Exception as e:
        return jsonify({"error":str(e)}),500
        


@app.before_request
def disable_csrf_for_blog():
    if request.path=='/blog':
        return

@app.route('/check_blog_name')
def check_blog_name():
    blog_name = request.args.get('name')
    existing_blog = Blog().get_one_by_name(blog_name) 
    return jsonify({"Blog name exists": existing_blog is not None})




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS     

def get_current_user_id():
    if current_user.is_authenticated:
        return current_user.id
    else:
        return None
#renderpostcreation
@app.route('/createpost', methods=['GET'])
def post_creation_page():
    return render_template('post.html')

   
#createnewpost
@app.route('/post', methods=['POST'])
def post():
    data=request.form
    try:
        title=data.get("title")
        content=data.get("content")
        email=session.get("email")
        blogname=data.get("blogname")
        cover_image=request.files.get("coverImage")

        if not (title and content and email and blogname and cover_image):
            return jsonify({"error": "Incomplete data provided"}), 400
        
        blog_id=Blog().get_id_by_blogname(blogname)
        if blog_id is None:
            return jsonify({"error": "Blogname does not exist"}), 400
        
        image_data=None
        if cover_image is not None:
            image_data=base64.b64encode(cover_image.read()).decode('utf-8')
        
        post = Post(title=title, email=email, blogname=blogname, content=content, blog_id=blog_id)
        post.save_data(image_data)

        return jsonify({"message": "Post created successfully"})
    
    except Exception as e:
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

@app.route('/user-posts', methods=['GET'])
def user_posts():
    try:
        posts=Post().get_random_posts_from_database()
        print(posts)
        for post in posts:
            if 'cover_image' in post and post['cover_image'] is not None:
                post['cover_image'] = base64.b64encode(post['cover_image']).decode('utf-8')
        return jsonify(posts=posts)
    except Exception as e:
        # logging.error(f"Error fetching random posts:{e}")
        return jsonify({"error":"Internal  Server Error"}),500

@app.route('/post_details/<int:post_id>')
def post_details(post_id):
    try:
        post=Post().get_post_by_id(post_id)
        email=session.get("email")
        session['post_id']=post_id
        print('Post_id:',post_id)
        print('Session:',email)
        post=Post().get_post_by_id(post_id)
        print(post)
        session['post_id']=post_id
        print(session['post_id'])
        # if email:
        author_name=Author().get_name_from_email(email)
        print(author_name)
        existing_comments = Comment().get_comments_by_post_id_with_author(post_id)
        print(existing_comments)
        if post is None:
            abort(404)
        author_name=Author().get_name_from_email(email)
        blog_name=Blog().get_name_from_email(email)
        cover_image_blob=post.get("cover_image")
        cover_image_base64=base64.b64encode(cover_image_blob).decode('utf-8')
        return render_template('post_details.html',post=post,cover_image_base64=cover_image_base64,author_name=author_name,blog_name=blog_name)
    except Exception as e:
        # logging.error("Error fetching post details:%s",e)
        return jsonify({"error":"Internal Server Error"}),500
    
#postcomment
@app.route('/comments',methods=['POST'])
def create_comment():
    data=request.form
    try:
        print('hi')
        email=session.get("email")
        comment=data.get("comment")
        author_id=Author().get_id_by_email(email)
        post_id=session.get('post_id',None)
        print(author_id,post_id)
        comment=Comment(comment=comment,author_id=author_id,post_id=post_id)
        comment.save_data()
        return jsonify({"message":"Comment created successfully"})
    except ValueError as e:
        return jsonify({"error":str(e)}),400
    
@app.route('/comments/<int:post_id>')
def get_comments_by_post_id(post_id):
    try:
        comments = Comment().get_comments_by_post_id_with_author(post_id)
        if comments is None:
            return jsonify({"error": "No comments found for this post"}), 404
        comments_list = [{'author_name': comment.author.name, 'comment': comment.comment} for comment in comments]
        print(comments_list)
        return render_template('post_details.html',comments=comments_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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