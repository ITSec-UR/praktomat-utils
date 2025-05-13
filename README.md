# 🐳 Dockerfile for Managing Praktomat Submissions

⚠️ **Warning:** This container directly interacts with the Praktomat database (performing Create, Read, Update, and Delete operations). It is intended to run as a scheduled **cron job**, e.g., every Monday at 03:00 (`0 3 * * 1`).

To connect to the database, the following environment variables **must** be provided:

- `POSTGRES_DB`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

---

## 📦 Supported Utility Modules

### 1. ⛔ Limit Submissions

This module limits the number of submissions per student. Any additional submissions beyond the allowed maximum are marked as not accepted and not final. Note: Exceeding submissions are **not deleted**.

#### Environment Variables

- `LIMIT_SUBMISSIONS`: Set to `True` to enable this module
- `PRAKTOMAT_MAX_UPLOADS`: Maximum number of allowed submissions
- `TASK_REGEX`: Apply this module only to tasks matching this regex. Multiple comma-separated regex patterns are supported (default: `*`)

---

### 2. 🤖 Auto Grading

This module automatically grades tasks using an admin account. It is designed for environments where automated grading is meaningful. The grading scheme should be binary: **0 = fail**, **1 = pass**.

#### Environment Variables

- `AUTO_GRADING`: Set to `True` to enable this module
- `PRAKTOMAT_ADMIN_ID`: ID of the admin account issuing attestations (commonly `1`; verify via: `SELECT id FROM auth_user WHERE username = 'praktomat';`)
- `PRAKTOMAT_ADMIN_NAME`: Alternative to `PRAKTOMAT_ADMIN_ID`; searches for an admin account by username
- `RATING_NAME`: Optional. Only apply grading to tasks with a rating scale matching this name. Multiple comma-separated values supported (default: `*`)
- `TASK_REGEX`: Optional. Only apply grading to tasks matching this regex. Multiple comma-separated values supported (default: `*`)
- `WAIT_DAYS`: Number of days after a task's submission date before grading begins (default: `5`)
- `INTERVAL_DAYS`: Time window (in days) to look back for eligible tasks to grade (default: `30`)
- `WORK_DATA`: Filesystem path to submitted solution files, used to generate annotated feedback (default: `/work-data`)
