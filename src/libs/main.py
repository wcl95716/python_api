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
    
    def _type_text(self, text: str):
        """使用 pynput 输入文本"""
        for char in text:
            self.keyboard.type(char)
            time.sleep(0.1)  # 添加延迟以确保输入稳定
    
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
            
            return True
        return False
    
    def send_message(self, message: str) -> bool:
        """发送消息"""
        if self.current_state == WeChatState.CHATTING:
            # 输入消息
            self._type_text(message)
            # 按回车发送
            self._press_enter()
            return True
        return False
    
    def get_current_state(self) -> WeChatState:
        """获取当前状态"""
        return self.current_state
    
    def reset(self):
        """重置状态机"""
        self.current_state = WeChatState.CLOSED

def main():
    # 测试状态机
    wechat = WeChatAutomation()
    
    # 测试打开微信
    print("尝试打开微信...")
    if wechat.open_wechat():
        print(f"微信已打开，当前状态: {wechat.get_current_state()}")
        
        # 测试搜索功能
        print("尝试搜索...")
        if wechat.search("文件传输助手"):
            print(f"搜索完成，当前状态: {wechat.get_current_state()}")
            
            # 发送消息
            print("尝试发送消息...")
            if wechat.send_message("这是一条测试消息"):
                print("消息发送成功")
            else:
                print("消息发送失败")
    else:
        print("操作失败")

if __name__ == "__main__":
    main()
    main()
