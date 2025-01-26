# 001 - Database Migration Process Established

**Date:** 2024-01-25

## What Changed

- Established a standardized process for managing database migrations with Neon PostgreSQL
- Created comprehensive documentation for database migrations in `docs/dev/database_migrations.md`
- Updated database schema to support:
  - JSON-based exercise storage in workouts
  - Improved tracking with `updated_at` timestamps
  - More flexible training plan structure
  - Enhanced exercise type descriptions
- Added development data population script with proper Neon compatibility
- Implemented proper handling of pooled vs unpooled connections for migrations

## Why

1. **Reliability**: Standardized process reduces risk of migration errors and data loss
2. **Maintainability**: Clear documentation ensures consistent practices across the team
3. **Scalability**: Proper connection handling supports growth in data volume
4. **Development Efficiency**: Sample data population script speeds up development and testing

## Technical Details

### Migration Changes
- Moved from separate `workout_exercises` table to JSON storage in `workouts`
- Added `updated_at` timestamps across all tables
- Made training plan dates nullable for draft plans
- Added exercise descriptions and removed generic parameters
- Implemented proper foreign key relationships for training blocks

### Infrastructure Updates
- Using unpooled connections for migrations (`DATABASE_URL_UNPOOLED`)
- Added proper SSL/TLS configuration for Neon
- Implemented connection string format conversion (postgres:// → postgresql://)

### Development Tools
- Added `clear_existing_data()` function for clean slate development
- Created structured sample data population
- Implemented proper error handling and rollback support

## Migration Commands
```bash
# Create migration
flask db migrate -m "update schema to match current models"

# Apply migration
flask db upgrade

# Populate development data
python api/scripts/populate_dev_db.py
```

## Related Files
- `api/migrations/versions/4b2ad13f471c_update_schema_to_match_current_models.py`
- `api/scripts/populate_dev_db.py`
- `docs/dev/database_migrations.md`
- `api/core/models.py` 