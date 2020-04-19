# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 13:55
import argparse
import sys
from functools import wraps

from common import TaskOperator


def parse_argument(func):
    @wraps(func)
    def wrapper(wf):
        # build argument parser to parse script args and collect their values
        parser = argparse.ArgumentParser()
        parser.add_argument('--add', dest='new_task', nargs='?', default=None)  # add new task
        parser.add_argument('--del', dest='del_num', nargs='?', default=None)
        parser.add_argument('--done', dest='done_num', nargs='?', default=None)
        parser.add_argument('--doing', dest='doing_num', nargs='?', default=None)
        # add an optional query and save it to 'query'
        parser.add_argument('query', nargs='?', default=None)
        args = parser.parse_args(wf.args)

        worker = TaskOperator()

        sys.stderr.write("args = {}\n".format(args))
        if args.new_task:
            worker.add_one_task(title=args.new_task)
            return 0
        elif args.del_num:
            worker.del_one_task(args.task_num)
            return 0
        elif args.done_num:  # set done
            worker.task_status_reverse(job_type="done", task_num=args.done_num)
            return 0
        elif args.doing_num:  # set doing
            worker.task_status_reverse(job_type="doing", task_num=args.doing_num)
            return 0

        return func(wf, worker)

    return wrapper
