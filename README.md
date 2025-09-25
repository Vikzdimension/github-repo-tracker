# GitHub Repository Tracker

A full-stack web application built with **Django + React + PostgreSQL** that tracks GitHub repositories, provides complete CRUD functionality, integrates with the GitHub API, and visualizes data through an interactive dashboard.

## 🚀 Live Demo
[Live Application](https://github-repo-tracker.onrender.com) | [Admin Dashboard](https://github-repo-tracker.onrender.com/admin/projects/project/) | [API Documentation](https://github-repo-tracker.onrender.com/api/)

**Demo Credentials:**
- Username: `admin`
- Password: `admin123`

## 📋 Demo Task Requirements

This project fulfills all requirements for the demo task:

✅ **Python (Django) with PostgreSQL integration**  
✅ **Complete CRUD functionality via REST APIs**  
✅ **Third-party API integration** (GitHub REST API)  
✅ **Data visualization and reporting features**  
✅ **Clean, production-ready code**  
✅ **Comprehensive documentation**  

---

## 🔹 Features

### Core Functionality
- **Complete CRUD Operations**: Create, Read, Update, Delete repositories via REST API
- **GitHub API Integration**: Import repository data directly from GitHub
- **Admin Dashboard**: Django admin interface with embedded React analytics
- **Data Visualization**: Interactive statistics and repository analytics
- **Authentication**: Secure admin-only access to API endpoints

### Technical Features
- **REST API**: Full RESTful API with proper HTTP methods
- **Database Integration**: PostgreSQL with Django ORM
- **Frontend Integration**: React components embedded in Django admin
- **Static File Handling**: WhiteNoise for production static files
- **CORS Support**: Proper cross-origin resource sharing setup

---

## 🔹 Tech Stack

**Backend:**
- Django 5.2.6
- Django REST Framework
- PostgreSQL
- WhiteNoise (Static files)
- python-dotenv (Environment variables)

**Frontend:**
- React 18
- Vite (Build tool)
- Custom CSS (Django admin styling)
- Fetch API for HTTP requests

**Deployment:**
- Render (Platform)
- PostgreSQL (Database)
- Static file serving

---

## 🔹 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List all repositories |
| POST | `/api/github/save/{owner}/{repo}/` | Import repository from GitHub |
| DELETE | `/api/projects/{id}/delete/` | Delete repository |
| GET | `/admin/projects/project/` | Admin dashboard with analytics |

---

## 🔹 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js 16+ (for frontend build)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/Vikzdimension/github-repo-tracker.git
cd github-repo-tracker
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Database Setup
```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE github_repo_tracker;
\q

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Frontend Build
```bash
# Build React frontend
python build.py

# Or manually:
cd frontend/admin-dashboard
npm install
npm run build
cd ../../
python manage.py collectstatic --noinput
```

### 5. Run Application
```bash
python manage.py runserver
```

Visit:
- **Admin Dashboard**: http://localhost:8000/admin/projects/project/
- **API**: http://localhost:8000/api/projects/
- **Home Page**: http://localhost:8000/

---

## 🔹 Environment Variables

Create `.env` file in the `backend` directory:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Database
DATABASE_URL=postgres://username:password@localhost:5432/github_repo_tracker

# GitHub API (Optional - for higher rate limits)
GITHUB_TOKEN=your-github-token

# Deployment
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

---

## 🔹 Usage

### 1. Access Admin Dashboard
1. Login at `/admin/` with superuser credentials
2. Navigate to "Projects" section
3. Use the embedded analytics dashboard

### 2. Import GitHub Repository
1. In the dashboard, use "Import GitHub Repository" form
2. Enter repository owner and name (e.g., `facebook`, `react`)
3. Click "Import Repository"
4. View imported data in the statistics and table

### 3. API Usage
```bash
# List repositories
curl -X GET https://github-repo-tracker.onrender.com/api/projects/

# Import repository (requires admin authentication)
curl -X POST https://github-repo-tracker.onrender.com/api/github/save/facebook/react/

# Delete repository
curl -X DELETE https://github-repo-tracker.onrender.com/api/projects/1/delete/
```

---

## 🔹 Project Structure

```
github-repo-tracker/
├── backend/
│   ├── backend/           # Django settings
│   ├── projects/          # Main app
│   │   ├── models.py      # Database models
│   │   ├── views.py       # API views
│   │   ├── api_integration.py  # GitHub API
│   │   └── admin.py       # Admin configuration
│   ├── frontend/
│   │   └── admin-dashboard/   # React components
│   ├── templates/         # Django templates
│   ├── staticfiles/       # Static files
│   └── manage.py
├── build.py              # Build automation
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 🔹 Key Design Decisions

### 1. **Embedded React Dashboard**
- Integrated React components directly into Django admin
- Maintains Django's authentication and security
- Provides modern UI within familiar admin interface

### 2. **GitHub API Integration**
- Direct integration with GitHub REST API
- Handles rate limiting gracefully
- Supports both authenticated and unauthenticated requests

### 3. **Single Repository Deployment**
- Frontend builds are served by Django
- Simplified deployment process
- Reduced infrastructure complexity

### 4. **Admin-First Approach**
- Leverages Django's robust admin system
- Secure by default with proper authentication
- Extensible for additional features

---

## 🔹 Testing

```bash
# Run Django tests
python manage.py test

# Test API endpoints
python manage.py shell
>>> from django.test import Client
>>> client = Client()
>>> response = client.get('/api/projects/')
>>> print(response.status_code)
```

---

## 🔹 Deployment

### Render Deployment
1. Connect GitHub repository to Render
2. Set environment variables in Render dashboard
3. Use provided `render.yaml` configuration
4. Deploy automatically on git push

### Manual Deployment
```bash
# Build for production
DJANGO_DEBUG=False python build.py

# Collect static files
python manage.py collectstatic --noinput

# Run with production server
gunicorn backend.wsgi:application
```

---

## 🔹 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🔹 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🔹 Contact

**Developer**: Vivek Lode 
**Email**: vivek.lode1@gmail.com  
**GitHub**: [@Vikzdimension](https://github.com/Vikzdimension)  
**Project Link**: [https://github.com/Vikzdimension/github-repo-tracker](https://github.com/Vikzdimension/github-repo-tracker)
