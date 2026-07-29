# Likhoni - Multi-Author Blogging Platform (Django)

A feature-rich Multi-Author Blogging Platform built with **Python 3** and **Django**. This platform features custom user roles (Reader, Author, Admin), Category & Tag filtering, Post Creation & Draft/Published workflow, Author Analytics Dashboard, Comment system with moderation, Post Likes system, full-text Search, Pagination, and Media file handling.

---

## 🌟 Key Features

- **Authentication & Roles**:
  - User registration, login, and secure logout.
  - Role hierarchy: **Reader** (default upon sign up), **Author** (promoted by site admin), and **Superuser/Admin**.
  - Role-based permissions: Readers browse, comment, and like posts. Authors create, edit, and delete their own posts.
  - Strict view-level security ensuring Authors cannot modify other authors' posts.
- **Category & Tag Management**:
  - Categorization (one category per post) and Tagging (many-to-many relationship).
  - Managed via Django Admin panel.
- **Post & Draft Workflow**:
  - Auto-generated unique post slugs from post titles.
  - Featured cover image uploads.
  - Draft vs. Published status. Draft posts are strictly protected and hidden from the public homepage, search, and non-author views.
- **Author Dashboard & Analytics**:
  - Personal dashboard listing author's posts with status badges.
  - Analytics cards displaying total articles, published count, draft count, and aggregate view counts.
  - Quick action links for post creation, editing, and deletion.
- **Public Discovery & Interactivity**:
  - Paginated post listings (newest first).
  - Filtering by category and tag.
  - Case-insensitive search by post title and content.
  - Single author public profile page listing their published works.
  - Request-session-guarded view count increment.
  - Unique post liking (toggle like/unlike).
  - Commenting system with moderation (comment owners, post authors, and admins can delete comments).

---

## 🚀 Setup & Local Execution Guide

### Prerequisites
- Python 3.10+ installed on your system.
- `pip` package manager.

---

### Step 1: Clone the Repository & Navigate to Workspace
```bash
git clone <your-repository-url>
cd likhoni_project
```

---

### Step 2: Create & Activate Virtual Environment
```bash
# On Linux / macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

---

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables (`.env`)
Copy `.env.example` to create your local `.env` file:
```bash
cp .env.example .env
```
Ensure `.env` contains your development configuration (never commit `.env` to Git):
```env
SECRET_KEY=django-insecure-multi-author-blogging-platform-key-2026
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*
```

---

### Step 5: Database Migrations
Run Django migrations to set up the database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 6: Create Superuser (Admin) or Seed Demo Data

#### Option A: Seed Pre-configured Demo Accounts & Sample Posts (Recommended)
We provide a seed script that creates demo users, categories, tags, and sample articles with featured images:
```bash
python seed_data.py
```
**Default Credentials Created by Seed Script**:
- **Superuser/Admin**: username: `admin` | password: `admin12345`
- **Author 1**: username: `john_author` | password: `author12345`
- **Author 2**: username: `sarah_writer` | password: `author12345`
- **Reader**: username: `alex_reader` | password: `reader12345`

#### Option B: Create Custom Superuser Manually
```bash
python manage.py createsuperuser
```

---

### Step 7: Run Development Server
Start the Django development server:
```bash
python manage.py runserver
```
Open your browser and visit:
- **Homepage**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Unit Tests

Run the full Django test suite covering models, permissions, views, comments, likes, search, and draft protection:
```bash
python manage.py test
```

---

## 📂 Project Structure Overview

```
likhoni_project/
├── blog_project/           # Django project settings & main URL configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog/                   # Main blogging app
│   ├── admin.py            # Custom User & Model Admin configurations
│   ├── decorators.py       # Role-based access control (@author_required)
│   ├── forms.py            # User registration, Post & Comment forms
│   ├── models.py           # User, Category, Tag, Post, Comment, PostLike models
│   ├── tests.py            # Automated test suite
│   ├── urls.py             # Application route mappings
│   └── views.py            # Function-based views for blog platform
├── templates/              # HTML templates with template inheritance (base.html)
│   ├── base.html
│   ├── blog/
│   └── registration/
├── static/                 # Static assets (Custom CSS design system)
│   └── css/style.css
├── media/                  # User uploaded featured images
│   └── post_images/
├── .env                    # Environment secrets (ignored by git)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
├── seed_data.py            # Database seeding script for quick setup
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```
# likhoni
