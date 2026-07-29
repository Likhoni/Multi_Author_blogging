import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog.models import Post

os.makedirs('media/post_images', exist_ok=True)

# High Quality Unsplash Image URLs
IMAGE_MAP = {
    'Building Scalable Web Applications with Django': {
        'url': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&q=80',
        'filename': 'tech_django_code.jpg'
    },
    'Top 10 Hidden Gems to Visit in 2026': {
        'url': 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1200&q=80',
        'filename': 'travel_landscape.jpg'
    },
    'Mastering Modern Python: Best Practices and Tips': {
        'url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&q=80',
        'filename': 'python_laptop.jpg'
    },
    'Upcoming Trends in Artificial Intelligence (Draft)': {
        'url': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&q=80',
        'filename': 'ai_futuristic.jpg'
    }
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for title, info in IMAGE_MAP.items():
    dest_path = os.path.join('media', 'post_images', info['filename'])
    print(f"Downloading internet image for '{title}'...")
    try:
        req = urllib.request.Request(info['url'], headers=headers)
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Successfully saved to {dest_path}")

        # Update Post in DB
        post = Post.objects.filter(title=title).first()
        if post:
            post.featured_image = f"post_images/{info['filename']}"
            post.save()
            print(f"Updated post '{title}' with internet image.")
    except Exception as e:
        print(f"Error downloading {info['url']}: {e}")

print("All internet theme images updated successfully!")
