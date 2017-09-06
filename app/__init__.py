from flask import Flask, abort, request, jsonify
import pymongo

app = Flask(__name__)

conn = pymongo.MongoClient(host="localhost", port=27017)
conn.db.event_coll.create_index('type', unique=True)


@app.route('/v1/start', methods=['POST'])
def start():
    doc = request.get_json(force=True)
    if not doc.get("type"):
        abort(400)

    if conn.db.event_coll.find_one({"type": doc.get("type")}):
        return jsonify({"message": "Already exists!"})

    doc.update({"state": 0})
    conn.db.event_coll.save(doc)

    return jsonify({"message": "Created success!"})


@app.route('/v1/finish', methods=['POST'])
def finish():
    event = request.get_json(force=True)
    if not event.get("type"):
        abort(400)

    conn.db.event_coll.update_one({"type": event.get("type")}, {'$set': {'state': 1}})
    return jsonify({"message": "Finished success!"})