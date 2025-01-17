import os
from uuid import uuid4
from fastapi import UploadFile
import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader
from pypdf.errors import EmptyFileError


async def read(_f: UploadFile | None):
    """
    Extracts text from a PDF file.

    Args:
        file: The PDF file object.

    Returns:
        A tuple containing:
            - A dictionary with the extracted text or an error message.
            - The HTTP status code (200 for success, 500 for error).

    Raises:
        ValueError: If no PDF file is provided.
        FileNotFoundError: If the PDF file cannot be found or accessed.
        PermissionError: If the script does not have permission to read the file.
        pytesseract.pytesseract.TesseractNotFoundError: If Tesseract-OCR is not found.
        Exception: For any other unexpected errors.
    """

    if not _f:
        raise ValueError("At least one 'pdf_file' must be provided")
    try:
        target_path = os.path.join(os.getcwd(), "tmp", str(uuid4()) + f"_{_f.filename}")
        print(target_path)

        content = await _f.read()
        with open(target_path, "wb") as f:
            f.write(content)
            f.close()

        reader = PdfReader(target_path)

        result = []
        for page in reader.pages:
            result.append(page.extract_text())

        if sum(len(text) for text in result) <= 10:
            result = [
                pytesseract.image_to_string(img)
                for img in convert_from_path(target_path)
            ]

        parsed_text = " ".join(result)
        os.remove(target_path)
        return parsed_text
    except EmptyFileError:
        return {"error": "Uploaded PDF file seems to be empty"}, 400
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error handling the file: {e}")
    except PermissionError as e:
        raise PermissionError(f"Error handling the file: {e}")
    except pytesseract.pytesseract.TesseractNotFoundError as e:
        raise pytesseract.pytesseract.TesseractNotFoundError()
    except Exception as e:
        raise Exception(str(e))
