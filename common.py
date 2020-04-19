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

    def status_reverse(self):
        self._status = not self._status

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
        self._doing_tasks = []
        self._done_tasks = []
        self.load_tasks()
        self.sort_tasks()

    @property
    def tasks(self):
        self.sort_tasks()
        return self._doing_tasks + self._done_tasks

    def belong_to_which_tasks(self, status):
        return getattr(self, "_{}_tasks".format(status))

    @staticmethod
    def str_status_reverse(status):
        return "doing" if status == "done" else "done"

    def task_status_reverse(self, job_type, task_num):
        if isinstance(task_num, str) or isinstance(task_num, unicode):
            task_num = int(task_num)

        not_job_list = self.belong_to_which_tasks(self.str_status_reverse(job_type))
        if task_num >= len(not_job_list):
            return

        job = not_job_list.pop(task_num)
        job.status_reverse()
        job_list = self.belong_to_which_tasks(job_type)
        job.display_num = len(job_list)
        job_list.append(job)

        for task in not_job_list:
            if task.display_num > task_num:
                task.display_num -= 1

        self.dump_tasks()

    def add_one_task(self, title):
        self._doing_tasks.append(Task(title))
        self.dump_tasks()

    def del_one_task(self, task_num):
        if isinstance(task_num, str):
            task_num = int(task_num)
        if task_num >= len(self._doing_tasks):
            self._done_tasks.pop(task_num)
        else:
            self._doing_tasks.pop(task_num)
        self.dump_tasks()

    def sort_tasks(self):
        self._doing_tasks.sort(key=lambda x: x.display_num)
        self._done_tasks.sort(key=lambda x: x.display_num)

    def load_tasks(self, file_path=DEFAULT_FILE_PATH):
        with open(file_path) as f:
            for line in f:
                if not line.strip():
                    continue
                title = line.replace("-", "").strip()
                status = line.startswith("-")  # True: done, False: doing
                display_num = len(self._done_tasks) if status else len(self._doing_tasks)
                task = Task(title=title, status=status, display_num=display_num)
                task_list = getattr(self, "_{}_tasks".format(task.status))
                task_list.append(task)

    def dump_tasks(self, file_path=DEFAULT_FILE_PATH):
        with open(file_path, "w") as f:
            for inx, task in enumerate(self.tasks):
                if inx != 0:
                    f.write("\n")
                status_flag = "- " if task.status == "done" else ""
                f.write("{}{}".format(status_flag, task.title))