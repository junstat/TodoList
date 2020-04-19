# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 13:55
import argparse
from functools import wraps

from common import TaskOperator


def parse_argument(func):
    @wraps(func)
    def wrapper(wf):
        # build argument parser to parse script args and collect their
        # values
        parser = argparse.ArgumentParser()
        # add new task
        parser.add_argument('--add', dest='new_task', nargs='?', default=None)
        parser.add_argument('--del', dest='task_num', nargs='?', default=None)
        # parser.add_argument('--change', dest='change_num', nargs='?', default=None)
        # add an optional query and save it to 'query'
        parser.add_argument('query', nargs='?', default=None)
        args = parser.parse_args(wf.args)

        worker = TaskOperator()

        if args.new_task:
            worker.add_one_task(title=args.new_task)
            return 0

        if args.task_num:
            worker.del_one_task(args.task_num)
            return 0

        # if args.change_num:
        #     change_num = int(args.change_num)
        #     tasks[change_num].status = True
        #     dump_tasks(tasks)
        #     return 0
        return func(wf, worker)

    return wrapper
