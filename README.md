# Dockerfile for managing Praktomat submissions
Warning: This container interacts directly with Praktomat's database (CRUD operations). It should run as a cron job, e.g. every Monday 03:00 (0 3 * * 1). For the database connection it needs the following environment variables.
- `POSTGRES_DB`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

The following util modules are supported.

## Limit submissions
This module limits the students' submissions by setting all solutions with a higher number to not accepted and not final. All submissions that exceed the maximum number will explicitly not be deleted. The following environment variables can be set.
- `LIMIT_SUBMISSIONS`: Set to `True` to enable this module
- `PRAKTOMAT_MAX_UPLOADS`: Limit submissions to this number
- `TASK_REGEX`: Only applies this module to tasks that are similar to this variable. Can contain multiple regex statements separated by commas (default: `H[0-9]{2}%`)

## Auto grading
This module automatically grades task with admin account. This module should only be used if automated grading makes sense. The grading scheme should be binary, 0 for fail, 1 for pass. The following environment variables can be set.
- `AUTO_GRADING`: Set to `True` to enable this module
- `PRAKTOMAT_ADMIN_ID`: ID for admin account which is used for issuing the attestations (usually id=1 but you can verify with `select id from auth_user where username='praktomat';`)
- `PRAKTOMAT_ADMIN_NAME`: Search for ID for an admin account. It is an alternative to `PRAKTOMAT_ADMIN_ID` if the ID is not known
- `RATING_REGEX`: Only applies this module to tasks with this rating scale (name). Can contain multiple regex statements separated by commas
- `TASK_REGEX`: Only applies this module to tasks that are similar to this variable. Can contain multiple regex statements separated by commas (default: `H[0-9]{2}%", "Ü[0-9]{2}%`)
- `WAIT_DAYS`: Specifies how long the task should be expired until the module is applied. This should enable tutors to change the assessment scale before automated assessment, e.g. homework to SBL (default: 5)
