import os

def final_fix():
    targets = [
        "main@ruimanuelalmeidapinheiro.work",
        "waveontology@ruimanuelalmeidapinheiro.work"
    ]
    
    count = 0
    updated_files = []
    
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            original = content
            for email in targets:
                # This pattern matches the mailto: link regardless of spaces
                # We target the 'a href' part directly
                part = f'mailto:{email}'
                if part in content and "email_off" not in content:
                    # Inject the bypass tag before the tag starts
                    # We look for the <a> tag that contains the mailto
                    search_str = f'<a href="{part}"'
                    replace_str = f'<a href="{part}"'
                    content = content.replace(search_str, replace_str)
                    
                    # Close the bypass tag after the </a>
                    content = content.replace(f'</a>', f'</a>')
            
            if content != original:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                updated_files.append(filename)
                print(f"Updated: {filename}")
    
    print(f"\nTotal files updated: {count}")
    print(f"List: {updated_files}")

if __name__ == "__main__":
    final_fix()