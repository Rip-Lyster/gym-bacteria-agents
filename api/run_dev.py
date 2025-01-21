import os
import sys
from pathlib import Path

def setup_dev_env():
    """Set up development environment variables."""
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['FLASK_HOST'] = 'localhost'
    os.environ['FLASK_PORT'] = '5328'

    # Add the project root to Python path
    project_root = str(Path(__file__).parent.parent)
    sys.path.insert(0, project_root)

if __name__ == '__main__':
    setup_dev_env()
    from api.app import run_app
    run_app() 