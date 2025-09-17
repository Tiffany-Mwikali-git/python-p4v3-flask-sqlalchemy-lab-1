# server/app.py
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Route: Get earthquake by id
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake:
        return jsonify(quake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

# Route: Get earthquakes with magnitude >= given value
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [quake.to_dict() for quake in quakes]
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
