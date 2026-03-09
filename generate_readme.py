from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List
from urllib.parse import quote

DATA_FILE = Path("data.json")
OUTPUT_FILE = Path("README.md")


# -----------------------------
# Utils
# -----------------------------

LOGO_MAP = {
    "C#": "csharp",
    "c#": "csharp",
}


def encode_label(name: str) -> str:
    """URL encode badge label."""
    return quote(name, safe="")


def get_logo_name(name: str) -> str:
    """Map language name to shields logo name."""
    return LOGO_MAP.get(name, name.lower())


def make_badge(label: str, color: str, logo: str, style: str) -> str:
    label_encoded = encode_label(label)
    logo_name = get_logo_name(logo)

    return (
        f'https://img.shields.io/badge/{label_encoded}-{color}'
        f'?style={style}&logo={logo_name}&logoColor=white'
    )


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class Profile:
    name: str
    title: str
    email: str
    blog: str
    github: str


@dataclass
class Tech:
    name: str
    color: str
    logo: str


@dataclass
class Project:
    name: str
    description: str
    url: str
    language: str
    language_color: str
    language_logo: str


@dataclass
class Blog:
    title: str
    url: str


@dataclass
class Data:
    profile: Profile
    tech_stack: List[Tech]
    projects: List[Project]
    blogs: List[Blog]


# -----------------------------
# Rendering Functions
# -----------------------------

def render_header(profile: Profile) -> List[str]:
    return [
        f"## 👋 Hi, I'm {profile.name}",
        "",
        f"I'm a **{profile.title}** passionate about building modern web applications.",
        "",
        "",
    ]


def render_project(project: Project) -> str:
    badge_url = make_badge(
        project.language,
        project.language_color,
        project.language_logo,
        "flat",
    )
    
    html_template = f"""
    <a href="{project.url}" style="text-decoration: none; flex: 1;">
      <div style="margin: 8px 0; padding: 16px; height: 120px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; border: 1px solid rgba(255,255,255,0.2); cursor: pointer; box-sizing: border-box; overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; height: 30px;">
          <strong style="color: #fff; font-size: 16px;">💻 {project.name}</strong>
          <img src="{badge_url}" alt="{project.language}" height="18" style="vertical-align: middle;" />
        </div>
        <p style="margin: 12px 0 0 0; font-size: 14px; color: rgba(255,255,255,0.9); line-height: 1.5; height: 50px; overflow: hidden;">
          {project.description}
        </p>
      </div>
    </a>
    """

    return textwrap.dedent(html_template).strip()


def render_projects(projects: List[Project]) -> List[str]:
    md = ["## 🚀 Featured Projects", ""]
    
    # 每2个项目为一组，实现两列布局
    for i in range(0, len(projects), 2):
        row_projects = projects[i:i+2]
        md.append('<div style="display: flex; gap: 16px;">')
        
        for project in row_projects:
            md.append(render_project(project))
        
        md.append('</div>')
        md.append("")
    
    return md


def render_blog_item(blog: Blog) -> str:
    html_template = f"""
    <li style="margin: 8px 0;">
      <a href="{blog.url}" style="text-decoration: none; color: #333; font-size: 15px; display: block; padding: 12px 16px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6; transition: background 0.2s;">
        <strong>📄 {blog.title}</strong>
      </a>
    </li>
    """
    return textwrap.dedent(html_template).strip()


def render_blogs(blogs: List[Blog]) -> List[str]:
    md = ["## 📝 Latest Blog Posts", ""]
    
    # 构建博客列表项
    blog_items = []
    for blog in blogs:
        blog_items.append(render_blog_item(blog))
    
    # 包装在卡片容器中
    html_template = f"""
    <div style="margin: 16px 0; padding: 16px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px; border: 1px solid #dee2e6;">
      <ul style="list-style: none; padding: 0; margin: 0;">
        {"".join(blog_items)}
      </ul>
    </div>
    """
    
    md.append(textwrap.dedent(html_template).strip())
    md.append("")
    return md


def render_tech_stack(tech_stack: List[Tech]) -> List[str]:
    md = ["## 🛠️ Tech Stack", "", '<p align="left">']

    for tech in tech_stack:
        badge = make_badge(
            tech.name,
            tech.color,
            tech.logo,
            "for-the-badge",
        )

        md.append(
            f'  <img src="{badge}" alt="{tech.name}" />'
        )

    md.extend(["</p>", ""])
    return md


# -----------------------------
# Data Loading
# -----------------------------

def load_data(path: Path) -> Data:
    raw = json.loads(path.read_text(encoding="utf-8"))

    return Data(
        profile=Profile(**raw["profile"]),
        tech_stack=[Tech(**t) for t in raw["tech_stack"]],
        projects=[Project(**p) for p in raw["projects"]],
        blogs=[Blog(**b) for b in raw["blogs"]],
    )


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    data = load_data(DATA_FILE)

    md: List[str] = []
    
    md += render_header(data.profile)
    md += render_projects(data.projects)
    md += render_blogs(data.blogs)
    md += [""]
    md += render_tech_stack(data.tech_stack)

    OUTPUT_FILE.write_text("\n".join(md), encoding="utf-8")

    print("README.md generated successfully!")


if __name__ == "__main__":
    main()
