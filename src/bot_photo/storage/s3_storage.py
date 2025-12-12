from __future__ import annotations

import aioboto3


class S3Storage:
    def __init__(
        self,
        *,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str = "ru-central1",
    ) -> None:
        self.endpoint_url = endpoint_url.rstrip("/")
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name.split(".")[0]
        self.region = region
        self._session = aioboto3.Session()

    async def upload_bytes(
        self,
        data: bytes,
        s3_key: str,
        content_type: str = "image/jpeg",
    ) -> str:
        async with self._session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        ) as s3:
            await s3.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=data,
                ContentType=content_type,
                ACL="public-read",
            )
        return f"{self.endpoint_url}/{self.bucket_name}/{s3_key}"


__all__ = ["S3Storage"]
