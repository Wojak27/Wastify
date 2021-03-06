from flask import Flask, request, jsonify
from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_marshmallow import Marshmallow
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.ext.declarative import declarative_base
import pytest
# from flask_socketio import SocketIO, send
import os

# Init app
app = Flask(__name__)
CORS(app)
# socketio = SocketIO(app)

api = Api(app)

Base = declarative_base()

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

# Database 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

########################## SCHEMAS #######################################

# post Class/Model
# A post can also be an event if you give the lat and lgn (later addition, hence why)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(100), unique=True)
    authorFirebaseID = db.Column(db.String(200), nullable=False)
    authorEmail = db.Column(db.String(200), db.ForeignKey('user.emailAddress'), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable= False)
    #Location of the post/poster, every post has purpouse...
    lat = db.Column(db.Integer, nullable= True)
    lng = db.Column(db.Integer, nullable= True)
    timestamp = db.Column(db.Integer, nullable= False)
    timeOfTheEvent = db.Column(db.String(200), nullable= True)
    imageReference = db.Column(db.String(200), nullable= True)
    comments = db.relationship('Comment', 
                            backref='post',
                            lazy='dynamic')

    # removed the lat and lng from here, have got to remove it from the 
    # backend as well
    def __init__(self,description, authorFirebaseID, authorEmail, lat, lng, timestamp, imageReference=None, title=None, timeOfTheEvent=None):
        self.title = title
        self.description = description
        self.authorEmail = authorEmail
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp
        self.imageReference = imageReference
        self.timeOfTheEvent = timeOfTheEvent
        self.authorFirebaseID = authorFirebaseID

#################### comment Class/Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable= False)
    authorEmail = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.Integer, nullable= False)
    parentPostID = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self,description, authorEmail, timestamp, parentPostID):
        self.description = description
        self.authorEmail = authorEmail
        self.timestamp = timestamp
        self.parentPostID = parentPostID

