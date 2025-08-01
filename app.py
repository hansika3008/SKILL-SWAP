from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---- User Loader ----
class User(UserMixin):
    def __init__(self, doc):
        self.id = str(doc['_id'])
        self.username = doc['username']
        self.email = doc['email']
        self.password_hash = doc['password_hash']
        self.bio = doc.get('bio', '')
        self.rating = doc.get('rating', 5.0)
        self.created_at = doc.get('created_at')

    @staticmethod
    def get(user_id):
        doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return User(doc) if doc else None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# ---- Routes ----

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if mongo.db.users.find_one({'email': data['email']}):
            return jsonify({'error': 'Email already registered'}), 400
        if mongo.db.users.find_one({'username': data['username']}):
            return jsonify({'error': 'Username already taken'}), 400
        user_doc = {
            'username': data['username'],
            'email': data['email'],
            'password_hash': generate_password_hash(data['password']),
            'bio': data.get('bio', ''),
            'rating': 5.0,
            'created_at': datetime.utcnow()
        }
        res = mongo.db.users.insert_one(user_doc)
        user_doc['_id'] = res.inserted_id
        login_user(User(user_doc))
        return jsonify({'success': True, 'user_id': str(res.inserted_id)})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        doc = mongo.db.users.find_one({'email': data['email']})
        if doc and check_password_hash(doc['password_hash'], data['password']):
            login_user(User(doc))
            return jsonify({'success': True, 'user_id': str(doc['_id'])})
        return jsonify({'error': 'Invalid email or password'}), 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')

# ---- API Endpoints ----

@app.route('/api/user/profile')
@login_required
def get_user_profile():
    doc = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
    skills_teach = [s['name'] for s in mongo.db.skills.find({'teacher_id': current_user.id})]
    skills_learn = [s['name'] for s in mongo.db.skills.find({'learner_id': current_user.id})]
    return jsonify({
        'id': current_user.id,
        'username': doc['username'],
        'email': doc['email'],
        'bio': doc.get('bio', ''),
        'rating': doc.get('rating', 5.0),
        'skills_teach': skills_teach,
        'skills_learn': skills_learn,
        'created_at': doc['created_at'].isoformat() if doc.get('created_at') else None
    })

@app.route('/api/users')
@login_required
def get_users():
    users = []
    for doc in mongo.db.users.find():
        if str(doc['_id']) == current_user.id:
            continue
        skills_teach = [s['name'] for s in mongo.db.skills.find({'teacher_id': str(doc['_id'])})]
        skills_learn = [s['name'] for s in mongo.db.skills.find({'learner_id': str(doc['_id'])})]
        users.append({
            'id': str(doc['_id']),
            'username': doc['username'],
            'bio': doc.get('bio', ''),
            'rating': doc.get('rating', 5.0),
            'skills_teach': skills_teach,
            'skills_learn': skills_learn
        })
    return jsonify(users)

@app.route('/api/skills', methods=['POST'])
@login_required
def add_skill():
    data = request.get_json()
    skill_doc = {
        'name': data['name'],
        'description': data.get('description', ''),
        'category': data.get('category', ''),
        'teacher_id': current_user.id if data['type'] == 'teach' else None,
        'learner_id': current_user.id if data['type'] == 'learn' else None,
        'created_at': datetime.utcnow()
    }
    res = mongo.db.skills.insert_one(skill_doc)
    return jsonify({'success': True, 'skill_id': str(res.inserted_id)})

@app.route('/api/skills/<skill_id>', methods=['DELETE'])
@login_required
def delete_skill(skill_id):
    skill = mongo.db.skills.find_one({'_id': ObjectId(skill_id)})
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    if skill.get('teacher_id') != current_user.id and skill.get('learner_id') != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    mongo.db.skills.delete_one({'_id': ObjectId(skill_id)})
    return jsonify({'success': True})

@app.route('/api/swap-requests', methods=['POST'])
@login_required
def create_swap_request():
    data = request.get_json()
    req_doc = {
        'requester_id': current_user.id,
        'recipient_id': data['recipient_id'],
        'message': data['message'],
        'status': 'pending',
        'created_at': datetime.utcnow()
    }
    res = mongo.db.swap_requests.insert_one(req_doc)
    return jsonify({'success': True, 'request_id': str(res.inserted_id)})

@app.route('/api/swap-requests/<request_id>', methods=['PUT'])
@login_required
def update_swap_request(request_id):
    data = request.get_json()
    req = mongo.db.swap_requests.find_one({'_id': ObjectId(request_id)})
    if not req:
        return jsonify({'error': 'Not found'}), 404
    if req['recipient_id'] != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    mongo.db.swap_requests.update_one({'_id': ObjectId(request_id)}, {'$set': {'status': data['status']}})
    return jsonify({'success': True})

@app.route('/api/messages')
@login_required
def get_messages():
    other_user_id = request.args.get('user_id', type=str)
    if not other_user_id:
        return jsonify({'error': 'User ID required'}), 400
    query = {'$or': [
        {'sender_id': current_user.id, 'receiver_id': other_user_id},
        {'sender_id': other_user_id, 'receiver_id': current_user.id}
    ]}
    messages = []
    for m in mongo.db.messages.find(query).sort('created_at', 1):
        messages.append({
            'id': str(m['_id']),
            'content': m['content'],
            'sender_id': m['sender_id'],
            'receiver_id': m['receiver_id'],
            'is_sent': m['sender_id'] == current_user.id,
            'created_at': m['created_at'].isoformat() if m.get('created_at') else None
        })
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    message_doc = {
        'content': data['content'],
        'sender_id': current_user.id,
        'receiver_id': data['receiver_id'],
        'created_at': datetime.utcnow(),
        'is_read': False
    }
    res = mongo.db.messages.insert_one(message_doc)
    return jsonify({
        'success': True,
        'message_id': str(res.inserted_id),
        'created_at': message_doc['created_at'].isoformat()
    })

@app.route('/api/search')
@login_required
def search_users():
    query = request.args.get('q', '').lower()
    regex = {'$regex': query, '$options': 'i'}
    users = []
    for doc in mongo.db.users.find({'$or': [{'username': regex}, {'bio': regex}]}):
        if str(doc['_id']) == current_user.id:
            continue
        skills_teach = [s['name'] for s in mongo.db.skills.find({'teacher_id': str(doc['_id'])})]
        skills_learn = [s['name'] for s in mongo.db.skills.find({'learner_id': str(doc['_id'])})]
        users.append({
            'id': str(doc['_id']),
            'username': doc['username'],
            'bio': doc.get('bio', ''),
            'rating': doc.get('rating', 5.0),
            'skills_teach': skills_teach,
            'skills_learn': skills_learn
        })
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
