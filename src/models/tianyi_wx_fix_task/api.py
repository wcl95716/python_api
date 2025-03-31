


from models.wechat_robot_tasks.types.robot_task_type import RobotTask


def fix_task_content(task: RobotTask):
    content = task.content
    toUser = task.to_user
    if task.task_type == 0:
        # 发送消息
        pass
    elif task.task_type == 1:
        # 发送图片
        pass
    pass

def fix_tasks(tasks: list[RobotTask]):
    for task in tasks:
        fix_task_content(task)
    pass



