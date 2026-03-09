from __future__ import annotations

import json
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
class Blog:
    title: str
    url: str


@dataclass
class Data:
    profile: Profile
    tech_stack: List[Tech]
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


def render_blogs(blogs: List[Blog]) -> List[str]:
    md = ["## 📝 Blog Posts", ""]
    for blog in blogs:
        md.append(f"[📄 {blog.title}]({blog.url})\n")
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
        blogs=[Blog(**b) for b in raw["blogs"]],
    )


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    data = load_data(DATA_FILE)

    md: List[str] = []

    md += render_header(data.profile)
    md += render_blogs(data.blogs)
    md += render_tech_stack(data.tech_stack)

    OUTPUT_FILE.write_text("\n".join(md), encoding="utf-8")

    print("README.md generated successfully!")


if __name__ == "__main__":
    main()
