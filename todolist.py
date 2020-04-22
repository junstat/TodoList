# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 12:52
import sys

from common import DONE_ICON, DOING_ICON, TaskOperator, DELETE_ICON
from utils import parse_argument
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding("utf-8")


# TODO: 2020-04-19  16:10
# 1. using link list save tasks
# 2. change title ->

@parse_argument
def main(wf):
    worker = TaskOperator.get_instance()
    for task in worker.filter_tasks:
        it = wf.add_item(
            title=task.title,
            subtitle=repr(task),
            valid=True,
            arg="set_{} {}".format(worker.str_status_reverse(task.status), task.display_num),
            icon=DONE_ICON if task.status == "done" else DOING_ICON,
        )
        it.add_modifier(
            key="ctrl",
            subtitle="Delete task: {}".format(task.title),
            valid=True,
            arg="del_{} {}".format(task.status, task.display_num),  # del_done 1
            icon=DELETE_ICON
        )

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
