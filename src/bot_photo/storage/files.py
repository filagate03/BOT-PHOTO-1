from __future__ import annotations

import uuid
from pathlib import Path

from aiogram import Bot

from .s3_storage import S3Storage


class FileStorage:
    def __init__(
        self,
        faces_root: Path,
        sessions_root: Path,
        s3: S3Storage | None = None,
    ) -> None:
        self._faces_root = faces_root
        self._sessions_root = sessions_root
        self._s3 = s3
        self._faces_root.mkdir(parents=True, exist_ok=True)
        self._sessions_root.mkdir(parents=True, exist_ok=True)

    async def save_face(self, bot: Bot, user_id: int, file_id: str) -> Path:
        face_dir = self._faces_root / str(user_id)
        face_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.jpg"
        destination = face_dir / filename
        await bot.download(file_id, destination=destination)
        if self._s3:
            try:
                await self._s3.upload_bytes(
                    destination.read_bytes(),
                    f"faces/{user_id}/{filename}",
                    content_type="image/jpeg",
                )
            except Exception:
                # S3 is optional; ignore upload failures.
                pass
        return destination

    async def save_generation(self, content: bytes, suffix: str = ".jpg") -> Path:
        filename = f"{uuid.uuid4().hex}{suffix}"
        destination = self._sessions_root / filename
        destination.write_bytes(content)
        if self._s3:
            try:
                await self._s3.upload_bytes(
                    content,
                    f"sessions/{filename}",
                    content_type="image/jpeg",
                )
            except Exception:
                pass
        return destination
