from flask import Flask, abort, request, jsonify
import pymongo


app = Flask(__name__)
app.config.from_object('app.config.Config')

conn = pymongo.MongoClient(host=app.config.get("MONGO_HOST"), port=app.config.get("MONGO_PORT"))
conn.db.event_coll.create_index('type')


@app.route('/v1/start', methods=['POST'])
def start():
    doc = request.get_json(force=True)
    if not doc.get("type"):
        abort(400)

    if conn.db.event_coll.find_one({"$and": [{"type": doc.get("type")}, {"state": 0}]}):
        return jsonify({"message": "Created success!"})

    doc.update({"state": 0})
    result = conn.db.event_coll.insert_one(doc)
    if not result.inserted_id:
        return abort(503)

    return jsonify({"message": "Created success!"})


@app.route('/v1/finish', methods=['POST'])
def finish():
    event = request.get_json(force=True)
    if not event.get("type"):
        abort(400)

    obj = conn.db.event_coll.update_one({"type": event.get("type")}, {'$set': {'state': 1}})

    if obj.modified_count != 1:
        return abort(503)

    return jsonify({"message": "Finished success!"})