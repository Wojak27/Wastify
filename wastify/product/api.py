from flask import Flask, request, jsonify
from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
CORS(app)

api = Api(app)

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

# Database 
path = 'postgresql:///var/run/postgresql/.s.PGSQL.5432'
print(path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:15432'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

# post Class/Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(100), unique=True)
    authorEmail = db.Column(db.String(200))
    description = db.Column(db.String(200))
    # add date, time, location, imgSrc and name 

    def __init__(self,description, authorEmail):
        self.description = description
        self.authorEmail = authorEmail

# post Schema
class PostSchema(ma.Schema):
     class Meta:
         fields = ('id', 'description', 'authorEmail')

# Create a post
@app.route('/post', methods=['POST'])
def add_post():
    description = request.json['description']
    authorEmail = request.json['authorEmail']

    new_post = Post(description, authorEmail)

    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post)

# Get all posts
@app.route('/post', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
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

    description = request.json['description']
    authorEmail = request.json['authorEmail']

    post.description = description
    post.authorEmail = authorEmail

    db.session.commit()

    return post_schema.jsonify(post)

# Delete post
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)

    db.session.commit()

    return post_schema.jsonify(post)


# Init schema
post_schema = PostSchema(strict=True)
posts_schema = PostSchema(many=True, strict=True)

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