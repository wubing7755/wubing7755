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
    description: str
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
    <details style="display: block; margin: 8px 0; background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; border: 1px solid #dee2e6;">
      <summary style="padding: 12px 16px; cursor: pointer; color: #333; list-style: none;">
        <strong>💻 {project.name}</strong> 
        <img src="{badge_url}" alt="{project.language}" height="18" style="vertical-align: middle;" />
        <p style="margin: 4px 0 0 0; font-size: 14px; color: #6c757d;">
          {project.description}
        </p>
      </summary>
      <div style="padding: 12px 16px; border-top: 1px solid #dee2e6; background: #f1f3f5;">
        <p style="margin: 0; font-size: 14px; color: #495057;">
          🔗 <a href="{project.url}" style="color: #007ACC; text-decoration: none;">View on GitHub →</a>
        </p>
      </div>
    </details>
    """

    return textwrap.dedent(html_template).strip()


def render_projects(projects: List[Project]) -> List[str]:
    md = ["## 🚀 Featured Projects", ""]
    for project in projects:
        md.append(render_project(project))
        md.append("")
    return md


def render_blog(blog: Blog) -> str:
    html_template = f"""
    <details style="display: block; margin: 8px 0; background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; border: 1px solid #dee2e6;">
      <summary style="padding: 12px 16px; cursor: pointer; color: #333; list-style: none;">
        <strong>📄 {blog.title}</strong>
        <p style="margin: 4px 0 0 0; font-size: 14px; color: #6c757d;">
          {blog.description}
        </p>
      </summary>
      <div style="padding: 12px 16px; border-top: 1px solid #dee2e6; background: #f1f3f5;">
        <p style="margin: 0; font-size: 14px; color: #495057;">
          🔗 <a href="{blog.url}" style="color: #007ACC; text-decoration: none;">View on CNBlogs →</a>
        </p>
      </div>
    </details>
    """
    
    return textwrap.dedent(html_template).strip()


def render_blogs(blogs: List[Blog]) -> List[str]:
    md = ["## 📝 Latest Blog Posts", ""]
    for blog in blogs:
        md.append(render_blog(blog))
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
