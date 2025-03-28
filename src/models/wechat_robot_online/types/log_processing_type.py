import math
import sys
import pandas as pd
from models.wechat_robot_online.types.robot_task_type import RobotTask, RobotTaskType
from utils.table_image import create_table_image

sys.path.append("./src")
from utils import local_logger

from models.wechat_robot_online.types.organization_group_type import OrganizationGroup
from models.wechat_robot_online.types.vehicle_type import Vehicle


class LogProcessingFilesUrl:
    
    def __init__(self,vehicle_data_url:str , organization_group_url:str,language_template_url:str) -> None:
        self.vehicle_data_url = vehicle_data_url
        self.organization_group_url = organization_group_url
        self.language_template_url = language_template_url
        pass
    pass

class LogProcessing:
    camera_status = "camera_status"
    vehicle_status = "vehicle_status"
    
    @staticmethod
    def get_pandas_df(vehicle_data_list:list[Vehicle],group:OrganizationGroup):
        data = []
        for vehicle_data in vehicle_data_list:
            
            row = {
                # 'Organization Group': vehicle_data.organization,
                # 'Plate_Number': vehicle_data.plate_number,
                # 'Organization': vehicle_data.organization,
                # 'Status': vehicle_data.status,
                # 'Camera_Status': vehicle_data.camera_status,
                # 'Group_Name': group.group_name
                '车牌号': vehicle_data.plate_number,
                '车辆组织': vehicle_data.organization,
                '车辆状态': vehicle_data.status,
                '摄像头状态': vehicle_data.camera_status,
                '服务到期时间': vehicle_data.expiration_date
            }

            data.append(row)
        # df = pd.DataFrame(data)
        # return df
        return data
        pass
    
    @staticmethod
    # 获取RobotTask
    def get_robot_task(vehicle_data_list:list[Vehicle],group:OrganizationGroup) -> RobotTask:
        data = LogProcessing.get_pandas_df(vehicle_data_list,group)
        df = pd.DataFrame(data)
        img_path = create_table_image(df,title = group.organization)
        to_user = group.group_name
        robot_task = RobotTask(to_user = to_user, content = img_path,task_type=RobotTaskType.IMAGE_TYPE.value)
        return robot_task
        pass
    
    
    @staticmethod
    def get_robot_task_by_status(vehicle_data_list:list[Vehicle],group:OrganizationGroup, status) -> RobotTask:
        content = "车辆组织: " + group.organization + '{ctrl}{ENTER}'  + "车牌号码: "
        for vehicle_data in vehicle_data_list:
            content += vehicle_data.plate_number+","
            
      
        to_user = group.group_name
        if status == LogProcessing.camera_status:
            #content +=  " "+ str(vehicle_data.camera_status) + "     " 
            content +=  '{ctrl}{ENTER}'+ group.camera_status_speech
        elif status == LogProcessing.vehicle_status:
            content += '{ctrl}{ENTER}'
            content += group.vehicle_status_speech
        robot_task = RobotTask(to_user = to_user, content = content ,task_type= RobotTaskType.TEXT_TYPE.value)
        return robot_task
        pass

    
    """
    LogProcessingType类用于分类日志数据
    vehicle_data 按照 organization_group进行分类
    """
    def __init__(self, vehicle_data: list[Vehicle], organization_group: list[OrganizationGroup]):
        self.vehicle_data = vehicle_data
        self.organization_group = organization_group
        self.vehicle_data_by_group = self.get_vehicle_data_by_group()
        self.vehicle_data_by_status = self.get_vehicle_data_by_status()
        pass
    
    def get_vehicle_data_by_status(self) -> dict[OrganizationGroup,dict[str , list[Vehicle] ]]:
        
        vehicle_data_by_group:dict[OrganizationGroup,list[Vehicle]] = self.get_vehicle_data_by_group()
        vehicle_data_by_status:dict[OrganizationGroup,dict[str , list[Vehicle] ]] = {}
        # vehicle_data_by_group 每个OrganizationGroup 下的 list[Vehicle]再根据 Vehicle 的 status 进行分类
        

        def check_and_add_by_camera_status(vehicle_data: Vehicle):
            if not str(vehicle_data.camera_status)   :
                return
            # 如果vehicle_data_by_status字典中不存在org_group组织，则创建一个空字典
            if org_group not in vehicle_data_by_status:
                vehicle_data_by_status[org_group] = {}
            # 如果vehicle_data_by_status字典中不存在vehicle_data.status状态，则创建一个空列表
            if self.camera_status not in vehicle_data_by_status[org_group]:
                vehicle_data_by_status[org_group][self.camera_status] = []
            vehicle_data_by_status[org_group][self.camera_status].append(vehicle_data)
        
        def check_and_add_by_status(vehicle_data: Vehicle):
            if not str(vehicle_data.status)   :
                return
            # 如果vehicle_data_by_status字典中不存在org_group组织，则创建一个空字典
            if org_group not in vehicle_data_by_status:
                vehicle_data_by_status[org_group] = {}
            # 如果vehicle_data_by_status字典中不存在vehicle_data.status状态，则创建一个空列表
            if self.vehicle_status not in vehicle_data_by_status[org_group]:
                vehicle_data_by_status[org_group][self.vehicle_status] = []
            vehicle_data_by_status[org_group][self.vehicle_status].append(vehicle_data)
            
        for org_group, vehicle_data_list in vehicle_data_by_group.items():
            # 遍历每个Vehicle对象
            for vehicle_data in vehicle_data_list:
                check_and_add_by_camera_status(vehicle_data)
                check_and_add_by_status(vehicle_data)
        return vehicle_data_by_status
        
        pass 
    
    def get_vehicle_data_by_group(self) -> dict[OrganizationGroup,list[Vehicle]]:
        """
        通过organization_group对vehicle_data进行分类
        """
        vehicle_data_by_group:dict[OrganizationGroup,list[Vehicle]] = {}
        
        # 遍历每个组织的Vehicle对象列表
        for vehicle_data in self.vehicle_data:
            
            # 遍历每个OrganizationGroup对象
            for org_group in self.organization_group:
                
                # 如果Vehicle对象的organization_group属性等于OrganizationGroup对象的group_name属性
                # print("vehicle_data.organization: ", vehicle_data.organization)
                # print("org_group.organization: ", org_group.organization)
                if vehicle_data.organization == org_group.organization:
                    
                    # 如果vehicle_data_by_group字典中不存在org_group组织，则创建一个空列表
                    if org_group not in vehicle_data_by_group:
                        vehicle_data_by_group[org_group] = []
                        
                    # 将Vehicle对象添加到vehicle_data_by_group字典中
                    vehicle_data_by_group[org_group].append(vehicle_data)
        
        # print("vehicle_data_by_group: ", vehicle_data_by_group)
        return vehicle_data_by_group
        pass
    
    
    # 获取RobotTask
    def get_all_robot_task_by_group(self) -> list[RobotTask]:
        vehicle_data_by_group = self.get_vehicle_data_by_group()
        result: list[RobotTask]=  []
        for org_group, vehicle_data_list in vehicle_data_by_group.items():
            task = LogProcessing.get_robot_task(vehicle_data_list, org_group)
            result.append(task)
        
        return result
        pass
    
    def get_all_robot_task_by_group_and_status(self) ->list[RobotTask]:
        vehicle_data_by_status = self.get_vehicle_data_by_status()
        result: list[RobotTask]=  []
        for org_group, vehicle_data_list in vehicle_data_by_status.items():
            for status, vehicles in vehicle_data_list.items():
                task = LogProcessing.get_robot_task_by_status(vehicles, org_group, status)
                result.append(task)
        return result
        pass
    
    
    pass


