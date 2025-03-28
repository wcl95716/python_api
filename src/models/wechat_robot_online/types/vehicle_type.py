# type_vehicle.py
import pandas as pd

class Vehicle:
    def __init__(self, plate_number, organization, status, camera_status,expiration_date):
        # 车牌号码
        self.plate_number = plate_number
        # 车辆组织
        self.organization = organization
        # 车辆状态
        self.status = status
        # 摄像头状态
        self.camera_status = camera_status
        # 服务到期时间
        self.expiration_date = expiration_date

    def __str__(self):
        return f"车牌号码: {self.plate_number}\n车辆组织: {self.organization}\n车辆状态: {self.status}\n摄像头状态: {self.camera_status}\n 服务到期时间:{self.expiration_date}\n"


def run_example():
    # 读取Excel文件
    df = pd.read_excel('/Users/panda/Desktop/github.nosync/ticketing-website/backend/src/models/wechat_robot_online/types/监控日志模板.xlsx')

    # 将Excel数据转化为Vehicle对象列表
    vehicles = []
    for index, row in df.iterrows():
        plate_number = row['车牌号码']
        organization = row['车辆组织']
        status = row['车辆状态（离线/定位）']
        camera_status = row['摄像头状态']
        expiration_date = row['服务到期时间']
        
        vehicle = Vehicle(plate_number, organization, status, camera_status,expiration_date)
        vehicles.append(vehicle)

    # 打印Vehicle对象列表
    for vehicle in vehicles:
        print(f"车牌号码: {vehicle.plate_number}")
        print(f"车辆组织: {vehicle.organization}")
        print(f"车辆状态: {vehicle.status}")
        print(f"摄像头状态: {vehicle.camera_status}")
        print()
        
        
if __name__ == '__main__':
    run_example()