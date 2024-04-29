#!/usr/bin/python

from os import environ

import auto_grading
import limit_submissions

if __name__ == '__main__':
    if environ.get('LIMIT_SUBMISSIONS') == 'True':
        limit_submissions.run()
    if environ.get('AUTO_GRADING') == 'True':
        auto_grading.run()
