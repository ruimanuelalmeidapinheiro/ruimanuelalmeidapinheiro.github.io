from pathlib import Path
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import secrets

ROOT = Path(__file__).parent

DOMAIN = "https://ruimanuelalmeidapinheiro.work"

SITEMAP = ROOT / "sitemap.xml"
ROBOTS = ROOT / "robots.txt"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".well-known",
    "ME",
    "Pi",
    "assets"
}

EXCLUDED_FILES = {
    "404.html"
}

KEY_FILE = ROOT / "indexnow.key"


# -----------------------------------------
# INDEXNOW KEY MANAGEMENT & CLEANUP
# -----------------------------------------

def load_and_clean_keys():
    current_key = None

    if KEY_FILE.exists():
        current_key = KEY_FILE.read_text().strip()
    else:
        current_key = secrets.token_hex(16)
        KEY_FILE.write_text(current_key, encoding="utf-8")
        (ROOT / f"{current_key}.txt").write_text(current_key, encoding="utf-8")

    # Clean up any orphaned verification text files in the root
    for txt_file in ROOT.glob("*.txt"):
        if txt_file.name in ["robots.txt", "header.txt", "footer.txt", "llms.txt"]:
            continue
        if txt_file.name != f"{current_key}.txt":
            try:
                txt_file.unlink()
            except OSError:
                pass

    return current_key


# -----------------------------------------
# URL BUILD
# -----------------------------------------

def canonical(page):

    rel = page.relative_to(ROOT).as_posix()

    if rel.lower() == "index.html":
        return DOMAIN

    return (
        DOMAIN
        + "/"
        + rel[:-5]
    )


# -----------------------------------------
# PAGE DISCOVERY
# -----------------------------------------

def pages():

    out = []

    for f in ROOT.rglob("*.html"):

        if any(
            p in EXCLUDED_DIRS
            for p in f.parts
        ):
            continue

        if f.name in EXCLUDED_FILES:
            continue

        out.append(f)

    return sorted(out)


# -----------------------------------------
# SITEMAP
# -----------------------------------------

def build_sitemap():

    urls = []

    root = ET.Element(
        "urlset",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    )

    for page in pages():

        url = canonical(page)

        urls.append(url)

        item = ET.SubElement(
            root,
            "url"
        )

        ET.SubElement(
            item,
            "loc"
        ).text = url

        ts = datetime.fromtimestamp(
            page.stat().st_mtime,
            timezone.utc
        )

        ET.SubElement(
            item,
            "lastmod"
        ).text = ts.strftime(
            "%Y-%m-%d"
        )

    tree = ET.ElementTree(root)

    ET.indent(tree)

    tree.write(
        SITEMAP,
        encoding="utf-8",
        xml_declaration=True
    )

    return urls


# -----------------------------------------
# ROBOTS
# -----------------------------------------

def update_robots():

    content = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {DOMAIN}/sitemap.xml\n"
    )

    ROBOTS.write_text(
        content,
        encoding="utf-8"
    )


# -----------------------------------------

key = load_and_clean_keys()
urls = build_sitemap()
update_robots()

print()
print("Done")
print("Pages compiled to sitemap:", len(urls))
print("Active IndexNow key verified:", key)