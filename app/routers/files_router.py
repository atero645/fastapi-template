from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from app.dependencies import PaginationParams, SessionDep
from app.internal.services.file_service import FileService
import mimetypes


router = APIRouter(tags=["files"])


@router.post("/files/")
async def upload_file(file: UploadFile, session: SessionDep):
    file_service = FileService(session)

    data = await file_service.upload_file(file)
    return data


@router.get("/files/")
def get_files(pagination: PaginationParams, session: SessionDep):
    file_service = FileService(session)

    data = file_service.get_files(**pagination)
    return data


@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    session: SessionDep,
    download: bool = Query(False, description="Force file download"),
):
    file_service = FileService(session)

    file = file_service.get_file(file_id)

    if not file:
        raise HTTPException(status_code=404, detail="File not found!")

    file_path = Path(file.path)
    media_type, _ = mimetypes.guess_type(str(file_path))
    media_type = media_type or "application/octet-stream"

    disposition = "attachment" if download else "inline"
    headers = {"Content-Disposition": f'{disposition}; filename="{file_path.name}"'}

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=file.original_name,
        headers=headers,
    )


@router.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
