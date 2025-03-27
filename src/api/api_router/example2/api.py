from fastapi import APIRouter, HTTPException
"""
This module provides the API endpoints for support work_orders.
"""
import json
import socket
from typing import Optional

from fastapi import Body, Depends, FastAPI, Query, Response, Path
from typing import List
from typing import TypeVar, List, Optional

def find_free_port(start_port: int = 8000, max_port: int = 9000) -> Optional[int]:
    """查找指定范围内的空闲端口"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

class ExampleAPI(APIRouter):
    def __init__(self):
        super().__init__(
            prefix="/example2",
            tags=["exampleAPIRouter2"],
        )
        self.setup_routes()
    
    def setup_routes(self):
        @self.post("", summary="创建")
        async def create_record() -> Response:
            return Response(status_code=200)

        @self.put("", summary="更新")
        async def update_record() -> Response:
            return Response(status_code=200)

        @self.delete("", summary="删除")
        async def delete_record(id: int = Path(..., description="id")) -> Response:
            return Response(status_code=200)

        @self.get("/{id}", summary="查找")
        async def get_record_by_id(id: int = Path(..., description="WorkOrder ID")) -> Response:
            return Response(content=json.dumps(""), media_type="application/json")

        @self.get("/free-port", summary="获取空闲端口")
        async def get_free_port(
            start_port: int = Query(8000, description="起始端口号"),
            max_port: int = Query(9000, description="最大端口号")
        ) -> Response:
            port = find_free_port(start_port, max_port)
            if port is None:
                raise HTTPException(status_code=404, detail="未找到可用端口")
            return Response(
                content=json.dumps({"port": port}),
                media_type="application/json"
            )

router = ExampleAPI()