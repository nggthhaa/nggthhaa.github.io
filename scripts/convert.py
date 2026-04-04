"""
convert.py — Converts markdown blog posts to HTML pages and generates blog index.

Usage:
    python scripts/convert.py

This script:
1. Reads all .md files from the posts/ directory
2. Parses YAML frontmatter for metadata (title, hospital, department, date, etc.)
3. Converts markdown content to HTML
4. Generates individual blog post pages in blog/ directory
5. Updates blog.html with a card listing of all posts
"""

import os
import re
import json
import markdown
from datetime import datetime

# === Paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
POSTS_DIR = os.path.join(ROOT_DIR, "posts")
BLOG_DIR = os.path.join(ROOT_DIR, "blog")
BLOG_INDEX = os.path.join(ROOT_DIR, "blog.html")
POSTS_JSON = os.path.join(ROOT_DIR, "posts.json")


def parse_frontmatter(content):
    """Parse YAML-like frontmatter from markdown content."""
    metadata = {}
    body = content

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        body = match.group(2)

        for line in frontmatter.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                metadata[key] = value

    return metadata, body


def convert_markdown_to_html(md_content):
    """Convert markdown to HTML with extensions."""
    extensions = ['extra', 'codehilite', 'toc', 'nl2br']
    html = markdown.markdown(md_content, extensions=extensions)
    return html


def generate_post_page(metadata, html_content, slug):
    """Generate a full HTML page for a blog post."""
    title = metadata.get('title', 'Untitled')
    hospital = metadata.get('hospital', '')
    department = metadata.get('department', '')
    date = metadata.get('date', '')
    duration = metadata.get('duration', '')
    category = metadata.get('category', '')

    # Format date for display
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_display = date_obj.strftime('%B %d, %Y')
    except (ValueError, TypeError):
        date_display = date

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Thu Ha Nguyen</title>
    <meta name="description" content="{metadata.get('excerpt', '')}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>

    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a href="../index.html" class="nav-logo">Thu Ha N.</a>
            <button class="nav-toggle" id="navToggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-links" id="navLinks">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../education.html">Education</a></li>
                <li><a href="../blog.html" class="active">Blog</a></li>
            </ul>
        </div>
    </nav>

    <!-- Post Content -->
    <main class="page-container">
        <article class="post-page fade-in">

            <a href="../blog.html" class="post-back-link">← Back to Blog</a>

            <div class="post-header">
                <div class="post-meta-bar">
                    <span class="post-category">{category}</span>
                    <span class="post-date">{date_display}</span>
                    {f'<span class="post-duration">⏱ {duration}</span>' if duration else ''}
                </div>
                <h1 class="post-title">{title}</h1>
                <div class="post-hospital-info">
                    <span class="post-hospital">🏥 {hospital}</span>
                    <span class="post-department">📋 {department}</span>
                </div>
            </div>

            <div class="post-body">
                {html_content}
            </div>

        </article>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-links">
            <a href="https://github.com/nggthha" class="footer-link" title="GitHub" target="_blank" rel="noopener">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            </a>
            <a href="mailto:contact@example.com" class="footer-link" title="Email">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
            </a>
        </div>
        <p class="footer-text">© 2026 Thu Ha Nguyen. Built with 💚</p>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>'''


def generate_blog_card(metadata, slug):
    """Generate HTML for a blog card in the listing."""
    title = metadata.get('title', 'Untitled')
    hospital = metadata.get('hospital', '')
    department = metadata.get('department', '')
    date = metadata.get('date', '')
    duration = metadata.get('duration', '')
    category = metadata.get('category', '')
    excerpt = metadata.get('excerpt', '')

    # Format date
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_display = date_obj.strftime('%B %Y')
    except (ValueError, TypeError):
        date_display = date

    # Department emoji map
    dept_emoji = {
        'Pediatrics': '👶',
        'Infectious Diseases': '🦠',
        'Dermatology': '🔬',
        'Internal Medicine': '🩺',
        'Surgery': '🏥',
        'Obstetrics': '🤱',
        'Cardiology': '❤️',
        'Neurology': '🧠',
        'Orthopedics': '🦴',
        'Ophthalmology': '👁️',
        'ENT': '👂',
        'Psychiatry': '🧠',
    }
    emoji = dept_emoji.get(department, '🏥')

    return f'''
            <a href="blog/{slug}.html" class="glass-card blog-card fade-in" id="post-{slug}">
                <div class="blog-card-image">{emoji}</div>
                <div class="blog-card-body">
                    <div class="blog-card-meta">
                        <span class="blog-card-date">{date_display}</span>
                        <span class="blog-card-category">{department}</span>
                    </div>
                    <h2 class="blog-card-title">{title}</h2>
                    <p class="blog-card-hospital">🏥 {hospital} — {duration}</p>
                    <p class="blog-card-excerpt">{excerpt}</p>
                    <span class="blog-card-link">Read more →</span>
                </div>
            </a>'''


def generate_blog_index(cards_html):
    """Generate the full blog.html page."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog — Thu Ha Nguyen</title>
    <meta name="description" content="Clinical rotation experiences and hospital blog posts by Thu Ha Nguyen.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a href="index.html" class="nav-logo">Thu Ha N.</a>
            <button class="nav-toggle" id="navToggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-links" id="navLinks">
                <li><a href="index.html">Home</a></li>
                <li><a href="education.html">Education</a></li>
                <li><a href="blog.html" class="active">Blog</a></li>
            </ul>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="page-container">

        <!-- Page Hero -->
        <div class="page-hero fade-in">
            <h1>Clinical Experience</h1>
            <p>Hospital rotations, departments, and lessons learned along the way</p>
            <div class="section-line"></div>
        </div>

        <!-- Blog Grid -->
        <section class="blog-grid">
{cards_html}
        </section>

    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-links">
            <a href="https://github.com/nggthha" class="footer-link" title="GitHub" target="_blank" rel="noopener">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            </a>
            <a href="mailto:contact@example.com" class="footer-link" title="Email">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
            </a>
        </div>
        <p class="footer-text">© 2026 Thu Ha Nguyen. Built with 💚</p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>'''


