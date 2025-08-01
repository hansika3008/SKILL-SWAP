# SkillSwap - Exchange Skills, Build Community

A modern web application enabling users to exchange skills and build community. Built with Flask, MongoDB, and modern frontend technologies.

## Features

- **User Registration & Authentication**: Secure accounts with email/password
- **Skill Management**: Add skills to teach and learn
- **User Discovery**: Search users by skills
- **Skill Swap Requests**: Send and manage exchange requests
- **Messaging System**: Real-time user messaging
- **Rating System**: Rate and review after exchanges
- **Responsive Design**: Works on desktop and mobile

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **ODM**: Flask-PyMongo or MongoEngine

## Database Schema

### Core Collections

1. **User**: Profiles and authentication
2. **Skill**: Skills users can teach/learn
3. **Message**: User messaging
4. **SwapRequest**: Skill exchange requests
5. **Rating**: User ratings and reviews

## Installation & Setup

### Prerequisites

- Python 3.8+
- MongoDB 6.0+
- pip

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd skillswap
```

### Step 2: Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MongoDB

1. Start MongoDB server
2. Create a database user or use default
3. Update connection in `app.py`:

```python
app.config['MONGO_URI'] = 'mongodb://username:password@localhost:27017/skillswap'
```

### Step 5: Set Up Database

No schema setup required for MongoDB; initialize collections or indexes if needed.

### Step 6: Run the Application

```bash
python app.py
```

Access at `http://localhost:5000`

## Usage

### For Users

1. **Register**: Create an account
2. **Add Skills**: List skills to teach/learn
3. **Browse Users**: Search by skills
4. **Request Swaps**: Send exchange requests
5. **Message**: Chat with users
6. **Rate**: Give feedback after exchanges

### For Developers

#### Project Structure

```
skillswap/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── browse.html
│   └── messages.html
└── skill_swap_website.html
```

#### API Endpoints

- `GET /` - Home
- `GET /register` - Registration
- `POST /register` - Create user
- `GET /login` - Login
- `POST /login` - Authenticate
- `GET /dashboard` - User dashboard
- `GET /browse` - Browse users
- `GET /messages` - Messaging

#### API Endpoints (JSON)

- `GET /api/user/profile` - Current user profile
- `GET /api/users` - All users
- `POST /api/skills` - Add skill
- `DELETE /api/skills/<id>` - Remove skill
- `POST /api/swap-requests` - Create swap request
- `PUT /api/swap-requests/<id>` - Update swap request
- `GET /api/messages` - Get messages
- `POST /api/messages` - Send message
- `GET /api/search` - Search users

## Configuration

### Environment Variables

- `FLASK_SECRET_KEY`: Session secret
- `MONGO_URI`: MongoDB connection
- `FLASK_ENV`: 'development' for debug

### Database Configuration

Update in `app.py`:

```python
app.config['MONGO_URI'] = 'mongodb://username:password@localhost:27017/skillswap'
```

## Security Features

- Password hashing (Werkzeug)
- Session authentication (Flask-Login)
- CSRF protection (Flask-WTF)
- Input validation
- NoSQL injection prevention

## Future Enhancements

- Real-time messaging (WebSockets)
- Email notifications
- File sharing
- Video calling
- Mobile app
- Advanced search
- Skill categories/tags
- Achievement system
- Group exchanges

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

MIT License - see LICENSE file.

## Support

Open an issue on GitHub for support.

## Acknowledgments

- Flask community
- MongoDB
- Modern CSS
- Font Awesome
