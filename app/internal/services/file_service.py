from pathlib import Path
from fastapi import UploadFile
import aiofiles
from sqlmodel import Session, select

from app.internal.database.models import AppFile
import uuid
import os


class FileService:
    def __init__(self, session: Session):
        self.session = session

    async def upload_file(self, file: UploadFile):
        upload_dir = Path("uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        safe_name = os.path.basename(file.filename) if file.filename else ""
        extension = Path(safe_name).suffix.lower()
        dest_file_name = f"{str(uuid.uuid4())}{extension}"
        destination = upload_dir.joinpath(dest_file_name)

        payload = {
            "filename": dest_file_name,
            "original_name": safe_name,
            "size": file.size,
            "extension": extension,
            "path": str(destination),
        }

        async with aiofiles.open(destination, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)

        new_file = AppFile(**payload)
        self.session.add(new_file)
        self.session.commit()
        self.session.refresh(new_file)

        return new_file

    def get_files(self, limit=10, page=1) -> list[AppFile]:
        offset = limit * (page - 1)
        files = self.session.exec(select(AppFile).limit(limit).offset(offset)).all()
        return list(files)

    def get_file(self, file_id: int) -> AppFile | None:
        file = self.session.exec(
            select(AppFile).where(AppFile.id == file_id)
        ).one_or_none()
        return file
