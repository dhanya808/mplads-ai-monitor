import os

os.makedirs('api', exist_ok=True)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write('''import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app
''')

with open('vercel.json', 'w', encoding='utf-8') as f:
    f.write('''{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/login",
      "dest": "/frontend/login.html"
    },
    {
      "src": "/dashboard",
      "dest": "/frontend/index.html"
    },
    {
      "src": "/static/(.*)",
      "dest": "/frontend/$1"
    },
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/",
      "dest": "/frontend/index.html"
    }
  ]
}
''')

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write('''cloudflared.exe
__pycache__/
*.pyc
.env
.venv/
env/
''')

print('Vercel configuration created successfully!')
