# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 12:52
import sys

from common import DONE_ICON, DOING_ICON
from utils import parse_argument
from workflow import Workflow

reload(sys)
sys.setdefaultencoding("utf-8")


# TODO: 2020-04-19  16:10
# 1. del task
# 2. reset tasks
# 3. using link list save tasks
# 4. change title

@parse_argument
def main(wf, worker=None):
    for inx, task in enumerate(worker.tasks):
        wf.add_item(
            title=task.title,
            subtitle="Task No.{} status: {}".format(
                inx + 1, task.status),
            valid=True,
            arg="{} {}".format(worker.str_status_reverse(task.status), task.display_num),
            icon=DONE_ICON if task.status == "done" else DOING_ICON,

        )

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
