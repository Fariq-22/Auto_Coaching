import io
import httpx

async def download_with_presigned(url: str) -> io.BytesIO:
    """
    Downloads a file from a given S3 pre-signed URL asynchronously.

    Args:
        url (str): The pre-signed S3 URL to download the file from.

    Returns:
        io.BytesIO: A byte stream of the downloaded file content.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)