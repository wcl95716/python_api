


from models.wechat_robot_tasks.types.robot_task_type import RobotTask


def fix_task_content(task: RobotTask):
    pass


def fix_tasks(tasks: list[RobotTask]):
    for task in tasks:
        fix_task_content(task)
    pass



