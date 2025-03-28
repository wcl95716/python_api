from fastapi import APIRouter, HTTPException, UploadFile, File
import pandas as pd
from typing import List

router = APIRouter(
    prefix="/tianyi_tasks",
    tags=["tianyiapi"],
)

@router.post("/upload-excel")
async def upload_excel(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        # 读取第一个 Excel 文件
        df1 = pd.read_excel(file1.file)
        # 读取第二个 Excel 文件
        df2 = pd.read_excel(file2.file)

        # 示例：将两个文件的行数返回
        result = {
            "file1_rows": len(df1),
            "file2_rows": len(df2),
        }
        return {"message": "Files processed successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing files: {str(e)}")

