#!/usr/bin/python3
# -*- coding: utf-8 -*-


import psycopg2


PRAKTOMAT_ADMIN_ID = 623


def grade_solutions(regex_task, id_passed, id_failed):
    """Creates attestations for all OOP tutorial students.

    Parameters:
    regex_task - Regular expression describing the tasks to be graded
    id_passed - Ratingscaleitem used for passed assignments
    id_failed - Ratingscaleitem used for failed assignments

    """

    tasks = []
    query_grade_passed = """INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) SELECT now(), '', '', 't', 't', now(), {}, {}, solutions_solution.id FROM accounts_user, solutions_solution, tasks_task WHERE accounts_user.user_ptr_id = solutions_solution.author_id AND tasks_task.id = solutions_solution.task_id AND accounts_user.user_ptr_id = solutions_solution.author_id AND solutions_solution.final = 't' AND solutions_solution.accepted = 't' AND tasks_task.submission_date < now() AND tasks_task.id = (%s) AND NOT EXISTS (SELECT solution_id FROM attestation_attestation WHERE attestation_attestation.solution_id = solutions_solution.id);""".format(
        PRAKTOMAT_ADMIN_ID, id_passed
    )

    query_grade_failed = """INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) SELECT now(), '', '', 't', 't', now(), {}, {}, MAX(solutions_solution.id) FROM solutions_solution, accounts_user, tasks_task WHERE solutions_solution.author_id = accounts_user.user_ptr_id AND tasks_task.id = solutions_solution.task_id AND tasks_task.submission_date < now() AND tasks_task.id = (%s) AND solutions_solution.accepted = 'f' AND solutions_solution.author_id NOT IN (SELECT solutions_solution.author_id FROM solutions_solution WHERE accounts_user.user_ptr_id = solutions_solution.author_id AND tasks_task.id = solutions_solution.task_id AND accounts_user.user_ptr_id = solutions_solution.author_id AND solutions_solution.final = 't' AND solutions_solution.accepted = 't' AND tasks_task.id = (%s)) AND accounts_user.user_ptr_id NOT IN (SELECT solutions_solution.author_id FROM solutions_solution, attestation_attestation WHERE solutions_solution.id = attestation_attestation.solution_id AND solutions_solution.task_id = (%s)) GROUP BY accounts_user.user_ptr_id;""".format(
        PRAKTOMAT_ADMIN_ID, id_failed
    )

    query_get_tasks = (
        "SELECT id "
        "FROM tasks_task "
        "WHERE title SIMILAR TO '" + regex_task + "'"
        "ORDER BY id ASC; "
    )

    print("Praktomat Grading Tasks:", query_get_tasks)
    print("Praktomat Grading Grade Passed:", query_grade_passed)
    print("Praktomat Grading Grade Failed:", query_grade_failed)

    try:
        ps_conn = psycopg2.connect(
            "host=DB_HOST port=DB_PORT dbname=DB_NAME user=DB_USER password=DB_PASS"
        )
        ps_conn.autocommit = True
        cursor = ps_conn.cursor()
        cursor.execute(query_get_tasks)
        task_id = cursor.fetchone()

        while task_id is not None:
            tasks += task_id
            task_id = cursor.fetchone()

        for task in tasks:
            print("Task", task)
            args = (task, task, task)
            cursor.execute(query_grade_passed, args[:1])
            cursor.execute(query_grade_failed, args)

        cursor.close()
        ps_conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


grade_solutions("(OOP|ADP): H[0-9]{2}%", "22", "23")
grade_solutions("(OOP|ADP): Ü[0-9]{2}%", "1", "3")
