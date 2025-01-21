# Development Documentation

This directory contains documentation specific to development setup and processes.

## Contents

### [Database Setup](./database.md)
- Environment configuration
- Sample data population
- Development scripts
- Best practices and troubleshooting

## Development Environment

### Prerequisites
- Python 3.12.8 or compatible
- Node.js v18.16.1
- PostgreSQL (via Vercel Postgres)

### Quick Start
1. Set up environment:
   ```bash
   python api/scripts/config_env.py
   ```

2. Configure database credentials from Vercel Dashboard

3. Populate development database:
   ```bash
   python api/scripts/populate_dev_db.py
   ```

### Development Tools
- **Environment Management**: `config_env.py`
- **Database Tools**: 
  - `populate_dev_db.py` - Create sample data
  - `check_db.py` - Verify database connection

## Best Practices
1. Always use development environment for local work
2. Keep environment files out of version control
3. Use sample data for testing
4. Document new development processes in this directory 