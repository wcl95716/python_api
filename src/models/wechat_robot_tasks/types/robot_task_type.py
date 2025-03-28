
from enum import Enum


class RobotTaskType(Enum):
    TEXT_TYPE = 0
    IMAGE_TYPE = 1
    VIDEO_TYPE = 2
    pass 

class RobotTask:
    # 任务类型
    # 发送的人
    # 发送的内容
    
    def __init__(self, to_user, content,task_type:int = RobotTaskType.TEXT_TYPE.value,):
        self.task_type = task_type
        self.to_user = to_user
        self.content = content
        pass
    
    def __str__(self):
        return f"任务类型: {self.task_type}\n发送的人: {self.to_user}\n发送的内容: {self.content}\n"
    
    