# Webhook Tracker – GitHub Webhook Event Listener & UI

This repository contains a **Flask-based backend and frontend** for tracking GitHub repository events like `Push`, `Pull Request`, and `Merge`. Events are received via webhook, saved to MongoDB, and displayed in a real-time UI that automatically refreshes every 15 seconds.

> ⚙️ This repo is designed to be connected to any GitHub repository that triggers webhook events.

---

## 📌 Features

- ✅ Receives GitHub webhook events (`Push`, `Pull Request`, `Merge`)
- ✅ Stores events in MongoDB with timestamps
- ✅ Displays human-readable events in a clean UI
- ✅ UI auto-refreshes every 15 seconds for real-time updates
- ✅ Dockerized for easy deployment
- ✅ Ngrok integration for local testing
- ✅ RESTful API endpoints for event data
- 🏆 Merge event detection for pull request closures

---

## 🚀 Getting Started

### 🐳 Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/webhook-repo.git
   cd webhook-repo
   ```

2. **Configure ngrok (for webhook testing)**
   - Sign up at [ngrok.com](https://ngrok.com) and get your auth token
   - Update `ngrok.yml` with your auth token:
   ```yaml
   version: "2"
   authtoken: YOUR_NGROK_AUTH_TOKEN_HERE
   tunnels:
     flask-webhook:
       proto: http
       addr: flask-app:5000
       schemes: [https]
       inspect: true
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Get your webhook URL**
   - Visit http://localhost:4040 (ngrok web interface)
   - Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 🔧 Local Development Setup

1. **Install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up MongoDB**
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   
   # Or install MongoDB locally
   ```

3. **Configure environment**
   Create a `.env` file:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   MONGO_URI=mongodb://localhost:27017/tachstax
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

---

## 🛰️ GitHub Webhook Setup

1. Go to your GitHub repository
2. Navigate to `Settings → Webhooks → Add webhook`
3. Configure the webhook:
   - **Payload URL**: `https://your-ngrok-url.ngrok.io/webhook`
   - **Content type**: `application/json`
   - **Events**: Select `Push events` and `Pull requests`
   - **Active**: ✅ Checked

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main UI dashboard |
| `/events` | GET | JSON list of recent events |
| `/webhook` | POST | GitHub webhook receiver |
| `/debug/events` | GET | HTML formatted event list |
| `/debug/stats` | GET | Database statistics |
| `/debug/test-insert` | POST | Insert test event |

### Example API Usage

```bash
# Get recent events
curl http://localhost:5000/events

# Get events with limit
curl http://localhost:5000/events?limit=5

# Test webhook manually
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Github-Event: push" \
  -d '{"ref": "refs/heads/main", "commits": [{"message": "Test"}]}'
```

---

## 📋 Event Format Examples

### Push Event
```
"john_doe pushed to main on 2025-05-31 14:30:00 UTC"
```

### Pull Request Events
```
"jane_smith submitted a pull request from feature-branch to main on 2025-05-31 14:25:00 UTC"
"jane_smith merged branch feature-branch to main on 2025-05-31 14:35:00 UTC"
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `1` |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/tachstax` |
| `FLASK_HOST` | Flask bind address | `0.0.0.0` |
| `FLASK_PORT` | Flask port | `5000` |

### Docker Compose Services

- **flask-app**: Main Flask application
- **ngrok**: Tunnel service for webhook testing

---

## 🧪 Testing

### Manual Testing
```bash
# Test database connection
curl http://localhost:5000/debug/stats

# Insert test event
curl -X POST http://localhost:5000/debug/test-insert

# View events
curl http://localhost:5000/events
```

### GitHub Event Testing
1. Make a commit to your connected repository
2. Create a pull request
3. Merge the pull request
4. Check http://localhost:5000 for real-time updates

---

## 🐛 Troubleshooting

### Common Issues

**Webhook delivery failed**
- Check if ngrok tunnel is active: http://localhost:4040
- Verify webhook URL in GitHub settings
- Check Flask app logs: `docker-compose logs flask-app`

**No events showing**
- Check database connection: `curl http://localhost:5000/debug/stats`
- Verify MongoDB is running
- Check webhook payload format

**Docker issues**
```bash
# Restart containers
docker-compose down && docker-compose up --build

# Check container status
docker-compose ps

# View logs
docker-compose logs -f flask-app
```

---

## 📦 Dependencies

```txt
Flask==3.1.0
pymongo==4.10.1
python-dotenv==1.0.1
```

---

## 🏗️ Architecture

```
GitHub Repository
       ↓ (webhook)
   Ngrok Tunnel
       ↓
  Flask Application
       ↓
   MongoDB Database
       ↓
    Web Interface
```

---

## 🚀 Deployment Options

### Local Development
- Use Docker Compose with ngrok for webhook testing

### Production Deployment
- Deploy to cloud platforms (Heroku, AWS, DigitalOcean)
- Use MongoDB Atlas for database
- Configure proper webhook URLs

---



