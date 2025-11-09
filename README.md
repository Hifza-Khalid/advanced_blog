# Advanced Blog Platform

A full-featured blog platform built with Django featuring user authentication, role-based permissions, comments, categories, tags, and search functionality.

## 🚀 Features

- User Authentication (Register, Login, Logout)
- Role-Based Permissions (Admin, Author, Reader)
- Blog Post Management (Create, Edit, Delete)
- Comment System with Moderation
- Categories & Tags Organization
- Search & Filter Functionality
- Responsive Bootstrap Design
- Rich Text Editor (CKEditor)
- Image Upload for Posts
- SEO-Friendly URLs

## 🛠️ Quick Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### 1. Clone and Setup
```bash
# Clone the project
git clone https://github.com/Hifza-Khalid/advanced_blog
cd advanced_blog

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create default data
python manage.py create_categories
python manage.py create_tags
python manage.py setup_groups
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Main Site**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## 👥 Default User Roles

- **Admin**: Full access (use superuser account)
- **Author**: Can create/edit/delete own posts
- **Reader**: Can view posts and comment

## 📁 Project Structure
```
advanced_blog/
├── advanced_blog/     # Project settings
├── blog/             # Main blog application
├── accounts/         # Authentication app
├── templates/        # HTML templates
├── static/          # CSS, JS, images
└── manage.py        # Django management script
```

## 🌐 Deployment

### Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DISABLE_COLLECTSTATIC=1

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### PythonAnywhere
1. Upload project files
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Run migrations

## 🐛 Troubleshooting

**Static files not loading?**
```bash
python manage.py collectstatic
```

**Database issues?**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Permission errors?**
- Check user groups in admin panel
- Ensure authors are in 'Authors' group

## 📞 Support

For issues and questions, please contact: hifzaofpk@gmail.com