def main():
    # Create output directory
    os.makedirs(BLOG_DIR, exist_ok=True)

    # Collect all posts
    posts = []

    if not os.path.exists(POSTS_DIR):
        print(f"Error: Posts directory not found at {POSTS_DIR}")
        return

    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]

    if not md_files:
        print("No markdown files found in posts/ directory.")
        return

    print(f"Found {len(md_files)} post(s) to convert.\n")

    for filename in md_files:
        filepath = os.path.join(POSTS_DIR, filename)
        slug = os.path.splitext(filename)[0]

        # Read markdown file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter and content
        metadata, body = parse_frontmatter(content)
        metadata['slug'] = slug

        # Convert markdown to HTML
        html_content = convert_markdown_to_html(body)

        # Generate post page
        post_html = generate_post_page(metadata, html_content, slug)
        output_path = os.path.join(BLOG_DIR, f"{slug}.html")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(post_html)

        posts.append(metadata)
        print(f"  [OK] Converted: {filename} -> blog/{slug}.html")

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x.get('date', ''), reverse=True)

    # Generate blog cards
    cards_html = ''
    for i, post in enumerate(posts):
        cards_html += generate_blog_card(post, post['slug'])

    # Generate blog index page
    blog_html = generate_blog_index(cards_html)

    with open(BLOG_INDEX, 'w', encoding='utf-8') as f:
        f.write(blog_html)

    print(f"\n  [OK] Generated blog.html with {len(posts)} post(s)")

    # Save posts metadata as JSON for potential future use
    with open(POSTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"  [OK] Saved posts metadata to posts.json")
    print(f"\nDone! {len(posts)} post(s) converted successfully.")


if __name__ == '__main__':
    main()
