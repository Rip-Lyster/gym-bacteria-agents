# Database Migrations Guide

This guide outlines the process for managing database migrations in the Gym Bacteria project using Flask-Migrate with Neon PostgreSQL.

## Prerequisites

- Access to the Neon project dashboard
- Python environment with required packages installed (`requirements.txt`)
- `.env.development.local` file with proper Neon database credentials

## Important Notes

1. **Always use unpooled connections for migrations**
   - Neon provides both pooled and unpooled connection strings
   - Use `DATABASE_URL_UNPOOLED` for migrations to avoid connection pool issues
   - Use `DATABASE_URL` (pooled) for regular application operations

2. **Database URLs**
   - Neon provides URLs starting with `postgres://`
   - SQLAlchemy requires URLs starting with `postgresql://`
   - Our configuration automatically handles this conversion

## Migration Process

### 1. Creating a New Migration

When you need to make changes to the database schema:

```bash
# Make sure you're in the api directory
cd api

# Set the Flask application
export FLASK_APP=app.py

# Create a new migration
flask db migrate -m "description of your changes"
```

The migration will be created in `api/migrations/versions/`.

### 2. Reviewing the Migration

Always review the generated migration file before applying it:
- Check that all intended changes are included
- Verify foreign key constraints
- Consider data preservation needs
- Test both upgrade and downgrade paths

### 3. Applying Migrations

To apply pending migrations:

```bash
# Apply migrations
flask db upgrade

# If you need to rollback
flask db downgrade
```

### 4. Handling Data

If you need to preserve existing data:
1. Create a data backup before migration
2. Modify the migration to handle data transformation
3. Test the migration on a development database first

If you don't need to preserve data:
1. Clear existing data using `populate_dev_db.py`'s `clear_existing_data()` function
2. Repopulate with fresh sample data

### 5. Populating Development Data

After applying migrations, you can populate the database with fresh development data:

```bash
# From the project root
python api/scripts/populate_dev_db.py
```

## Common Issues and Solutions

### 1. Connection Issues
```
Error: connection to server at "ep-xyz-123.region.aws.neon.tech" failed
```
- Verify your `.env.development.local` has the correct credentials
- Check if you're using the right connection string (pooled vs unpooled)
- Verify SSL/TLS settings (`sslmode=require`)

### 2. Migration Errors
```
Error: Target database is not up to date
```
- Run `flask db history` to see migration state
- Run `flask db current` to see current revision
- Use `flask db stamp head` to mark all migrations as applied (use with caution)

### 3. Data Integrity Issues
```
Error: violates foreign key constraint
```
- Ensure you're dropping/creating tables in the correct order
- Use `CASCADE` in your constraints where appropriate
- Consider using `clear_existing_data()` and repopulating

## Best Practices

1. **Version Control**
   - Always commit migration files to version control
   - Include both the migration file and corresponding model changes in the same commit
   - Add descriptive commit messages explaining the schema changes

2. **Testing**
   - Test migrations on a development database first
   - Verify both upgrade and downgrade paths
   - Test with realistic data volumes

3. **Documentation**
   - Update API documentation when schema changes
   - Document any required application changes
   - Add migration notes to changelog

4. **Backup**
   - Always backup production data before migrations
   - Keep rollback scripts ready
   - Test restore procedures

## Useful Commands

```bash
# View migration history
flask db history

# View current migration state
flask db current

# Create a new migration
flask db migrate -m "description"

# Apply migrations
flask db upgrade

# Rollback one migration
flask db downgrade

# Mark migrations as complete without running them
flask db stamp head
```

## Related Files

- `api/migrations/env.py` - Migration environment configuration
- `api/core/models.py` - SQLAlchemy models
- `api/scripts/populate_dev_db.py` - Development data population
- `.env.development.local` - Database credentials

## Additional Resources

- [Neon Documentation](https://neon.tech/docs/guides/sqlalchemy-migrations)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/) 