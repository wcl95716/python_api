import platform
import os
import subprocess
import time
from enum import Enum
from typing import Optional
from pynput.keyboard import Key, Controller

class WeChatState(Enum):
    """微信状态枚举"""
    CLOSED = "closed"           # 微信未打开
    OPENED = "opened"          # 微信已打开
    SEARCHING = "searching"    # 正在搜索
    CHATTING = "chatting"      # 正在聊天

class WeChatAutomation:
    """微信自动化状态机"""
    
    def __init__(self):
        self.current_state = WeChatState.CLOSED
        self.system = platform.system().lower()
        self.keyboard = Controller()
        # 根据系统设置快捷键
        self.cmd_key = Key.cmd if self.system == 'darwin' else Key.ctrl
    
    def _execute_command(self, command: list, shell: bool = False) -> bool:
        """执行系统命令"""
        try:
            subprocess.run(command, shell=shell)
            return True
        except Exception as e:
            print(f"执行命令时出错: {str(e)}")
            return False
    
    def _process_message(self, text: str) -> str:
        """处理消息文本，将特殊标记转换为实际换行符
        Args:
            text: 原始消息文本
        Returns:
            处理后的文本
        """
        # 替换特殊标记为换行符
        return text.replace("{ctrl}{ENTER}", "\n")
    
    def _type_text(self, text: str):
        """使用 pynput 输入文本"""
        for char in text:
            if char == "\n":
                # 根据操作系统选择换行快捷键
                if self.system == 'darwin':
                    # macOS 使用 Command+Enter
                    self.keyboard.press(Key.cmd)
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)
                    self.keyboard.release(Key.cmd)
                else:
                    # Windows 使用 Ctrl+Enter
                    self.keyboard.press(Key.ctrl)
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)
                    self.keyboard.release(Key.ctrl)
                time.sleep(0.5)  # 等待换行完成
            else:
                self.keyboard.type(char)
                time.sleep(0.1)  # 添加延迟以确保输入稳定
    
    def clear_message_list(self) -> bool:
        """清空消息列表
        Returns:
            bool: 是否成功清空消息列表
        """
        # 全选消息列表
        print("全选消息列表...")
        self.keyboard.press(self.cmd_key)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(self.cmd_key)
        time.sleep(0.5)
        
        # 删除选中的消息
        print("删除选中的消息...")
        self.keyboard.press(Key.delete)
        self.keyboard.release(Key.delete)
        time.sleep(0.5)
        
        print("消息列表清空完成")
        return True
    
    def _press_enter(self):
        """按回车键"""
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(0.5)  # 等待操作完成
    
    def _press_cmd_f(self):
        """按 Command+F (macOS) 或 Ctrl+F (Windows)"""
        self.keyboard.press(self.cmd_key)
        self.keyboard.press('f')
        self.keyboard.release('f')
        self.keyboard.release(self.cmd_key)
        time.sleep(0.5)
    
    def _press_esc(self):
        """按 ESC 键"""
        self.keyboard.press(Key.esc)
        self.keyboard.release(Key.esc)
        time.sleep(0.3)
    
    def _press_cmd_v(self):
        """按 Command+V (macOS) 或 Ctrl+V (Windows)"""
        self.keyboard.press(self.cmd_key)
        self.keyboard.press('v')
        self.keyboard.release('v')
        self.keyboard.release(self.cmd_key)
        time.sleep(0.5)
    
    def _copy_file_to_clipboard(self, file_path: str) -> bool:
        """将文件复制到剪贴板"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return False
            
        try:
            if self.system == 'darwin':
                # macOS 使用 osascript 来复制文件到剪贴板
                script = f'''
                tell application "System Events"
                    set the clipboard to POSIX file "{file_path}"
                end tell
                '''
                success = self._execute_command(['osascript', '-e', script])
                if not success:
                    print("复制文件到剪贴板失败")
                    return False
            elif self.system == 'windows':
                # Windows 使用 clip
                subprocess.run(['clip'], input=file_path.encode(), shell=True)
            else:
                print(f"不支持的操作系统: {self.system}")
                return False
            time.sleep(0.5)  # 等待剪贴板操作完成
            return True
        except Exception as e:
            print(f"复制文件到剪贴板时出错: {str(e)}")
            return False
    
    def open_wechat(self) -> bool:
        """打开微信"""
        if self.current_state == WeChatState.CLOSED:
            if self.system == 'darwin':
                success = self._execute_command(['osascript', '-e', 'tell application "WeChat" to activate'])
            elif self.system == 'windows':
                success = self._execute_command(['start', 'weixin://'], shell=True)
            else:
                print(f"不支持的操作系统: {self.system}")
                return False
            
            if success:
                self.current_state = WeChatState.OPENED
                time.sleep(1)  # 等待微信启动
                return True
        return False
    
    def search(self, keyword: str) -> bool:
        """搜索聊天 并打开聊天框"""
        if self.current_state == WeChatState.OPENED:
            # 发送 Command+F (macOS) 或 Ctrl+F (Windows)
            self._press_cmd_f()
            
            time.sleep(0.5)  # 等待搜索框出现
            self.current_state = WeChatState.SEARCHING
            
            # 使用 pynput 输入搜索关键词
            self._type_text(keyword)
            time.sleep(0.5)  # 等待搜索结果
            
            # 第一次按回车确认搜索
            self._press_enter()
            time.sleep(0.5)  # 等待搜索结果列表
            
            # 第二次按回车选择第一个聊天框
            self._press_enter()
            self.current_state = WeChatState.CHATTING

            # 为了重新获取输入框焦点
            # 发送 Command+F (macOS) 或 Ctrl+F (Windows)
            self._press_cmd_f()
            # esc
            self._press_esc()
            # 清空消息列表
            self.clear_message_list()
            
            return True
        return False
    
    def send_message(self, user: str, message: str) -> bool:
        """发送消息
        Args:
            user: 接收消息的用户或群组名称
            message: 要发送的消息内容，支持特殊换行符 {ctrl}{ENTER}
        """
        print(f"开始发送消息给 {user}...")
        print(f"当前状态: {self.current_state}")
        
        # 确保微信已打开
        if self.current_state == WeChatState.CLOSED:
            if not self.open_wechat():
                print("打开微信失败")
                return False
            time.sleep(1)  # 等待微信启动
        
        # 如果当前在聊天状态，先退出
        if self.current_state == WeChatState.CHATTING:
            print("退出当前聊天...")
            self._press_esc()
            time.sleep(0.5)
            self.current_state = WeChatState.OPENED
        
        # 先搜索用户
        print(f"搜索用户 {user}...")
        if not self.search(user):
            print(f"搜索用户 {user} 失败")
            return False
            
        print("搜索成功，准备发送消息...")
        # 处理消息文本
        processed_message = self._process_message(message)
        # 发送消息
        self._type_text(processed_message)
        self._press_enter()  # 最后发送消息
        print("消息发送完成")
        return True
    
    def send_file(self, user: str, file_path: str) -> bool:
        """发送文件
        Args:
            user: 接收文件的用户或群组名称
            file_path: 要发送的文件路径
        """
        print(f"开始发送文件给 {user}...")
        print(f"当前状态: {self.current_state}")
        
        # 确保微信已打开
        if self.current_state == WeChatState.CLOSED:
            if not self.open_wechat():
                print("打开微信失败")
                return False
            time.sleep(1)  # 等待微信启动
        
        # 如果当前在聊天状态，先退出
        if self.current_state == WeChatState.CHATTING:
            print("退出当前聊天...")
            self._press_esc()
            time.sleep(0.5)
            self.current_state = WeChatState.OPENED
        
        # 先搜索用户
        print(f"搜索用户 {user}...")
        if not self.search(user):
            print(f"搜索用户 {user} 失败")
            return False
            
        print("搜索成功，准备发送文件...")
        
        # 将文件复制到剪贴板
        print(f"复制文件到剪贴板: {file_path}")
        if not self._copy_file_to_clipboard(file_path):
            print("复制文件到剪贴板失败")
            return False
        
        print("文件已复制到剪贴板，准备粘贴...")
        # 粘贴文件
        self._press_cmd_v()
        time.sleep(1)  # 增加等待时间，确保文件粘贴完成
        
        print("文件已粘贴，准备发送...")
        # 按回车发送
        self._press_enter()
        print("文件发送完成")
        return True
    
    def get_current_state(self) -> WeChatState:
        """获取当前状态"""
        return self.current_state
    
    def reset(self):
        """重置状态机"""
        self.current_state = WeChatState.CLOSED

def main():
    # 测试状态机
    wechat = WeChatAutomation()
    
    # 发送消息
    print("尝试发送消息...")
    if wechat.send_message("文件传输助手", "这是一条测试消息"):
        print("消息发送成功")
    else:
        print("消息发送失败")
        
    # 发送文件
    print("尝试发送文件...")
    file_path = "/Users/panda/Documents/code/python_api/data/pngs/f395a87ff22a4a6db5d0fc1156375fe3.png"
    if wechat.send_file("文件传输助手", file_path):
        print("文件发送成功")
    else:
        print("文件发送失败")

if __name__ == "__main__":
    main()
