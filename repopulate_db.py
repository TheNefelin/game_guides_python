"""Repobla db_testing con el schema y el seed (o verifica su estado).

Uso:
  python repopulate_db.py          # verifica tablas y repuebla si faltan/vacías
  python repopulate_db.py --force  # siempre re-ejecuta schema + seed

La BD de tests comparte db_testing: correr pytest ejecuta drop_all del
conftest y deja la BD sin tablas. Este script restaura schema + seed.
"""
import argparse
import asyncio
import os
import sys

import asyncpg

DSN = os.getenv("REPOPULATE_DATABASE_URL", "postgresql://testing:testing@localhost:5432/db_testing")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(BASE_DIR, "postgre_schema.sql")
SEED = os.path.join(BASE_DIR, "postgre_seed.sql")

SCHEMA_START = "-- Drop existentes"


async def count_tables(conn: asyncpg.Connection) -> int:
    rows = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    return len(rows)


async def apply_sql(conn: asyncpg.Connection, path: str, label: str, start_at: str | None = None) -> None:
    if not os.path.exists(path):
        print(f"[ERROR] No existe {path}")
        sys.exit(1)
    sql = open(path, encoding="utf-8").read()
    if start_at and start_at in sql:
        sql = sql[sql.index(start_at):]
    await conn.execute(sql)
    print(f"[OK] {label}: {os.path.basename(path)}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Verifica y repuebla db_testing con schema + seed")
    parser.add_argument("--force", action="store_true", help="Re-ejecuta schema + seed aunque haya tablas")
    args = parser.parse_args()

    conn = await asyncpg.connect(DSN)
    try:
        tables = await count_tables(conn)
        print(f"Tablas en '{DSN.split('/')[-1]}': {tables}")

        if tables > 0 and not args.force:
            print("La BD ya tiene tablas. Nada que hacer (usa --force para re-poblar).")
            return

        await apply_sql(conn, SCHEMA, "Schema", start_at=SCHEMA_START)
        await apply_sql(conn, SEED, "Seed")

        tables = await count_tables(conn)
        print(f"Repoblado. Tablas finales: {tables}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
