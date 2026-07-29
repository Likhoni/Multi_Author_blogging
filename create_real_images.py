import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFont
from blog.models import Post

os.makedirs('media/post_images', exist_ok=True)

def generate_cover_image(filename, bg_color1, bg_color2, title_text, category_text):
    width, height = 800, 450
    image = Image.new('RGB', (width, height), bg_color1)
    draw = ImageDraw.Draw(image)

    # Draw smooth diagonal gradient lines / shapes
    for y in range(height):
        r = int(bg_color1[0] + (bg_color2[0] - bg_color1[0]) * (y / height))
        g = int(bg_color1[1] + (bg_color2[1] - bg_color1[1]) * (y / height))
        b = int(bg_color1[2] + (bg_color2[2] - bg_color1[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add geometric accents
    draw.polygon([(600, 0), (800, 0), (800, 450), (450, 450)], fill=(255, 255, 255, 30))
    draw.ellipse([50, -50, 350, 250], outline=(255, 255, 255, 60), width=8)
    draw.ellipse([550, 200, 850, 500], outline=(255, 255, 255, 40), width=12)

    # Draw Category pill background
    draw.rounded_rectangle([60, 60, 220, 100], radius=10, fill=(15, 23, 42))

    # Save to media/post_images
    filepath = os.path.join('media', 'post_images', filename)
    image.save(filepath)
    print(f"Generated image: {filepath}")
    return f"post_images/{filename}"

# Generate cover images for sample posts
img1 = generate_cover_image('python_cover.png', (79, 70, 229), (14, 165, 233), "Python & Django Guide", "EDUCATION")
img2 = generate_cover_image('travel_cover.png', (16, 185, 129), (6, 182, 212), "Travel Destinations", "TRAVEL")
img3 = generate_cover_image('django_cover.png', (99, 102, 241), (236, 72, 153), "Building Web Apps", "TECHNOLOGY")

# Update post objects in database
posts = list(Post.objects.filter(status='PUBLISHED').order_by('created_at'))
if len(posts) >= 1:
    posts[0].featured_image = img3
    posts[0].save()

if len(posts) >= 2:
    posts[1].featured_image = img2
    posts[1].save()

if len(posts) >= 3:
    posts[2].featured_image = img1
    posts[2].save()

print("Successfully updated database posts with real cover images!")
