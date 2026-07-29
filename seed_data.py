import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Post, Comment, PostLike

User = get_user_model()

print("Seeding initial platform data with internet theme images...")

os.makedirs('media/post_images', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_image(url, filename):
    filepath = os.path.join('media', 'post_images', filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(filepath, 'wb') as f:
            f.write(resp.read())
        return f"post_images/{filename}"
    except Exception as e:
        print(f"Image fetch error: {e}")
        return f"post_images/{filename}"

# 1. Create Superuser (Admin)
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@likhoni.com',
        'is_staff': True,
        'is_superuser': True,
        'is_author': True,
        'bio': 'Site Owner and Super Administrator of Likhoni.'
    }
)
if created:
    admin_user.set_password('admin12345')
    admin_user.save()

# 2. Create Demo Authors
author_john, created = User.objects.get_or_create(
    username='john_author',
    defaults={
        'email': 'john@likhoni.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'is_author': True,
        'bio': 'Tech enthusiast, backend software engineer, and open source advocate.'
    }
)
if created:
    author_john.set_password('author12345')
    author_john.save()

author_sarah, created = User.objects.get_or_create(
    username='sarah_writer',
    defaults={
        'email': 'sarah@likhoni.com',
        'first_name': 'Sarah',
        'last_name': 'Conner',
        'is_author': True,
        'bio': 'Travel blogger and lifestyle writer documenting global adventures.'
    }
)
if created:
    author_sarah.set_password('author12345')
    author_sarah.save()

# 3. Create Demo Reader
reader_alex, created = User.objects.get_or_create(
    username='alex_reader',
    defaults={
        'email': 'alex@likhoni.com',
        'first_name': 'Alex',
        'last_name': 'Smith',
        'is_author': False,
        'bio': 'Avid reader and tech commenter.'
    }
)
if created:
    reader_alex.set_password('reader12345')
    reader_alex.save()

# 4. Create Categories
cat_tech, _ = Category.objects.get_or_create(name='Technology', defaults={'description': 'Latest news, coding tutorials, and web development.'})
cat_life, _ = Category.objects.get_or_create(name='Lifestyle', defaults={'description': 'Life tips, mindfulness, and productivity hacks.'})
cat_travel, _ = Category.objects.get_or_create(name='Travel', defaults={'description': 'Guides to extraordinary destinations around the world.'})
cat_edu, _ = Category.objects.get_or_create(name='Education', defaults={'description': 'Learning resources, career advice, and deep dives.'})

# 5. Create Tags
tag_django, _ = Tag.objects.get_or_create(name='Django')
tag_python, _ = Tag.objects.get_or_create(name='Python')
tag_web, _ = Tag.objects.get_or_create(name='WebDev')
tag_tips, _ = Tag.objects.get_or_create(name='Tips')
tag_adventure, _ = Tag.objects.get_or_create(name='Adventure')

# 6. Create Demo Posts with Real Internet Images
if Post.objects.count() == 0:
    img_django = fetch_image('https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&q=80', 'tech_django_code.jpg')
    img_travel = fetch_image('https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1200&q=80', 'travel_landscape.jpg')
    img_python = fetch_image('https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&q=80', 'python_laptop.jpg')
    img_ai = fetch_image('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&q=80', 'ai_futuristic.jpg')

    p1 = Post.objects.create(
        title='Building Scalable Web Applications with Django',
        content=(
            "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.\n\n"
            "In this article, we explore how to leverage Django's ORM, middleware, and custom security models to construct "
            "production-ready web platforms with multi-author permissions, session management, and robust static/media serving."
        ),
        category=cat_tech,
        author=author_john,
        status='PUBLISHED',
        featured_image=img_django,
        view_count=42
    )
    p1.tags.add(tag_django, tag_python, tag_web)

    p2 = Post.objects.create(
        title='Top 10 Hidden Gems to Visit in 2026',
        content=(
            "From serene mountain retreats to vibrant coastal villages, traveling opens our eyes to new cultures and horizons.\n\n"
            "Here is our curated list of 10 breathtaking destinations that remain undisturbed by mass tourism. "
            "Pack your bags and prepare for an unforgettable adventure!"
        ),
        category=cat_travel,
        author=author_sarah,
        status='PUBLISHED',
        featured_image=img_travel,
        view_count=89
    )
    p2.tags.add(tag_adventure, tag_tips)

    p3 = Post.objects.create(
        title='Mastering Modern Python: Best Practices and Tips',
        content=(
            "Python continues to dominate web backend engineering, data science, and AI development.\n\n"
            "Discover essential pythonic idioms, pattern matching, async constructs, and virtual environment management "
            "that will make your codebase cleaner and faster."
        ),
        category=cat_edu,
        author=author_john,
        status='PUBLISHED',
        featured_image=img_python,
        view_count=15
    )
    p3.tags.add(tag_python, tag_tips)

    # Draft Post
    Post.objects.create(
        title='Upcoming Trends in Artificial Intelligence (Draft)',
        content='Draft content on generative models, subagents, and automated pair programming tools...',
        category=cat_tech,
        author=author_john,
        status='DRAFT',
        featured_image=img_ai,
        view_count=0
    )

    # Seed comments and likes
    Comment.objects.create(post=p1, user=reader_alex, text="Great overview of Django architecture!")
    Comment.objects.create(post=p1, user=author_sarah, text="Loved reading this, John! Very informative.")
    PostLike.objects.create(post=p1, user=reader_alex)
    PostLike.objects.create(post=p1, user=author_sarah)
    PostLike.objects.create(post=p2, user=reader_alex)

print("Seed completed successfully with internet images!")
