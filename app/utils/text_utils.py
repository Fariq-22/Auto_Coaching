import easyocr
import numpy as np
from PIL import Image
import fitz 
from io import BytesIO




async def text_extract(pdf_stream):
    """
    Extracts text and OCRs images from a PDF in a BytesIO stream.
    
    Args:
        pdf_stream (io.BytesIO): In-memory PDF content
    
    Returns:
        str: Extracted full text

    """
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Rewind the stream to the beginning
    pdf_stream.seek(0)

    # Open PDF from memory
    doc = fitz.open(stream=pdf_stream.read())
    full_text = ""

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        page_text = page.get_text()

        image_list = page.get_images(full=True)

        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]  # Raw bytes of the image

            # Load image into PIL Image
            image = Image.open(BytesIO(image_bytes)).convert("RGB")

            # Convert PIL Image to NumPy array (RGB format)
            image_np = np.array(image)

            # Now pass the NumPy array to EasyOCR
            result = reader.readtext(image_np)
            ocr_text = " ".join([res[1] for res in result])

            if ocr_text:
                page_text += "\n\n[Image Text]\n" + ocr_text

        full_text += f"\n\n--- Page {page_index + 1} ---\n\n" + page_text

    doc.close()
    return full_text

