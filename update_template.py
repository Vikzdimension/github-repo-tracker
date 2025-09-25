import os
import re
from pathlib import Path

def update_template():
    script_dir = Path(__file__).parent
    
    dist_dir = script_dir / "backend" / "frontend" / "admin-dashboard" / "dist"
    template_file = script_dir / "backend" / "templates" / "admin" / "dashboard.html"
    
    index_html = dist_dir / "index.html"
    if not index_html.exists():
        print("Build files not found. Run 'npm run build' first.")
        return
    
    content = index_html.read_text()
    
    js_match = re.search(r'/assets/(index-[^"]+\.js)', content)
    css_match = re.search(r'/assets/(index-[^"]+\.css)', content)
    
    if not js_match or not css_match:
        print("Could not find asset filenames in build")
        return
    
    js_file = js_match.group(1)
    css_file = css_match.group(1)
    
    template_content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>Projects Dashboard</title>
            {{% load static %}}
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="csrf-token" content="{{{{ csrf_token }}}}">
            <link rel="stylesheet" href="{{% static 'assets/{css_file}' %}}">
        </head>
        <body>
            <div id="root"></div>
            <script type="module" src="{{% static 'assets/{js_file}' %}}"></script>
        </body>
        </html>"""
    template_file.write_text(template_content)
    print(f"Template updated with {js_file} and {css_file}")

if __name__ == "__main__":
    update_template()