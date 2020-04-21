# -*- coding:utf-8 -*-
# @Author : jun
# @Time   : 2020/4/19 12:52
import sys

from common import DONE_ICON, DOING_ICON, TaskOperator
from utils import parse_argument
from workflow import Workflow

reload(sys)
sys.setdefaultencoding("utf-8")


# TODO: 2020-04-19  16:10
# 1. filter
# 2. del task -> ctrl
# 3. reset tasks -> tdre
# 4. using link list save tasks
# 5. change title ->

@parse_argument
def main(wf):
    worker = TaskOperator.get_instance()
    for task in worker.filter_tasks:
        wf.add_item(
            title=task.title,
            subtitle=repr(task),
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
