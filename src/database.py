import sys
from os import environ

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
            return []
    except psycopg.DatabaseError as e:
        print(f"[SQL Error] {e}\nQuery: {query}\nParams: {params}", file=sys.stderr)
        return []


def connect_db():
    """
    Establish a PostgreSQL connection using environment variables.
    Returns a psycopg.Connection object with autocommit enabled.
    """
    try:
        conn = psycopg.connect(
            host=environ["POSTGRES_HOST"],
            port=environ["POSTGRES_PORT"],
            dbname=environ["POSTGRES_DB"],
            user=environ["POSTGRES_USER"],
            password=environ["POSTGRES_PASSWORD"]
        )
        conn.autocommit = True
        return conn
    except psycopg.DatabaseError as e:
        print(f"[DB Connection Error] {e}", file=sys.stderr)
        sys.exit(1)
