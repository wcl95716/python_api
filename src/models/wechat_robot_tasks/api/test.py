import requests

    # vehicle_url= "http://127.0.0.1:8001/test/uploads/eebba396c5c74f488a9383c1334ddb61_-.xlsx"
    # excel_file_path= "http://localhost:8001/test/uploads/4410e88715f94c1fac7db506eb252ede_-.xlsx"
def test1():
    # 定义 LogProcessingFilesUrl 对象数据
    data = {
        'vehicle_data_url': 'http://47.116.201.99:8001/test/uploads/201a044dd5e142dabf4264be33dcb449_-.xlsx',
        'organization_group_url': 'http://47.116.201.99:8001/test/uploads/c5b6860bd57e4922a8faf8fc25417ceb_-.xlsx',
        'language_template_url': ''
    }

    # 发送 POST 请求到 API 端点
    url = 'http://47.116.201.99:8001/wechat_robot_online/process_log'  # 替换为实际的 API 地址
    response = requests.post(url, json=data)

    # 检查响应
    if response.status_code == 200:
        print('Request successful!')
        print(response.json())
    else:
        print(f'Request failed with status code: {response.status_code}')
        print(response.text)


def test2():
    # 设置 API 地址
    api_url = 'http://47.116.201.99:8001/wechat_robot_online/get_task'  # 替换为实际的 API 地址

    try:
        # 发送 GET 请求
        response = requests.get(api_url)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析 JSON 响应
            task_data = response.json()
            # 处理任务数据
            print(task_data)
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"请求发生异常：{str(e)}")

test1()
# test2()