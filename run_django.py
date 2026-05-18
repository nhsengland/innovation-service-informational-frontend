import os
import sys
from pathlib import Path

def load_env(env_path):
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            os.environ[key] = value

if __name__ == "__main__":
    project_root = Path(__file__).parent
    load_env(project_root / ".env")
    
    # Set default settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "is_homepage.settings.dev")
    
    from django.core.management import execute_from_command_line
    
    # Run the command
    execute_from_command_line(sys.argv)
