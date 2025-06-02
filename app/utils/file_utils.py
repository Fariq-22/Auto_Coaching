import io
import requests

# Download PDF from URL
def download_with_presigned(url):
    """
    Download the file via s3 url
    Args:
        s3 link
    Returns:
        bytesteam of file
    """
    response = requests.get(url)
    response.raise_for_status()
    return io.BytesIO(response.content)

