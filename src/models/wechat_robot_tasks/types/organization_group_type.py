import pandas as pd

# 创建表示车辆组织和群名称的类
class OrganizationGroup:
    def __init__(self, organization, group_name,vehicle_status_speech,camera_status_speech):
        self.organization = organization
        self.group_name = group_name
        #车辆状态（离线/定位）
        self.vehicle_status_speech = vehicle_status_speech
        #摄像头状态
        self.camera_status_speech = camera_status_speech
              
    pass



