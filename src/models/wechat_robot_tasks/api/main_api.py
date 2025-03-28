
import datetime
import sys
import time
sys.path.append("./src")
import requests

from models.wechat_robot_tasks.types.robot_task_type import RobotTask


from models.wechat_robot_tasks.types.log_processing_type import LogProcessing
from utils import local_logger
from utils.table_image import create_table_image


import pandas as pd
from models.wechat_robot_tasks.types.organization_group_type import OrganizationGroup
from models.wechat_robot_tasks.types.vehicle_type import Vehicle

from utils.download_file import download_excel_and_read


def get_vehicles_from_url(excel_url:str) -> list[Vehicle]:
    # 读取Excel文件
    
    df:pd.DataFrame = download_excel_and_read(excel_url)
    
    df['车牌号码'] = df['车牌号码'].fillna('').astype(str)
    df['车辆组织'] = df['车辆组织'].fillna('').astype(str)
    # 类型为时间
    df['车辆状态（离线/定位）'] = df['车辆状态（离线/定位）'].fillna('').astype(str)
    df['摄像头状态'] = df['摄像头状态'].fillna('').astype(str)
    if df.get('服务到期时间') is not None:
        df['服务到期时间'] = df['服务到期时间'].fillna('').astype(str)
    else:
        df['服务到期时间'] = ''
    # print(df)
    # print("asdasddasd  ",df)
    if df is None:
        return None
    # 将Excel数据转化为Vehicle对象列表
    
    vehicles:list[Vehicle] = []
    for index, row in df.iterrows():
        plate_number = row['车牌号码']
        organization = row['车辆组织']
        status:str = row['车辆状态（离线/定位）']
        camera_status = row['摄像头状态']
        # row['服务到期时间']
        expiration_date = row['服务到期时间']
        print("expiration_date: ", expiration_date)
        
        # print("status: ", status , isinstance(status, float))
        # 判断status 是否为浮点数
        try:
            # print("status is float")
            # 假设从Excel中读取的时间值是 "0.0770833333333333"（1小时51分钟）
            excel_time = float(status)
            print("excel_time: ", excel_time)
            hours = int(excel_time * 24)  # 将小数部分转换为小时数
            print("hours: ", hours)
            # 将Excel时间值转换为Python的datetime对象
            minutes = int((excel_time * 24- hours)  * 60)
            print("minutes: ", minutes)
            my_datetime = datetime.datetime(1900, 1, 1, hours, minutes)  # 日期部分可以是任意日期
            print("my_datetime: ", my_datetime)
            # 将datetime对象格式化为字符串
            time_str = my_datetime.strftime("%H:%M")
            print("time_str: ", time_str)
            status = time_str
        except Exception as e:
            pass 
            # print("status is not float" , e)
            pass
        
        vehicle = Vehicle(plate_number, organization, status, camera_status,expiration_date)
        # print("vehicle: ", vehicle.__str__())
        vehicles.append(vehicle)
    return vehicles


def get_organizationgroups_from_url(excel_url: str) -> list[OrganizationGroup]:

    # 使用download_excel_and_read函数下载Excel文件并读取内容
    df = download_excel_and_read(excel_url)
    
    if df is not None:
        # 创建一个空列表来存储OrganizationGroup对象
        organization_groups = []

        # 遍历DataFrame的行，为每一行的数据创建一个OrganizationGroup对象
        for index, row in df.iterrows():
            organization = row['车辆组织']
            group_name = row['微信服务群名称']
            vehicle_status_speech = row['车辆状态（离线/定位）']
            camera_status_speech = row['摄像头状态']
            org_group = OrganizationGroup(organization, group_name , vehicle_status_speech , camera_status_speech)
            organization_groups.append(org_group)
            
        return organization_groups
    else:
        return []

def get_log_processing(vehicle_url, organization_group_url) -> LogProcessing:
    vehicle_list = get_vehicles_from_url(vehicle_url)
    org_group_list = get_organizationgroups_from_url(organization_group_url)
    
    log_processing = LogProcessing(vehicle_list, org_group_list)
    return log_processing
    pass

def get_tasks( vehicle_url, organization_group_url) -> list[RobotTask]:
    log_processing = get_log_processing(vehicle_url, organization_group_url)
    tasks = log_processing.get_all_robot_task_by_group_and_status()
    return tasks
    pass 

def upload_img_file(img_path:str) -> None:
    url = 'http://47.116.201.99:8001/test/upload_file'
    file_path = img_path
    # files = {'file': ( , open(file_path, 'rb'))}
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    
    # 检查响应状态码是否为 200，表示请求成功
    if response.status_code == 200:
        # 使用 response.json() 方法解析返回的 JSON 数据
        json_data = response.json()
        
        # 获取 file_url 字段的值
        file_url = json_data.get('file_url', None)
        
        if file_url:
            return file_url
        else:
            print("File URL not found in the JSON response.")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

    

if __name__=='__main__':

    # 传入Excel文件路径，并获取OrganizationGroup对象列表
    # vehicle_url= "http://127.0.0.1:8001/test/uploads/5d1cf85c71b94aa4bdac16393c986d55_12.6.xlsx"
    # excel_file_path= "http://localhost:8001/test/uploads/757e28eb783e4f86af3e48bb2580c237_-12-6.xlsx"
    
    vehicle_url= "http://0.0.0.0:25432/FileStoreAPI/get_file_uu_id/10bc559c-8680-4ba2-815f-7fd1b0264359"
    # a71a109e-bb4c-4efb-a8dc-d44f3a678ce4
    excel_file_path= "http://0.0.0.0:25432/FileStoreAPI/get_file_uu_id/7e985b48-a5fe-49e1-b225-d68b3b769f54"


    # 获取分类后的数据
    # 创建LogProcessingType对象并进行分类
    log_processing = get_log_processing(vehicle_url, excel_file_path)
    
    tasks = log_processing.get_all_robot_task_by_group_and_status()
    tasks.extend(log_processing.get_all_robot_task_by_group())
    print(len(log_processing.vehicle_data_by_group.keys()) , len(tasks) )
    for task in tasks:
        print("task: ", task.task_type,task.to_user , task.content)

    # Create a DataFrame from the list of dictionaries
