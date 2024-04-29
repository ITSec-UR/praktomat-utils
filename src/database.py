from os import environ

import psycopg2


def run_sql(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = [record for record in cursor]

        cursor.close()
        return results
    except psycopg2.DatabaseError as error:
        print(error)


def connect_db():
    try:
        ps_conn = psycopg2.connect(
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
    except psycopg2.DatabaseError as error:
        print(error)
