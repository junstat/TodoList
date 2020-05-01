# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 13:55
import argparse
import sys
from functools import wraps

from common import TaskOperator


def search_key_for_task(task):
    return unicode(task.title)


def parse_argument(func):
    @wraps(func)
    def wrapper(wf):
        worker = TaskOperator.get_instance()

        # build argument parser to parse script args and collect their values
        parser = argparse.ArgumentParser()
        parser.add_argument('--exchange', action="append")
        parser.add_argument('--add', dest='new_task', nargs='?', default=None)  # add new task
        parser.add_argument('--reset', action="store_true")
        parser.add_argument('--change_title', action="append")
        parser.add_argument('--del_done', dest='del_done_num', nargs='?', default=None)
        parser.add_argument('--del_doing', dest='del_doing_num', nargs='?', default=None)
        parser.add_argument('--set_done', dest='set_done_num', nargs='?', default=None)
        parser.add_argument('--set_doing', dest='set_doing_num', nargs='?', default=None)
        parser.add_argument('--order', dest='orders', nargs='?', default=None)
        # add an optional query and save it to 'query'
        parser.add_argument('query', nargs='?', default=None)
        args = parser.parse_args(wf.args)

        query = args.query
        if query:
            worker.filter_tasks = wf.filter(query, worker.tasks, key=search_key_for_task)
        else:
            worker.filter_tasks = worker.tasks

        sys.stderr.write("args = {}\n".format(args))
        if args.new_task:
            worker.add_one_task(title=args.new_task)
            return 0
        elif args.set_done_num:  # set done
            worker.task_status_reverse(job_type="done", task_num=args.set_done_num)
            return 0
        elif args.set_doing_num:  # set doing
            worker.task_status_reverse(job_type="doing", task_num=args.set_doing_num)
            return 0
        elif args.del_done_num:
            worker.del_one_task("done", args.del_done_num)
            return 0
        elif args.del_doing_num:
            worker.del_one_task("doing", args.del_done_num)
            return 0
        elif args.orders:
            worker.set_order(orders=args.orders)
            return 0
        elif args.change_title:
            task_num, new_title = args.change_title
            worker.change_task_title(task_num, new_title)
            return 0
        elif args.reset:
            worker.reset_tasks()
            return 0
        elif args.exchange:
            from_num, to_num = args.exchange
            worker.exchange_tasks(from_num, to_num)
            return 0
        return func(wf)

    return wrapper


'''
def singleton(cls):
    """
    Singleton decorate
    :param cls:
    :return:
    """
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner
'''
