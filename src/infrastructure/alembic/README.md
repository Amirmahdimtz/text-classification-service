# Alembic foundation

There are intentionally **no revision files** in `versions/`. Physical taxonomy, report, classification, audit, and identity schemas remain blocked by DEC-01/02/06/07/08/11. `Base.metadata` therefore has no application tables. Do not run `revision --autogenerate` against a production database until an approved physical schema and reviewed model imports exist. No schema upgrade, drift check, or rollback has been verified on PostgreSQL in the current execution environment.
