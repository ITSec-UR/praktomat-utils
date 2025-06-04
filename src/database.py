import os
import sys
from pathlib import Path

import psycopg
from psycopg import sql

from util import get_env_bool

VERBOSE = get_env_bool("VERBOSE", False)


def format_query_for_debug(query, params):
    """
    Safely format the query string with parameters for debugging,
    using psycopg.sql.Literal to escape params properly.
    """
    if not params:
        return query

    # Build a list of Literals corresponding to params
    literals = [sql.Literal(p) for p in params]

    try:
        # Format the query with literals
        # Note: this assumes %s placeholders (standard psycopg)
        # but psycopg.sql.SQL.format uses {} placeholders, so we replace %s with {} here
        formatted_query = query.replace('%s', '{}')
        composed = sql.SQL(formatted_query).format(*literals)
        return composed.as_string(None)  # None because no actual connection needed for formatting
    except Exception as e:
        return f"[SQL Error] {e}"


def run_sql(conn, query, params=None):
    """
    Execute a SQL query with optional parameters.
    Logs the query in full if VERBOSE is enabled.
    Returns the result rows, or an empty list if no rows are returned.
    """
    try:
        with conn.cursor() as cursor:
            if VERBOSE:
                full_query = format_query_for_debug(query, params)
                print(f"[SQL] {full_query}")

            cursor.execute(query, params)
            if cursor.description:
                return cursor.fetchall()
            return cursor.rowcount
    except psycopg.DatabaseError as e:
        print(f"[SQL Error] {e}\nQuery: {query}\nParams: {params}", file=sys.stderr)
        return []


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
