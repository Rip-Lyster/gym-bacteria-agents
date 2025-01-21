import os
import shutil
from pathlib import Path

def create_env_files():
    """Create and set up environment files for development and production."""
    api_dir = Path(__file__).parent.parent
    
    # Template for development environment
    dev_template = """# Development Environment
# Get these values from Vercel Dashboard -> Storage -> Postgres -> .env.local tab
POSTGRES_URL=
POSTGRES_PRISMA_URL=
POSTGRES_URL_NON_POOLING=
POSTGRES_USER=
POSTGRES_HOST=
POSTGRES_PASSWORD=
POSTGRES_DATABASE=

# Flask settings
FLASK_ENV=development
FLASK_DEBUG=1
"""

    # Template for production environment
    prod_template = """# Production Environment
# These will be automatically set by Vercel in production
POSTGRES_URL=
POSTGRES_PRISMA_URL=
POSTGRES_URL_NON_POOLING=
POSTGRES_USER=
POSTGRES_HOST=
POSTGRES_PASSWORD=
POSTGRES_DATABASE=

FLASK_ENV=production
FLASK_DEBUG=0
"""

    # Create .env.development.local if it doesn't exist
    dev_env_path = api_dir / '.env.development.local'
    if not dev_env_path.exists():
        with open(dev_env_path, 'w') as f:
            f.write(dev_template)
        print(f"Created {dev_env_path}")
    else:
        print(f"{dev_env_path} already exists")

    # Create .env.production.local if it doesn't exist
    prod_env_path = api_dir / '.env.production.local'
    if not prod_env_path.exists():
        with open(prod_env_path, 'w') as f:
            f.write(prod_template)
        print(f"Created {prod_env_path}")
    else:
        print(f"{prod_env_path} already exists")

    # Create .env that points to development by default
    env_path = api_dir / '.env'
    if not env_path.exists():
        shutil.copy2(dev_env_path, env_path)
        print(f"Created {env_path} (copied from development)")
    else:
        print(f"{env_path} already exists")

    print("\nEnvironment files created/checked.")
    print("\nTo get your development database credentials:")
    print("1. Go to Vercel Dashboard")
    print("2. Select your project")
    print("3. Go to Storage -> Postgres")
    print("4. Click '.env.local' tab")
    print("5. Copy all environment variables to .env.development.local")
    print("\nTo switch between environments:")
    print("- Development: cp .env.development.local .env")
    print("- Production: cp .env.production.local .env")

if __name__ == "__main__":
    create_env_files() 