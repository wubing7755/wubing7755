import json
from urllib.parse import quote

# URL encode for badge label (special chars like #)
def encode_label(name):
    return quote(name, safe='')

# Map language names to logo names
LOGO_MAP = {
    'C#': 'csharp',
    'c#': 'csharp',
}

# Get logo name (use mapped value or lowercase)
def get_logo_name(name):
    return LOGO_MAP.get(name, name.lower())

# Read data from JSON file
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

profile = data['profile']
tech_stack = data['tech_stack']
projects = data['projects']
blogs = data['blogs']

# Generate markdown content
md = []

# Header
md.append(f"## 👋 Hi, I'm {profile['name']}")
md.append("")
md.append(f"I'm a **{profile['title']}** passionate about building modern web applications.")
md.append("")

# Divider
# md.append("---")
md.append("")

# Featured Projects
md.append("## 🚀 Featured Projects")
md.append("")

for project in projects:
    label_encoded = encode_label(project['language'])
    logo_name = get_logo_name(project['language_logo'])
    project_card = f'''<details style="display: block; margin: 8px 0; background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; border: 1px solid #dee2e6;">
  <summary style="padding: 12px 16px; cursor: pointer; color: #333; list-style: none;">
    <strong>💻 {project['name']}</strong> <img src="https://img.shields.io/badge/{label_encoded}-{project['language_color']}?style=flat&logo={logo_name}&logoColor=white" alt="{project['language']}" height="18">
    <p style="margin: 4px 0 0 0; font-size: 14px; color: #6c757d;">{project['description']}</p>
  </summary>
  <div style="padding: 12px 16px; border-top: 1px solid #dee2e6; background: #f1f3f5;">
    <p style="margin: 0; font-size: 14px; color: #495057;">🔗 <a href="{project['url']}" style="color: #007ACC; text-decoration: none;">View on GitHub →</a></p>
  </div>
</details>'''
    md.append(project_card)
    md.append("")

# Latest Blog Posts
md.append("## 📝 Latest Blog Posts")
md.append("")

for blog in blogs:
    blog_card = f'''<details style="display: block; margin: 8px 0; background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; border: 1px solid #dee2e6;">
  <summary style="padding: 12px 16px; cursor: pointer; color: #333; list-style: none;">
    <strong>📄 {blog['title']}</strong>
    <p style="margin: 4px 0 0 0; font-size: 14px; color: #6c757d;">{blog['description']}</p>
  </summary>
  <div style="padding: 12px 16px; border-top: 1px solid #dee2e6; background: #f1f3f5;">
    <p style="margin: 0; font-size: 14px; color: #495057;">🔗 <a href="{blog['url']}" style="color: #007ACC; text-decoration: none;">View on CNBlogs →</a></p>
  </div>
</details>'''
    md.append(blog_card)
    md.append("")

# Divider
# md.append("---")
md.append("")

# Tech Stack
md.append("## 🛠️ Tech Stack")
md.append("")
md.append('<p align="left">')
for tech in tech_stack:
    label_encoded = encode_label(tech['name'])
    logo_name = get_logo_name(tech['logo'])
    badge = f'  <img src="https://img.shields.io/badge/{label_encoded}-{tech["color"]}?style=for-the-badge&logo={logo_name}&logoColor=white" alt="{tech["name"]}" />'
    md.append(badge)
md.append("</p>")
md.append("")

# Write to README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

print("README.md generated successfully!")
