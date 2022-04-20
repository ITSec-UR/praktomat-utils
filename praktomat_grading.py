#!/usr/bin/python3
# -*- coding: utf-8 -*-


import psycopg2
import os

PRAKTOMAT_ADMIN_ID = os.environ["PRAKTOMAT_ADMIN_ID"]


def grade_solutions(conn, task, id_passed, id_failed):
    """Creates attestations for all OOP tutorial students.

    Parameters:
    conn - Connection to Database
    task - ID for task
    id_passed - Ratingscaleitem used for passed assignments
    id_failed - Ratingscaleitem used for failed assignments

    """
    query_grade_passed = """INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) SELECT now(), '', '', 't', 't', now(), {}, {}, solutions_solution.id FROM accounts_user, solutions_solution, tasks_task WHERE accounts_user.user_ptr_id = solutions_solution.author_id AND tasks_task.id = solutions_solution.task_id AND accounts_user.user_ptr_id = solutions_solution.author_id AND solutions_solution.final = 't' AND solutions_solution.accepted = 't' AND tasks_task.id = {} AND NOT EXISTS (SELECT solution_id FROM attestation_attestation WHERE attestation_attestation.solution_id = solutions_solution.id);""".format(
        PRAKTOMAT_ADMIN_ID, id_passed, task
    )

    query_grade_failed = """INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) SELECT now(), '', '', 't', 't', now(), {}, {}, MAX(solutions_solution.id) FROM solutions_solution, accounts_user, tasks_task WHERE solutions_solution.author_id = accounts_user.user_ptr_id AND tasks_task.id = solutions_solution.task_id AND tasks_task.id = {} AND solutions_solution.accepted = 'f' AND solutions_solution.author_id NOT IN (SELECT solutions_solution.author_id FROM solutions_solution WHERE accounts_user.user_ptr_id = solutions_solution.author_id AND tasks_task.id = solutions_solution.task_id AND accounts_user.user_ptr_id = solutions_solution.author_id AND solutions_solution.final = 't' AND solutions_solution.accepted = 't' AND tasks_task.id = {}) AND accounts_user.user_ptr_id NOT IN (SELECT solutions_solution.author_id FROM solutions_solution, attestation_attestation WHERE solutions_solution.id = attestation_attestation.solution_id AND solutions_solution.task_id = {}) GROUP BY accounts_user.user_ptr_id;""".format(
        PRAKTOMAT_ADMIN_ID, id_failed, task, task, task
    )

    print(query_grade_passed)
    print(query_grade_failed)

    run_sql(conn, query_grade_passed)
    run_sql(conn, query_grade_failed)


def get_tasks(conn, regex_task, rating_scale):
    query_get_tasks = "SELECT id FROM tasks_task WHERE title SIMILAR TO '{}' AND final_grade_rating_scale_id = {} AND submission_date < now() AND publication_date > now() - INTERVAL '14 DAY'ORDER BY id ASC;".format(
        regex_task, rating_scale
    )
    print(query_get_tasks)
    return run_sql(conn, query_get_tasks)


def get_rating(conn, rating_name):
    query_get_rating = (
        "SELECT id FROM attestation_ratingscale WHERE name = '{}';".format(rating_name)
    )
    print(query_get_rating)
    rating = run_sql(conn, query_get_rating)[0][0]

    query_rating_item = "SELECT id FROM attestation_ratingscaleitem WHERE scale_id = {} AND position < 2 ORDER BY position ASC;".format(
        rating
    )
    result = run_sql(conn, query_rating_item)
    id_failed, id_passed = [r[0] for r in result]
    return rating, id_failed, id_passed


def run_sql(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = [record for record in cursor]

        cursor.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def connect_db():
    try:
        ps_conn = psycopg2.connect(
            "host={} port={} dbname={} user={} password={}".format(
                os.environ["DB_HOST"],
                os.environ["DB_PORT"],
                os.environ["DB_NAME"],
                os.environ["DB_USER"],
                os.environ["DB_PASS"],
            )
        )
        ps_conn.autocommit = True
        return ps_conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


print("Run Praktomat grade solutions")

conn = connect_db()
if not conn:
    print("No connection is established!")
    exit(1)

regexes = ["(OOP|ADP): H[0-9]{2}%", "(OOP|ADP): Ü[0-9]{2}%"]
ratings = [os.environ["PRAKTOMAT_HOMEWORK"], os.environ["PRAKTOMAT_EXERCISE"]]

for title_regex, rating_scale in zip(regexes, ratings):
    rating_scale, id_failed, id_passed = get_rating(conn, rating_scale)
    tasks = get_tasks(conn, title_regex, rating_scale)
    for task in tasks:
        grade_solutions(conn, task[0], id_passed, id_failed)
conn.close()
