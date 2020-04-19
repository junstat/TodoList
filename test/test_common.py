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

    def test_task_status_reverse(self):
        self.worker.task_status_reverse(job_type="doing", task_num=str(0))
        print self.worker.tasks[1]

    def test_set_order(self):
        self.worker.set_order("4 3 1 2")
        print self.worker.tasks


if __name__ == '__main__':
    unittest.main()
