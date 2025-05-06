#!/usr/bin/python


from os import environ

from database import connect_db, run_sql


def grade_solutions(conn, task, id_admin, id_passed, id_failed):
    """Creates attestations for all tutorial students.

    Parameters:
    conn - Connection to Database
    task - ID for task
    id_passed - Ratingscaleitem used for passed assignments
    id_failed - Ratingscaleitem used for failed assignments

    """

    query_grade_passed = """INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) SELECT now(), '', '', 't', 't', now(), {}, {}, solutions_solution.id FROM accounts_user, solutions_solution, tasks_task WHERE accounts_user.user_ptr_id = solutions_solution.author_id AND tasks_task.id = solutions_solution.task_id AND accounts_user.user_ptr_id = solutions_solution.author_id AND solutions_solution.final = 't' AND solutions_solution.accepted = 't' AND solutions_solution.plagiarism  = 'f' AND 't' IN (SELECT bool_and(passed) FROM checker_checkerresult WHERE solution_id = solutions_solution.id AND object_id NOT IN (SELECT id FROM checker_checkstylechecker)) AND tasks_task.id = {} AND NOT EXISTS (SELECT solution_id FROM attestation_attestation WHERE attestation_attestation.solution_id = solutions_solution.id);""".format(
        id_admin, id_passed, task
    )

    query_grade_failed = """INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) SELECT now(), '', '', 't', 't', now(), {}, {}, solutions_solution.id FROM accounts_user, solutions_solution, tasks_task WHERE accounts_user.user_ptr_id = solutions_solution.author_id AND tasks_task.id = solutions_solution.task_id AND accounts_user.user_ptr_id = solutions_solution.author_id AND solutions_solution.final = 't' AND solutions_solution.accepted = 't' AND (solutions_solution.plagiarism  = 't' OR 'f' IN (SELECT bool_and(passed) FROM checker_checkerresult WHERE solution_id = solutions_solution.id AND object_id NOT IN (SELECT id FROM checker_checkstylechecker))) AND tasks_task.id = {} AND NOT EXISTS (SELECT solution_id FROM attestation_attestation WHERE attestation_attestation.solution_id = solutions_solution.id);""".format(
        id_admin, id_failed, task
    )

    print(query_grade_passed)
    print(query_grade_failed)

    run_sql(conn, query_grade_passed)
    run_sql(conn, query_grade_failed)


def get_tasks(conn, regex_task, rating_scale, wait_days=5):
    query_get_tasks = "SELECT id FROM tasks_task WHERE title SIMILAR TO '{}' AND final_grade_rating_scale_id = {} AND submission_date < now() - INTERVAL '{} DAY' AND publication_date > now() - INTERVAL '{} DAY' ORDER BY id ASC;".format(
        regex_task, rating_scale, wait_days, wait_days + 30
    )
    print(query_get_tasks)
    return run_sql(conn, query_get_tasks)


def get_rating(conn, rating_name):
    query_get_rating = (
        "SELECT id FROM attestation_ratingscale WHERE name = '{}';".format(
            rating_name)
    )
    print(query_get_rating)
    rating = run_sql(conn, query_get_rating)[0][0]

    query_rating_item = "SELECT id FROM attestation_ratingscaleitem WHERE scale_id = {} AND position < 2 ORDER BY position ASC;".format(
        rating
    )
    print(query_rating_item)
    result = run_sql(conn, query_rating_item)
    id_failed, id_passed = [r[0] for r in result]
    return rating, id_failed, id_passed


def run():
    id_admin = environ.get("PRAKTOMAT_ADMIN_ID", 1)
    wait_days = int(environ.get("WAIT_DAYS", 5))
    print(f"Run Praktomat grade solutions for PRAKTOMAT_ADMIN_ID = {id_admin}")
    conn = connect_db()
    if not conn:
        print("No connection is established!")
        exit(1)

    if 'TASK_REGEX' in environ:
        task_regexes = [e.strip() for e in environ['TASK_REGEX'].split(',')]
    else:
        task_regexes = ["H[0-9]{2}%", "Ü[0-9]{2}%"]

    ratings = [e.strip() for e in environ["RATING_REGEX"].split(',')]

    for rating_regex in ratings:
        rating_scale, id_failed, id_passed = get_rating(conn, rating_regex)
        for task_regex in task_regexes:
            print(f"Task = {task_regex} Rating = {rating_regex}")
            tasks = get_tasks(conn, task_regex, rating_scale, wait_days)
            for task in tasks:
                grade_solutions(conn, task[0], id_admin, id_passed, id_failed)
    conn.close()


if __name__ == '__main__':
    run()
