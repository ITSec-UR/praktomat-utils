import sys
import os
from pathlib import Path

import psycopg

from util import get_env_bool

VERBOSE = get_env_bool("VERBOSE", False)


def run_sql(conn, query, params=None):
    """
    Execute a SQL query with optional parameters.
    Logs the query in full if VERBOSE is enabled.
    Returns the result rows, or an empty list if no rows are returned.
    """
    try:
        with conn.cursor() as cursor:
            if VERBOSE:
                print(f"[SQL] Executing query: {query}")
                if params:
                    print(f"[SQL] With params: {params}")

            cursor.execute(query, params)
            if cursor.description:
                return cursor.fetchall()
            return cursor.rowcount
    except psycopg.DatabaseError as e:
        print(f"[SQL Error] {e}\nQuery: {query}\nParams: {params}", file=sys.stderr)
        return None


def connect_db():
    """
    Establish a PostgreSQL connection using environment variables.
    Returns a psycopg.Connection object with autocommit enabled.
    """

    pw_path = Path(os.environ["POSTGRES_PASSWORD"])
    db_pass = pw_path.read_text() if pw_path.exists() else os.environ["POSTGRES_PASSWORD"]

    try:
        conn = psycopg.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=db_pass
        )
        conn.autocommit = True
        return conn
    except psycopg.DatabaseError as e:
        print(f"[DB Connection Error] {e}", file=sys.stderr)
        sys.exit(1)
