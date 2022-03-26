from sqlite3 import Timestamp
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
import os
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
db = SQLAlchemy(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/test')
def hello():
  return "test"

# @app.route('/hello')
# def hello():
#   return "Hello World!"

# # Item
# class Item(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(80), unique=True, nullable=False)
#   content = db.Column(db.String(120), unique=True, nullable=False)

#   def __init__(self, title, content):
#     self.title = title
#     self.content = content

#   @app.route('/items/<id>', methods=['GET'])
#   def get(id):
#     item = Item.query.get(id)
#     del item.__dict__['_sa_instance_state']
#     return jsonify(item.__dict__)

#   @app.route('/items', methods=['GET'])
#   def get_items():
#     items = []
#     for item in db.session.query(Item).all():
#       del item.__dict__['_sa_instance_state']
#       items.append(item.__dict__)
#     print(items)
#     return jsonify(items)

#   @app.route('/items', methods=['POST'])
#   def create_item():
#     body = request.get_json()
#     db.session.add(Item(body['title'], body['content']))
#     db.session.commit()
#     return "item created"

#   @app.route('/items/<id>', methods=['PUT'])
#   def update_item(id):
#     body = request.get_json()
#     db.session.query(Item).filter_by(id=id).update(
#       dict(title=body['title'], content=body['content']))
#     db.session.commit()
#     return "item updated"

#   @app.route('/items/<id>', methods=['DELETE'])
#   def delete_item(id):
#     db.session.query(Item).filter_by(id=id).delete()
#     db.session.commit()
#     return "item deleted"

# Entry
    # SpO2: float
    # HR: integer
    # updated_at: timestamp



class Entry(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  device = db.Column(db.String(80), unique=False, nullable=False)
  spo2 = db.Column(db.Float, unique=False, nullable=True)
  hr = db.Column(db.Float, unique=False, nullable=True)
  timestamp = db.Column(db.DateTime, unique=True, nullable=False)

  def __init__(self, device, spo2, hr, timestamp):
    self.device = device
    self.spo2 = spo2
    self.hr = hr
    self.timestamp = timestamp

  @app.route('/items/<id>', methods=['GET'])
  def get(id):
    item = Entry.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)

  @app.route('/items', methods=['GET'])
  def get_items():
    items = []
    for item in db.session.query(Entry).all():
      del item.__dict__['_sa_instance_state']
      items.append(item.__dict__)
    print(items)
    return jsonify(items)

  @app.route('/items', methods=['POST'])
  def create_item():
    body = request.get_json()
    db.session.add(Entry(body['device'], body['spo2'], body['hr'], body['timestamp']))
    db.session.commit()
    return "item created"

  @app.route('/items/<id>', methods=['PUT'])
  def update_item(id):
    body = request.get_json()
    db.session.query(Entry).filter_by(id=id).update(
      dict(device = body['device'], spo2=body['spo2'], hr=body['hr'], timestamp=body['timestamp']))
    db.session.commit()
    return "item updated"

  @app.route('/items/<id>', methods=['DELETE'])
  def delete_item(id):
    db.session.query(Entry).filter_by(id=id).delete()
    db.session.commit()
    return "item deleted"

db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)