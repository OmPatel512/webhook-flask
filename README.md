# Webhook Tracker – GitHub Webhook Event Listener & UI

This repository (`webhook-repo`) contains the **Flask-based backend and frontend** for tracking GitHub repository events like `Push`, `Pull Request`, and optionally `Merge`. Events are received via webhook, saved to MongoDB, and displayed in a UI that refreshes every 15 seconds.

> ⚙️ This repo is meant to be connected to a GitHub Actions testing repo (e.g. [`action-repo`](#action-repo-link-here)) that triggers webhook events.

---

## 📌 Features

- ✅ Receives GitHub webhook events (`Push`, `Pull Request`, `Merge`)
- ✅ Stores events in MongoDB
- ✅ Displays human-readable events in a simple UI
- ✅ UI auto-refreshes every 15 seconds (no JavaScript needed)
- 🏆 Bonus: Merge events supported for extra credit

---

## 📁 Project Structure

```bash
webhook-repo/
│
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # All Flask routes: UI and webhook handler
│   ├── models.py            # MongoDB access and queries
│   ├── utils.py             # Formatting utilities
│   └── db.py                # MongoDB connection setup
│
├── templates/
│   └── index.html           # UI template (auto-refreshes)
│
├── static/
│   └── style.css            # Optional styles for the UI
│
├── run.py                   # Entry point for the Flask app
├── requirements.txt         # Python dependencies
└── README.md                # You're here
```

---

## 🚀 How It Works

### 🛰️ GitHub Repo Setup

1. Deploy this Flask app locally or online.
2. Expose it via a public URL (e.g. using `ngrok` or a cloud host).
3. In your **GitHub repo** (e.g., [`action-repo`](#)), go to:
   - `Settings → Webhooks → Add webhook`
   - Payload URL: `https://your-app-url/webhook`
   - Content type: `application/json`
   - Events to trigger: `Push`, `Pull Request`, optionally others

### 📥 Incoming Webhook Events

| Event Type    | Format Example |
|---------------|----------------|
| `push`        | `"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC` |
| `pull_request`| `"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC` |
| `merge` 🏆    | `"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC` |

> Merge detection is based on `pull_request` event with `"action": "closed"` and `"merged": true`.

---

## 🧪 Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo
```

### 2. Create a virtual environment & install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the root:

```env
FLASK_APP=run.py
MONGO_URI=mongodb://localhost:27017/github_webhooks
```

### 4. Run the app

```bash
flask run
```

Now open: `http://localhost:5000`  
Use `ngrok http 5000` to make it public for GitHub webhook testing.

---

## 🌐 Deployed Repositories

| Repo Name     | Purpose                           |
|---------------|-----------------------------------|
| [`action-repo`](#) | Dummy GitHub repo to trigger events |
| `webhook-repo`     | This repo – webhook listener and UI |

---

## 📦 Dependencies

- Python 3.x
- Flask
- pymongo
- python-dotenv

Install via:

```bash
pip install -r requirements.txt
```

---

## 📬 Example Webhook Payloads

Handled GitHub events:
- `push`
- `pull_request` (`opened`, `closed` if merged)

Sample webhook delivery looks like:

```json
{
  "repository": { "full_name": "user/repo" },
  "pusher": { "name": "Travis" },
  "ref": "refs/heads/staging",
  ...
}
```

---

## 💡 Notes

- UI uses `meta` tag to auto-refresh every 15 seconds — no JavaScript involved.
- Events older than your desired time window can be filtered in `models.py`.
- You can extend `models.py` to log repo name, branch details, and action type.

---

## ✅ Submission Checklist

- [x] `Push`, `Pull Request` events handled
- [x] Events stored in MongoDB
- [x] Clean, readable UI with auto-refresh
- [x] Code modularized with clear naming and structure
- [x] Two separate GitHub repositories: `webhook-repo` and `action-repo`
- [x] Merge handling (optional brownie point)

