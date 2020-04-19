# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 12:53
import os

DEFAULT_FILE_PATH = os.path.expanduser('~/Todolist/demo.txt')

DOING_ICON = "./icons/doing.png"
DONE_ICON = "./icons/done.png"


class Task(object):

    def __init__(self, title=None, status=False, display_num=None):
        self.title = title
        self._status = status
        self.display_num = display_num

    def set_done(self):
        if not self._status:
            self._status = True

    @property
    def status(self):
        # True: done, False: doing
        return "done" if self._status else "doing"

    @status.setter
    def status(self, value):
        self._status = value

    def __repr__(self):
        return "Task No.{num}:{title} [{status}]".format(
            num=self.display_num, title=self.title, status=self.status
        )


class TaskOperator(object):

    def __init__(self):
        self._tasks = []
        self._doing_task_nums = 0
        self.load_tasks()
        self.sort_tasks()

    @property
    def tasks(self):
        self.sort_tasks()
        return self._tasks

    def add_one_task(self, title):
        self._tasks.append(Task(title))
        self.dump_tasks()

    def del_one_task(self, task_num):
        if isinstance(task_num, str):
            task_num = int(task_num)
        self._tasks.pop(task_num)
        self.dump_tasks()

    def sort_tasks(self):
        self._tasks.sort(key=lambda x: x.display_num)

    def load_tasks(self, file_path=DEFAULT_FILE_PATH):
        with open(file_path) as f:
            for line in f:
                if not line.strip():
                    continue
                status = line.startswith("-")  # True: done, False: doing
                display_num = len(self._tasks)

                # status == False, and exist done tasks
                if not status and self._doing_task_nums != len(self._tasks):
                    # adjust the done tasks' display num to make room for new doing task
                    reversed_done_tasks = reversed([task for task in self._tasks if task.status == "done"])
                    for task in reversed_done_tasks:
                        task.display_num += 1
                    display_num = self._doing_task_nums
                    self._doing_task_nums += 1

                self._tasks.append(Task(
                    title=line.replace("-", "").strip(),
                    status=status,
                    display_num=display_num
                ))

    def dump_tasks(self, file_path=DEFAULT_FILE_PATH):
        with open(file_path, "w") as f:
            for task in self._tasks:
                status_flag = "- " if task.status else ""
                f.write("{}{}\n".format(status_flag, task.title))
