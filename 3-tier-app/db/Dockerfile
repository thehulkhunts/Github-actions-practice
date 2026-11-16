FROM postgres:16-alpine
# Scripts in this folder run once, on first start with an empty data directory
COPY init.sql /docker-entrypoint-initdb.d/init.sql
EXPOSE 5432
# Set POSTGRES_USER, POSTGRES_PASSWORD and POSTGRES_DB at runtime
