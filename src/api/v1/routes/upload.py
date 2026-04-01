from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os

from src.ingestion.ingestion import ingest_file

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/admin/upload")
async def upload_file(
    file: UploadFile = File(...),
    regulation_type: str | None = Form(None)
):
    
   
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )

   
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

   
    result = ingest_file(
        file_path=file_path,
        filename=file.filename,
        regulation_type=regulation_type
    )

    return {
        "message": "File uploaded and processed successfully",
        "file_name": file.filename,
        "chunks_created": result["chunks"]
    }