likes = db.Table(
    'Likes',
    db.Column('user_id', db.String(200), db.ForeignKey('user.firebase_id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

# User Class/Model
class User(db.Model):

    firebase_id = db.Column(db.String(200), primary_key=True, nullable = False)
    username = db.Column(db.String(200), unique=True, nullable = False)
    emailAddress = db.Column(db.String(200), nullable = False)
    #following = db.relationship('User', backref='followe', lazy=True)
    description = db.Column(db.Text, nullable=True)
    motto = db.Column(db.Text, nullable = True)

    # Firebase image references for the user profile image and backgroud
    profileImageRef = db.Column(db.String(200), nullable = True)
    backgroundImageRef = db.Column(db.String(200), nullable = True)

    #creating the relation to the post
    posts = db.relationship('Post', 
                            backref='author',
                            lazy='dynamic')

    # Creation time of the account
    creation_time = db.Column(db.Integer, nullable = False)

    liked_posts = db.relationship('Post', secondary=likes, backref=db.backref('user_likes', lazy = 'dynamic'))
    ### This is just a test for relationships and self referal ###    

    def __init__(self,firebase_id, username, emailAddress, creation_time):
        self.firebase_id = firebase_id
        self.username = username
        self.emailAddress = emailAddress
        self.description = "Write something about yourself!"
        self.motto = "You don't have any motto!"
        self.posts = []
        self.creation_time = creation_time
        self.following = []    
        self.profileImageRef = "https://www.bsn.eu/wp-content/uploads/2016/12/user-icon-image-placeholder-300-grey.jpg"
        self.backgroundImageRef = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Shaqi_jrvej.jpg/1200px-Shaqi_jrvej.jpg"

######################### SCHEMAS ##############################
# User Schema
class UserSchema(ma.Schema):
     class Meta:
         fields = ('firebase_id', 'username', 'emailAddress', 'creation_time', 'motto', 'profileImageRef','backgroundImageRef')

# post Schema
class PostSchema(ma.Schema):
     class Meta:
         fields = ('id', 'description', 'authorFirebaseID' , 'authorEmail', 'lat', 'lng', 'timestamp', 'imageReference', 'title')
        
# comment Schema
class CommentSchema(ma.Schema):
     class Meta:
         fields = ('id', 'description', 'authorEmail', 'timestamp', 'parentPostID')

########################## THE API #######################################

# Create a post
@app.route('/post', methods=['POST'])
def add_post():
    print("Adding a new post")
    title = request.json['title']
    authorFirebaseID = request.json['authorFirebaseID']
    description = request.json['description']
    authorEmail = request.json['authorEmail']
    lat = request.json['lat']
    lng = request.json['lng']
    timestamp = request.json['timestamp']
    imageReference = request.json['imageReference']
    timeOfTheEvent = request.json['timeOfTheEvent']
    new_post = Post(description, authorFirebaseID, authorEmail, lat, lng, timestamp, imageReference, title, timeOfTheEvent)

    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post)

# Create a comment
@app.route('/add_comment/<postID>', methods=['POST'])
def add_comment(postID):
    print("Adding a new comment")
    description = request.json['description']
    authorEmail = request.json['authorEmail']
    timestamp = request.json['timestamp']
    parentPostID = request.json['parentPostID']

    # Create the comment
    new_comment = Comment(description, authorEmail, timestamp, parentPostID)

    # Get the post for the comment from ID
    post = Post.query.get(int(postID))
    post.comments.append(new_comment)
    db.session.commit()

    return comment_schema.jsonify(new_comment)

# Get selected posts. This method is adapted for the infinite scroll,
# hence the different return statements
@app.route('/latest_posts/<index>', methods=['GET'])
def get_selected_posts(index):
    post_limit = 5
    posts = Post.query.order_by(desc(Post.timestamp)).all()
    posts_count = len(posts)
    index = int(index)
    all_posts = []
    print(index)
    print(posts_count)
    if (posts_count - index) >= 5:
        # We have more than 5 posts remaining
        print("We have more than 5 posts remaining")
        all_posts = posts[index:index+post_limit]
    elif (posts_count - index) > 0:
        # We have less than 5 posts left, return the rest
        print("We have less than 5 posts left, return the rest")
        all_posts = posts[index:]  
    else:
        # If the index that we ask for is bigger than the post we have
        # just return an empty array
        print("No more posts")
    result = posts_schema.dump(all_posts)
    print(type(result.data))
    return jsonify(result.data)

# Get all posts
@app.route('/latest_posts/', methods=['GET'])
def get_posts():
    all_posts = Post.query.order_by(desc(Post.timestamp)).all()
    result = posts_schema.dump(all_posts)
    return jsonify(result.data)

# Get all comments for the posts
@app.route('/get_comments/<postID>', methods=['GET'])
def get_comments(postID):
    comments = Post.query.get(int(postID)).comments.all()
    result = comments_schema.dump(comments)
    return jsonify(result.data)

#Get one post
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    
    return post_schema.jsonify(post)

# Update a post
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    
    title = request.json['title']
    description = request.json['description']
    authorEmail = request.json['authorEmail']
    lat = request.json['lat']
    lng = request.json['lng']
    timestamp = request.json['timestamp']
    imageReference = request.json['imageReference']
    post.title = title
    post.description = description
    post.authorEmail = authorEmail
    post.lat = lat
    post.lng = lng
    post.timestamp = timestamp
    post.imageReference = imageReference

    db.session.commit()

    return post_schema.jsonify(post)
0
# Like post
@app.route('/like_post', methods=['POST'])
def like_post():
    post_id = request.json['post_id']
    user_id = request.json['user_id']
    post = Post.query.get(int(post_id))
    user = User.query.get(user_id)
    post.user_likes.append(user)

    db.session.commit()
    print("Added a like to post id: ", post_id, " and user: ", user_id)
    return str(len(post.user_likes.all()))

# Get likes 
@app.route('/get_likes/<post_id>', methods=['GET'])
def get_likes(post_id):
    post = Post.query.get(int(post_id))
    return str(len(post.user_likes.all()))

# Get comments 
@app.route('/get_comments_num/<post_id>', methods=['GET'])
def get_comments_number(post_id):
    post = Post.query.get(int(post_id))
    return str(len(post.comments.all()))

# Get number of posts
@app.route('/get_post_number/<uID>', methods=['GET'])
def get_post_number(uID):
    user = User.query.get(uID)
    print("posts: ", user.posts.all())
    return str(len(user.posts.all()))

# Delete post
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return post_schema.jsonify(post)

# Chechs if user have 
@app.route('/has_liked', methods=['GET', 'POST', 'PUT'])
def has_liked():
    post_id = request.json['post_id']
    post = Post.query.get(int(post_id))
    firebase_id = request.json['firebase_id']
    for user in post.user_likes.all():
        if user.firebase_id in firebase_id:
            return "True"
    return "False"

# Init schemas
post_schema = PostSchema(strict=True)
posts_schema = PostSchema(many=True, strict=True)

comment_schema = CommentSchema(strict=True)
comments_schema = CommentSchema(many=True, strict=True)


# Create a User
@app.route('/user/create/', methods=['POST'])
def add_User():
    print("Creating the user in the database")
    firebase_id = request.json['firebase_id']
    username = request.json['username']
    emailAddress = request.json['emailAddress']
    creation_time = request.json['creation_time']
    
    new_User = User(firebase_id, username, emailAddress, creation_time)

    db.session.add(new_User)
    db.session.commit()

    return user_schema.jsonify(new_User)

# Get all Users
@app.route('/all_users', methods=['GET'])
def get_Users():
    all_Users = User.query.all()
    result = users_schema.dump(all_Users)
    return jsonify(result.data)

#Get one User
@app.route('/user/id/<firebase_id>', methods=['GET'])
def get_User(firebase_id):
    user = User.query.get(firebase_id)
    return user_schema.jsonify(user)

#Get currently signed in User
@app.route('/current_user/<firebase_id>', methods=['GET'])
def get_signedIn_User(firebase_id):
    user = User.query.get(firebase_id)
    return user_schema.jsonify(user)

# TODO: Get all of the post in the neighbearhood (radious or something similar)

# Update a User
@app.route('/user/update_user/<firebase_id>', methods=['PUT'])
def update_User(firebase_id):
    user = User.query.get(firebase_id)
    
    username = request.json['username']
    emailAddress = request.json['emailAddress']
    creation_time = request.json['creation_time']

    user.username = username
    user.emailAddress = emailAddress
    user.creation_time = creation_time

    db.session.commit()

    return user_schema.jsonify(user)

# Update a User motto
@app.route('/user/update_user_motto/<firebase_id>', methods=['PUT'])
def update_user_motto(firebase_id):
    user = User.query.get(firebase_id)
    
    motto = request.json['motto']

    user.motto = motto

    db.session.commit()

    return user_schema.jsonify(user)

# Update a User profile image reference
@app.route('/user/update_profile_image/<firebase_id>', methods=['PUT'])
def update_user_profile_image(firebase_id):
    user = User.query.get(firebase_id)
    
    profileImageRef = request.json['profileImageRef']

    user.profileImageRef = profileImageRef

    db.session.commit()

    return user_schema.jsonify(user)

# Update a User background image reference
@app.route('/user/update_background_image/<firebase_id>', methods=['PUT'])
def update_user_background_image(firebase_id):
    user = User.query.get(firebase_id)
    
    backgroundImageRef = request.json['backgroundImageRef']

    user.backgroundImageRef = backgroundImageRef

    db.session.commit()

    return user_schema.jsonify(user)

# Delete User
@app.route('/user/delete_user/<firebase_id>', methods=['DELETE'])
def delete_User(firebase_id):
    user = User.query.get(firebase_id)
    db.session.delete(user)

    db.session.commit()

    return user_schema.jsonify(User)


# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

def testFunction(a):
    return 1

# Some reference code
@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})


# Socket for the posts
# Not working
# @socketio.on('new_post')
# def handleNewPost(post):
#     print('Post: '+ post)
#     send(post, broadcast=True)


# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    # socketio.run(app)

db.create_all()