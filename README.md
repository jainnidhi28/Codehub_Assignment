# 🎬 Movie Database Application

A full-stack movie database application built with Vue.js frontend and Django backend.

## 📁 Project Structure

### 🎨 Frontend (Vue.js)
**Location: `frontend_repo/`**

- **`src/App.vue`** - Main Vue component with movie interface
- **`src/main.js`** - Vue application entry point
- **`src/style.css`** - Global styles
- **`package.json`** - Frontend dependencies
- **`vite.config.js`** - Vite configuration

**Key Features:**
- 🏠📋❤🤍🔖📑⭐☆🎬 Emoji buttons for better UX
- Movie search and details
- Review and discussion forms
- Responsive design with dark theme
- Interactive movie recommendations

### 🔧 Backend (Django)
**Location: `backend_repo/`**

- **`apps/demo/`** - Django app with models, views, serializers
- **`demo_project/`** - Django project settings and configuration
- **`manage.py`** - Django management script
- **`requirements.txt`** - Python dependencies

**Key Features:**
- REST API endpoints
- Database models for movies, reviews, discussions
- Serializers for API responses
- Management commands for data population

## 🚀 Quick Start

### Frontend Setup
```bash
cd frontend_repo
npm install
npm run dev
```

### Backend Setup
```bash
cd backend_repo
pip install -r requirements.txt
python manage.py runserver
```

## 📋 Features

### ✅ Implemented Features
- **Movie Database Interface** - Browse and view movie details
- **Emoji Buttons** - Interactive buttons with emojis
- **Review System** - Add and view movie reviews
- **Discussion System** - Start and participate in discussions
- **Responsive Design** - Works on all devices
- **Dark Theme** - Modern UI with dark color scheme

### 🎯 Key Files to Explore

**Frontend:**
- `frontend_repo/src/App.vue` - Main application component
- `frontend_repo/src/style.css` - Styling and animations

**Backend:**
- `backend_repo/apps/demo/models.py` - Database models
- `backend_repo/apps/demo/views.py` - API endpoints
- `backend_repo/apps/demo/serializers.py` - Data serialization

## 🔗 Repository Links

- **Frontend Code**: [frontend_repo/src/](frontend_repo/src/)
- **Backend Code**: [backend_repo/apps/demo/](backend_repo/apps/demo/)
- **Project Settings**: [backend_repo/demo_project/](backend_repo/demo_project/)

## 📝 Notes

- The repository includes both frontend and backend code
- `node_modules` and `__pycache__` files are excluded via `.gitignore`
- Database file (`db.sqlite3`) is excluded for security
- All source code is properly organized in respective folders

## 🎉 Getting Started

1. **Clone the repository**
2. **Navigate to frontend_repo** for Vue.js application
3. **Navigate to backend_repo** for Django API
4. **Follow setup instructions** in each folder

---

**Built with ❤️ using Vue.js and Django**