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


if __name__ == '__main__':
    unittest.main()
