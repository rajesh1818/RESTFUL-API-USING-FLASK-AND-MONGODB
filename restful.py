from pymongo import MongoClient
from flask import Flask
from flask import jsonify, make_response
import jwt
import datetime
from flask_restful import Api, Resource, reqparse, abort
from flask_restful import request
from pymongo import MongoClient
from functools import wraps




app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"]= "thisissecretkey"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token= request.args.get("token")
        if  not token:
            return jsonify({"message": "token is missing!!!!!"}), 403
        try:
            data= jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "token is invalid"}), 403

        return f(*args, **kwargs)
    return decorated




uri = "mongodb+srv://<USERNAME>:<PASSWORD>@imdb.8hily.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(uri)
db= client.list_database_names()
imdb = client.imdb
myuser = imdb.user.find_one({}, {"_id": 0})
print(myuser)

class login(Resource):
    def post(self):
        auth = request.get_json()
        user = imdb.user.find_one({'name': auth['name']}, {"_id": 0 })
        print('user')
        print(user)
        if auth and auth['password'] == user["password"]:
            token = jwt.encode({"user":auth['name'], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config["SECRET_KEY"])
            return jsonify({"token": token})
        return make_response("could not verify!!!!!!!!!!!!")
class getmovie(Resource):
    def get(self):
        mymovies = imdb.movies.find_one({}, {"_id": 0})
        return jsonify(movies=mymovies)


class getuser(Resource):
    def get(self):
        user = imdb.user.find_one({}, {"_id": 0})
        return jsonify(user=user)


class searchbyname(Resource):
    def get(self, moviename):
        mymovies = imdb.movies.find_one({"name": moviename}, {"_id": 0})
        return mymovies

class userbyname(Resource):
    def get(self, username):
        user = imdb.user.find_one({"name": username}, {"_id": 0})
        return user


class add(Resource):
    def post(self):
        data = request.get_json()
        imdb.movies.insert_one(data)
        return jsonify({'message': 'registered successfully'})

class adduser(Resource):
    def post(self):
        data = request.get_json()
        imdb.user.insert_one(data)
        return jsonify({'message': 'User Added successfully'})

class delete(Resource):
    def post(self):
        data = request.get_json()
        imdb.movies.delete_one(data)
        return jsonify({'message': 'deleted successfully'})

class deleteuser(Resource):
    def post(self):
        data = request.get_json()
        imdb.user.delete_one(data)
        return jsonify({'message': 'User deleted successfully'})

class update(Resource):
    def post(self, moviename):
        data = request.get_json()
        updatedMovie = data['name']
        imdb.movies.update_one({"name":moviename}, {"$set": {"name": updatedMovie}})
        return jsonify({'message': 'updated successfully'})

class updateuser(Resource):
    def post(self, username):
        data = request.get_json()
        updateduser = data['name']
        imdb.user.update_one({"name":username}, {"$set": {"name": updateduser}})
        return jsonify({'message': 'updated successfully'})



api.add_resource(getmovie, '/a')
api.add_resource(getuser, '/u')
api.add_resource(searchbyname,"/a/<moviename>")
api.add_resource(userbyname,"/u/<username>")
api.add_resource(add,"/add")
api.add_resource(adduser,"/adduser")
api.add_resource(delete,"/delete")
api.add_resource(deleteuser,"/deleteuser")
api.add_resource(updateuser,"/updateuser/<username>")
api.add_resource(login, '/login')

if __name__ == '__main__':
    app.run(debug=True)

