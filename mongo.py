from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from datetime import date
from marshmallow import Schema, fields, pprint

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'cali'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cali'

mongo = PyMongo(app)


CORS(app)

class LevelingSchema(Schema):
    user = fields.Str()
    date = fields.Date()
    points = fields.Str()

@app.route('/api/levelings', methods=['GET'])
def get_all_leveling():
    levelings = mongo.db.levelings
    result = []
    for field in levelings.find():
        result.append({'_id' : str(field['_id']), 'user' : str(field['_id']), 'date': field['date'], 'points': field['points']})

    return jsonify(result)

@app.route('/api/levelings', methods=['POST'])
def add_leveling():
    levelings = mongo.db.levelings

    leveling = dict(user = request.get_json()['user'], date = date(2019, 2, 10), points = '21.25')
    
    schema = LevelingSchema()
    result = schema.dump(leveling)

    leveling_id = levelings.insert(result)
    new_leveling = levelings.find_one({'_id': leveling_id})

    result = {'result': 'Leveling registered'}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)