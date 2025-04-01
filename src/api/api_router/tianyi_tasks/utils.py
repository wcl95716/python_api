


from libs.main import WeChatAutomation
from models.wechat_robot_tasks.types.robot_task_type import RobotTask

wechat = WeChatAutomation()

def fix_task_content(task: RobotTask):
    content = task.content
    toUser = task.to_user
    print(f"发送消息给{toUser}，内容为{content}")
    if task.task_type == 0:
        # 发送消息
        wechat.send_message("AI苏博蒂奇", content)
        pass
    elif task.task_type == 1:
        # 发送图片
        wechat.send_file("文件传输助手", content)
        pass
    pass

def fix_tasks(tasks: list[RobotTask]):
    for task in tasks:
        fix_task_content(task)
    pass



