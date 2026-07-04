import os
import xml.etree.ElementTree as ET
import json
import sys

# Configuration: Exclusion list
EXCLUDED = {
    'deploy.bat', 'generate_sitemap.py', 'submit_indexnow.py', 
    'indexnow.json', 'sitemap.xml', '.git', '.well-known', 'README.md', 'robots.txt'
}

def is_valid(filename):
    if filename in EXCLUDED: return False
    if filename.startswith('google') and filename.endswith('.html'): return False
    return filename.endswith('.html')

def generate():
    # 1. Identify valid files
    files = [f for f in os.listdir('.') if is_valid(f)]
    
    # 2. Generate sitemap.xml
    root = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for f in files:
        url = ET.SubElement(root, 'url')
        ET.SubElement(url, 'loc').text = f"https://ruimanuelalmeidapinheiro.work/{f}"
    
    tree = ET.ElementTree(root)
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)
    
    # 3. Generate indexnow.json
    with open('indexnow.json', 'w') as f:
        json.dump({"urlList": [f"https://ruimanuelalmeidapinheiro.work/{fname}" for fname in files]}, f)
        
    # 4. Integrity Audit (Write-Read-Compare)
    try:
        with open('sitemap.xml', 'r', encoding='UTF-8') as f:
            if 'urlset' not in f.read(): raise Exception("Malformed sitemap")
        with open('indexnow.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            if len(data['urlList']) != len(files): raise Exception("IndexNow mismatch")
        print("Audit completed: OK.")
    except Exception as e:
        print(f"Audit failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate()