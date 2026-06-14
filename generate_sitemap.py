import os
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_sitemap():
    # Configuration
    base_url = "https://ruimanuelalmeidapinheiro.work"
    root_dir = os.getcwd()
    sitemap_filename = "sitemap.xml"
    
    # Skip directories that shouldn't be indexed
    excluded_dirs = {'.git', '.well-known', 'ME', 'Pi'}
    
    # Skip specific files (add any others you want to exclude)
    excluded_files = {
        'google8af3e8699578313a.html',  # Google Search Console verification
        # Add other files to exclude here if needed
        # 'example.html',
    }
    
    # Create the root element with the correct namespace
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        
        for filename in filenames:
            # Only include HTML files, excluding unwanted specific files
            if filename.lower().endswith('.html') and filename not in excluded_files:
                # Calculate relative path
                rel_dir = os.path.relpath(dirpath, root_dir)
                if rel_dir == '.':
                    rel_path = filename
                else:
                    rel_path = os.path.join(rel_dir, filename).replace('\\', '/')
                
                # Canonical URL mapping
                # If it's index.html, map it to the bare directory/root domain
                if rel_path == 'index.html':
                    page_url = base_url + "/"
                else:
                    page_url = f"{base_url}/{rel_path}"
                
                # Get last modification time
                full_path = os.path.join(dirpath, filename)
                mtime = os.path.getmtime(full_path)
                lastmod = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                
                # Build XML structure
                url_el = ET.SubElement(urlset, "url")
                loc_el = ET.SubElement(url_el, "loc")
                loc_el.text = page_url
                lastmod_el = ET.SubElement(url_el, "lastmod")
                lastmod_el.text = lastmod
                
                # Optional: Add changefreq and priority (uncomment if desired)
                # changefreq_el = ET.SubElement(url_el, "changefreq")
                # changefreq_el.text = "monthly"
                # priority_el = ET.SubElement(url_el, "priority")
                # if rel_path == 'index.html':
                #     priority_el.text = "1.0"
                # else:
                #     priority_el.text = "0.8"
    
    # Count URLs for verification
    url_count = len(urlset.findall('url'))
    
    # Format the XML into a readable string
    xml_str = ET.tostring(urlset, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="UTF-8").decode("utf-8")
    
    # Write to sitemap.xml
    output_path = os.path.join(root_dir, sitemap_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"Success: {sitemap_filename} updated successfully.")
    print(f"Total URLs included: {url_count}")
    print(f"Excluded files: {', '.join(excluded_files) if excluded_files else 'none'}")

if __name__ == "__main__":
    generate_sitemap()