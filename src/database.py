from os import environ

import psycopg


def run_sql(conn, sql):
    print(sql)

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        cursor.close()
        return results
    except psycopg.DatabaseError as error:
        print(error)


def connect_db():
    try:
        ps_conn = psycopg.connect(
            "host={} port={} dbname={} user={} password={}".format(
                environ["POSTGRES_HOST"],
                environ["POSTGRES_PORT"],
                environ["POSTGRES_DB"],
                environ["POSTGRES_USER"],
                environ["POSTGRES_PASSWORD"],
            )
        )
        ps_conn.autocommit = True
        return ps_conn
    except psycopg.DatabaseError as error:
        print(error)
