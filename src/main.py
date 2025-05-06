#!/usr/bin/python

from os import environ

import auto_grading
import limit_submissions

if __name__ == '__main__':
    if environ.get('LIMIT_SUBMISSIONS', 'false').lower() == 'true':
        limit_submissions.run()
    if environ.get('AUTO_GRADING', 'false').lower() == 'true':
        auto_grading.run()
