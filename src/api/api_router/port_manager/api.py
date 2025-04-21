from fastapi import APIRouter, HTTPException, Query, Response, Path
"""
端口管理模块

提供系统端口管理相关的功能，如：
- 获取空闲端口
- 检查端口状态

该模块实现了线程安全的端口管理，支持自动清理未使用的端口，
并提供灵活的端口范围配置。
"""
import json
import socket
import threading
import time
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime
import os
import subprocess

@dataclass(frozen=True)
class PortInfo:
    """
    端口信息类，记录端口分配时间和使用状态
    
    Attributes:
        port: 端口号
        allocated_time: 分配时间戳
        is_used: 是否已被使用
    """
    port: int
    allocated_time: float
    is_used: bool = False

class PortManagerAPI(APIRouter):
    """
    端口管理API类
    
    提供端口管理相关的API接口，包括：
    1. 获取空闲端口
    2. 检查端口状态
    
    特点：
    - 线程安全：使用锁机制确保多线程环境下的安全
    - 端口追踪：维护已使用端口集合，避免重复分配
    - 灵活配置：支持默认范围和自定义范围
    - 自动清理：定期清理未使用的超时端口
    """
    
    # 默认端口范围配置
    DEFAULT_START_PORT: int = 10000  # 默认起始端口
    DEFAULT_MAX_PORT: int = 65000   # 默认最大端口
    CLEANUP_INTERVAL: int = 60      # 清理间隔（秒）
    
    def __init__(self) -> None:
        """
        初始化端口管理API
        
        设置路由前缀和标签，并初始化路由
        """
        super().__init__(
            prefix="/port-manager",  # API路由前缀
            tags=["port_manager"],   # API文档标签
        )
        # 线程安全相关
        self._lock: threading.Lock = threading.Lock()   # 线程锁，用于同步
        self._used_ports: Dict[int, PortInfo] = {}     # 已使用端口信息字典
        self._last_cleanup: float = 0                  # 上次清理时间
        self.setup_routes()  # 设置路由
    
    def _cleanup_ports(self) -> None:
        """
        清理超时的未使用端口
        
        检查并移除分配超过清理间隔但未使用的端口。
        清理操作在锁的保护下进行，确保线程安全。
        """
        current_time = time.time()
        # 如果距离上次清理时间未超过清理间隔，则不进行清理
        if current_time - self._last_cleanup < self.CLEANUP_INTERVAL:
            return
            
        with self._lock:
            # 更新清理时间
            self._last_cleanup = current_time
            
            # 找出需要清理的端口（未使用且超时）
            ports_to_remove = [
                port for port, info in self._used_ports.items()
                if not info.is_used and current_time - info.allocated_time >= self.CLEANUP_INTERVAL
            ]
            
            # 移除超时的未使用端口
            for port in ports_to_remove:
                del self._used_ports[port]
    
    def _validate_port_range(self, start_port: int, max_port: int) -> None:
        """
        验证端口范围是否有效
        
        Args:
            start_port: 起始端口号
            max_port: 最大端口号
            
        Raises:
            ValueError: 当端口范围无效时抛出
        """
        if start_port > max_port:
            raise ValueError("起始端口不能大于最大端口")
        if start_port < 0 or max_port > 65535:
            raise ValueError("端口范围必须在 0-65535 之间")
    
    def _try_bind_port(self, port: int) -> bool:
        """
        尝试绑定端口
        
        Args:
            port: 要绑定的端口号
            
        Returns:
            bool: 是否成功绑定
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.settimeout(0.1)
                try:
                    # 尝试连接到端口
                    s.connect(('127.0.0.1', port))
                    return False  # 如果能连接上，说明端口被占用
                except (socket.timeout, ConnectionRefusedError):
                    # 连接失败说明端口可能可用
                    try:
                        # 尝试绑定到所有接口
                        s.bind(('0.0.0.0', port))
                        s.close()
                        return True
                    except OSError:
                        # 如果绑定失败，尝试使用 netstat 检查
                        try:
                            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
                            return str(port) not in result.stdout
                        except Exception:
                            return False
        except Exception:
            return False
    
    def find_free_port(self, start_port: Optional[int] = None, max_port: Optional[int] = None) -> Optional[int]:
        """
        查找指定范围内的空闲端口
        
        Args:
            start_port: 起始端口号，如果为None则使用默认值
            max_port: 最大端口号，如果为None则使用默认值
            
        Returns:
            Optional[int]: 找到的空闲端口号，如果未找到则返回None
            
        Raises:
            ValueError: 当端口范围无效时抛出
        """
        # 使用默认值或自定义值
        start = start_port if start_port is not None else self.DEFAULT_START_PORT
        max_p = max_port if max_port is not None else self.DEFAULT_MAX_PORT
        
        # 验证端口范围
        self._validate_port_range(start, max_p)
        
        # 清理超时的未使用端口
        self._cleanup_ports()
        
        # 使用线程锁确保线程安全
        with self._lock:
            # 遍历指定范围内的所有端口
            for port in range(start, max_p + 1):
                # 检查端口是否已被记录使用
                if port in self._used_ports:
                    continue
                    
                # 尝试绑定端口
                if self._try_bind_port(port):
                    # 将端口添加到已使用集合，记录分配时间
                    self._used_ports[port] = PortInfo(
                        port=port,
                        allocated_time=time.time(),
                        is_used=True
                    )
                    return port
        return None
    
    def is_port_available(self, port: int) -> bool:
        """
        检查指定端口是否可用
        
        Args:
            port: 要检查的端口号
            
        Returns:
            bool: 端口是否可用
        """
        # 清理超时的未使用端口
        self._cleanup_ports()
        
        # 使用线程锁确保线程安全
        with self._lock:
            # 检查端口是否已被记录使用
            if port in self._used_ports:
                return False
            return self._try_bind_port(port)
    
    def setup_routes(self) -> None:
        """
        设置API路由
        
        配置所有API端点，包括：
        1. 获取空闲端口
        2. 检查端口状态
        """
        @self.get("/free-port", summary="获取空闲端口")
        async def get_free_port(
            start_port: Optional[int] = Query(None, description="起始端口号（可选）"),
            max_port: Optional[int] = Query(None, description="最大端口号（可选）")
        ) -> Response:
            """
            获取空闲端口的API端点
            
            Args:
                start_port: 可选的起始端口号
                max_port: 可选的最大端口号
                
            Returns:
                Response: 包含端口号的JSON响应
                
            Raises:
                HTTPException: 当未找到可用端口或参数无效时抛出
            """
            try:
                # 查找空闲端口
                port = self.find_free_port(start_port, max_port)
                if port is None:
                    raise HTTPException(status_code=404, detail="未找到可用端口")
                # 返回端口号
                return Response(
                    content=json.dumps({
                        "port": port,
                        "allocated_at": datetime.fromtimestamp(time.time()).isoformat()
                    }),
                    media_type="application/json"
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @self.get("/check-port/{port}", summary="检查端口状态")
        async def check_port(port: int = Path(..., description="要检查的端口号")) -> Response:
            """
            检查端口状态的API端点
            
            Args:
                port: 要检查的端口号
                
            Returns:
                Response: 包含端口状态的JSON响应
            """
            # 检查端口是否可用
            is_available = self.is_port_available(port)
            # 返回检查结果
            return Response(
                content=json.dumps({
                    "port": port,
                    "available": is_available,
                    "checked_at": datetime.fromtimestamp(time.time()).isoformat()
                }),
                media_type="application/json"
            )

# 创建端口管理API实例
router = PortManagerAPI() 
