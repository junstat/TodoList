# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 14:00

import unittest

from common import TaskOperator


class TaskOperatorTest(unittest.TestCase):

    def setUp(self):
        self.worker = TaskOperator()

    def test_sort_tasks(self):
        self.worker.sort_tasks()
        for task in self.worker.tasks:
            print task

    def test_task_finished(self):
        self.worker.status_reverse(job_type="doing", task_num=str(0))
        print self.worker.tasks[1]


if __name__ == '__main__':
    unittest.main()
