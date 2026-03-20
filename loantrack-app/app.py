from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loantrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))

# CREATE DB
@app.before_first_request
def setup():
    db.create_all()
    if not User.query.first():
        db.session.add(User(username="admin", password="admin123", role="Admin"))
        db.session.add(User(username="staff", password="staff123", role="Staff"))
        db.session.commit()

# ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(
        username=data['username'],
        password=data['password']
    ).first()

    if user:
        return jsonify({"success": True, "username": user.username, "role": user.role})
    else:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True)