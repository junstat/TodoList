#!/usr/bin/python
# encoding: utf-8
import argparse
import os
import sys

from workflow import Workflow

reload(sys)
sys.setdefaultencoding("utf-8")

DEFAULT_FILE_PATH = os.path.expanduser('~/Todolist/demo.txt')

DOING_ICON = "./icons/time.png"


class Task(object):

    def __init__(self, title=None, status=False):
        self.title = title
        self.status = status

    def revers_status(self):
        self.status = not self.status

    def reset_status(self):
        if self.status:
            self.reset_status()

    def __repr__(self):
        return "{} [{}]".format(self.title, self.status)


def load_tasks(file_path=DEFAULT_FILE_PATH):
    tasks = []
    with open(file_path) as f:
        for line in f:
            if not line.strip():
                continue
            tasks.append(Task(
                title=line.replace("-", "").strip(),
                status=line.startswith("-"),  # True: done, False: doing
            ))
    return tasks


def dump_tasks(tasks, file_path=DEFAULT_FILE_PATH):
    with open(file_path, "w") as f:
        for task in tasks:
            status_flag = "- " if task.status else ""
            f.write("{}{}\n".format(status_flag, task.title))


def main(wf):
    tasks = load_tasks()
    parser = argparse.ArgumentParser()
    # add new task
    parser.add_argument('--add', dest='new_task', nargs='?', default=None)
    parser.add_argument('--del', dest='task_num', nargs='?', default=None)
    parser.add_argument('--change', dest='cha_num', nargs='?', default=None)
    # add an optional query and save it to 'query'
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    if args.new_task:
        tasks.append(Task(title=args.new_task))
        dump_tasks(tasks)
        return 0
    elif args.task_num:
        task_num = int(args.task_num)
        if task_num > 0:
            task_num = task_num - 1  # 位序转换为下标
        tasks.pop(task_num)
        dump_tasks(tasks)
        return 0
    elif args.cha_num:
        cha_num = int(args.cha_num)
        if cha_num > 0:
            cha_num = cha_num - 1  # 位序转换为下标
        tasks[cha_num].status = True
        dump_tasks(tasks)
        return 0

    for num, task in enumerate(tasks):
        sta = "done" if task.status else "doing"
        wf.add_item(
            title=task.title,
            subtitle="status:[{}] order:[{}]".format(sta, num + 1),
            valid=True,
            arg=str(num),
            icon=DOING_ICON
        )

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
