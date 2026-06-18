from pathlib import Path
import xml.etree.ElementTree as ET
import urllib.request
import json

ROOT = Path(__file__).parent
DOMAIN = "https://ruimanuelalmeidapinheiro.work"
SITEMAP = ROOT / "sitemap.xml"
KEY_FILE = ROOT / "indexnow.key"

def submit():
    if not KEY_FILE.exists():
        print("Error: indexnow.key missing. Run generate_sitemap first.")
        return
        
    if not SITEMAP.exists():
        print("Error: sitemap.xml missing. Run generate_sitemap first.")
        return

    key = KEY_FILE.read_text().strip()

    # Parse URLs straight from the freshly generated sitemap.xml
    namespaces = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(SITEMAP)
    urls = [loc.text for loc in tree.findall(".//ns:loc", namespaces)]

    payload = {
        "host": "ruimanuelalmeidapinheiro.work",
        "key": key,
        "keyLocation": f"{DOMAIN}/{key}.txt",
        "urlList": urls
    }

    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            if status == 200:
                print(f"IndexNow API submission successful (Status 200). Submitted {len(urls)} URLs.")
            else:
                print(f"IndexNow responded with status code: {status}")
    except Exception as e:
        print(f"Submission failed: {e}")

if __name__ == "__main__":
    submit()