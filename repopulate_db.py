"""Repobla db_testing con el schema y el seed (o verifica su estado).

Uso:
  python repopulate_db.py          # verifica tablas y repuebla si faltan/vacías
  python repopulate_db.py --force  # siempre re-ejecuta schema + seed

La BD de tests comparte db_testing: correr pytest dropea las tablas gg_*
(teardown del conftest) y las deja vacías. Este script restaura schema + seed.
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


async def count_tables(conn: asyncpg.Connection) -> int:
    # Solo cuentan las tablas de este proyecto (gg_*). La BD de tests la
    # comparten otros proyectos, así que contar TODAS las tablas haría que
    # `tables > 0` siempre fuese cierto y el script nunca repoblase.
    rows = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'gg_%'")
    return len(rows)


async def apply_sql(conn: asyncpg.Connection, path: str, label: str) -> None:
    if not os.path.exists(path):
        print(f"[ERROR] No existe {path}")
        sys.exit(1)
    sql = open(path, encoding="utf-8").read()
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

        await apply_sql(conn, SCHEMA, "Schema")
        await apply_sql(conn, SEED, "Seed")

        tables = await count_tables(conn)
        print(f"Repoblado. Tablas finales: {tables}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
