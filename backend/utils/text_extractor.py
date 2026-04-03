from io import BytesIO

from fastapi import HTTPException, UploadFile
from pdfminer.high_level import extract_text as pdf_extract_text
from pdfminer.pdfparser import PDFSyntaxError
from docx import Document
from PIL import Image, ImageOps, ImageFilter
import pytesseract
# Optional: set this if Tesseract is not on PATH. Update to your install location.
TESSERACT_CMD = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Set to None if already on PATH.


async def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        pdf_bytes = await file.read()
        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Empty PDF file.")

        buffer = BytesIO(pdf_bytes)
        text = pdf_extract_text(buffer)
        if not text:
            raise HTTPException(status_code=422, detail="Unable to extract text from PDF.")

        return text.strip()
    except PDFSyntaxError as exc:
        raise HTTPException(status_code=400, detail="Corrupted or invalid PDF file.") from exc
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - runtime guard
        raise HTTPException(status_code=500, detail="Failed to process PDF.") from exc


async def extract_text(file: UploadFile) -> str:
    if file.content_type and "pdf" in file.content_type:
        return await extract_text_from_pdf(file)

    if file.content_type and "word" in file.content_type:
        return await extract_text_from_docx(file)

    if file.content_type and file.content_type.lower() in {"image/png", "image/jpeg", "image/jpg"}:
        return await extract_text_from_image(file)

    data = await file.read()

    text = data.decode("utf-8", errors="ignore")
    if not text:
        text = data.decode("latin1", errors="ignore")

    return text.strip()


async def extract_text_from_docx(file: UploadFile) -> str:
    try:
        doc_bytes = await file.read()
        if not doc_bytes:
            raise HTTPException(status_code=400, detail="Empty DOCX file.")

        buffer = BytesIO(doc_bytes)
        document = Document(buffer)
        paragraphs = [p.text for p in document.paragraphs if p.text]
        text = "\n".join(paragraphs).strip()

        if not text:
            raise HTTPException(status_code=422, detail="No text found in DOCX.")

        return text
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - runtime guard
        raise HTTPException(status_code=500, detail="Failed to process DOCX.") from exc


async def extract_text_from_image(file: UploadFile) -> str:
    try:
        if TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty image file.")

        with Image.open(BytesIO(image_bytes)) as img:
            # Normalize orientation and convert to grayscale for OCR.
            img = ImageOps.exif_transpose(img)
            img = img.convert("L")
            # Increase contrast slightly and denoise.
            img = ImageOps.autocontrast(img)
            img = img.filter(ImageFilter.MedianFilter(size=3))

            text = pytesseract.image_to_string(img)

        text = text.strip()
        if not text:
            raise HTTPException(status_code=422, detail="No text detected in image.")

        return text
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - runtime guard
        raise HTTPException(status_code=500, detail="Failed to process image.") from exc
