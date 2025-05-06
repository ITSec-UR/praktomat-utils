#!/usr/bin/python

from os import environ

from database import connect_db, run_sql


def limit_submissions(conn, task, max_upload):
    query_above = f"UPDATE solutions_solution SET accepted = 'f', final = 'f' WHERE number > {max_upload} AND task_id = {task};"

    query_max = f"UPDATE solutions_solution SET accepted = 't', final = 't' WHERE number = {max_upload} AND task_id = {task};"
    run_sql(conn, query_above)
    run_sql(conn, query_max)


def get_tasks(conn, regex_task):
    query_get_tasks = f"SELECT id FROM tasks_task WHERE title SIMILAR TO '{regex_task}' AND submission_date < now() AND publication_date > now() - INTERVAL '14 DAY'ORDER BY id ASC;"
    return run_sql(conn, query_get_tasks)


def run():
    max_uploads = int(environ.get('PRAKTOMAT_MAX_UPLOADS', 3))
    if max_uploads <= 0:
        print(f"Stop limit homework solutions due to PRAKTOMAT_MAX_UPLOADS = {max_uploads} <= 0")
        return

    print(f"Run Praktomat limit homework solutions to {max_uploads}")

    conn = connect_db()
    if not conn:
        print("No connection is established!")
        exit(1)

    if 'TASK_REGEX' in environ:
        task_regexes = [e.strip() for e in environ['TASK_REGEX'].split(',')]
    else:
        task_regexes = ["H[0-9]{2}%"]

    for task_regex in task_regexes:
        print(f"\t- {task_regex}")
        tasks = get_tasks(conn, task_regex)
        if tasks is None:
            raise ValueError(
                f"Couldn't find any tasks with task regex = {task_regex}")
        for task in tasks:
            limit_submissions(conn, task[0], max_uploads)
    conn.close()


if __name__ == '__main__':
    run()
