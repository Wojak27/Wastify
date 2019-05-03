from flask import Flask, request, jsonify
from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_marshmallow import Marshmallow
from flask_wtf.file import FileField, FileAllowed
import os

# Init app
app = Flask(__name__)
CORS(app)

api = Api(app)

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

# Database 
#path = 'postgresql:///var/run/postgresql/.s.PGSQL.5432'
#print(path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:15432'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

########################## SCHEMAS #######################################

# Here all of the post followers are contained
# the user_id also works as a reference to an actual user
#class PostFollowers(db.Model):
#    id = db.Column(db.Integer, primary=True) 
#    user_id = db.Column(db.String(200), db.ForeignKey('user.firebase_id'), nullable=False)

# post Class/Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(100), unique=True)
    authorEmail = db.Column(db.String(200), db.ForeignKey('user.firebase_id'), nullable=False)
    description = db.Column(db.Text, nullable= False)
    #Location of the post/poster, every post has purpouse...
    lat = db.Column(db.Integer, nullable= True)
    lng = db.Column(db.Integer, nullable= True)
    timestamp = db.Column(db.Integer, nullable= False)
    timeOfTheEvent = db.Column(db.String(200), nullable= True)
    imageReference = db.Column(db.String(200), nullable= True)
    # add date, time, location, imgSrc and name 

    # removed the lat and lng from here, have got to remove it from the 
    # backend as well
    def __init__(self,description, authorEmail, lat, lng, timestamp, imageReference=None):
        self.description = description
        self.authorEmail = authorEmail
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp
        self.imageReference = imageReference
        

    
# post Schema
class PostSchema(ma.Schema):
     class Meta:
         fields = ('id', 'description', 'authorEmail', 'lat', 'lng', 'timestamp', 'imageReference')


# User Class/Model
class User(db.Model):
    firebase_id = db.Column(db.String(200), primary_key=True, nullable = False)
    username = db.Column(db.String(200), unique=True, nullable = False)
    emailAddress = db.Column(db.String(200), nullable = False)
    # Here we can add firends and some extra content data
    #followers = db.Column(db) # all of the followers
    #following = db.relationship('User', backref='followe', lazy=True)
    description = db.Column(db.Text, nullable=True)
    motto = db.Column(db.Text, nullable = True)
    #likedPosts = db.relationship('Post', backref='hasLiked', lazy=True, nullable = True)
    #creating the relation to the post
    posts = db.relationship('Post', backref='author', lazy=True)

    # Creation time of the account
    creation_time = db.Column(db.Integer, nullable = False)

    # add date, time, location, imgSrc and username 

    def __init__(self,firebase_id, username, emailAddress, creation_time):
        self.firebase_id = firebase_id
        self.username = username
        self.emailAddress = emailAddress
        self.creation_time = creation_time

# User Schema
class UserSchema(ma.Schema):
     class Meta:
         fields = ('firebase_id', 'username', 'emailAddress', 'creation_time')


########################## THE API #######################################

# Create a post
@app.route('/post', methods=['POST'])
def add_post():
    print("Adding a new post")
    description = request.json['description']
    authorEmail = request.json['authorEmail']
    lat = request.json['lat']
    lng = request.json['lng']
    timestamp = request.json['timestamp']
    imageReference = request.json['imageReference']

    new_post = Post(description, authorEmail, lat, lng, timestamp)

    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post)

# Get all posts
@app.route('/latest_posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.order_by(desc(Post.timestamp)).limit(20).all()
    result = posts_schema.dump(all_posts)
    return jsonify(result.data)



#Get one post
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    
    return post_schema.jsonify(post)

# get data from JSON
def getDataFromJson():
    description = request.json['description']
    authorEmail = request.json['authorEmail']
    lat = request.json['lat']
    lng = request.json['lng']
    timestamp = request.json['timestamp']
    imageReference = request.json['imageReference']
    return [description, authorEmail, lat, lng, timestamp, imageReference]

# Update a post
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    
    description = request.json['description']
    authorEmail = request.json['authorEmail']
    lat = request.json['lat']
    lng = request.json['lng']
    timestamp = request.json['timestamp']
    imageReference = request.json['imageReference']
    post.description = description
    post.authorEmail = authorEmail
    post.lat = lat
    post.lng = lng
    post.timestamp = timestamp
    post.imageReference = imageReference

    db.session.commit()

    return post_schema.jsonify(post)

# Delete post
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(firebase_id):
    post = Post.query.get(id)
    db.session.delete(post)

    db.session.commit()

    return post_schema.jsonify(post)


# Init schema
post_schema = PostSchema(strict=True)
posts_schema = PostSchema(many=True, strict=True)



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
# TODO: aa$


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

    return user_schema.jsonify(User)

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




# Some reference code
#I just want to be able to manipulate the parameters
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    print(username)
    print(password) 

@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}


# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

db.create_all()