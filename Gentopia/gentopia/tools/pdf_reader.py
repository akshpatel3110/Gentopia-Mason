from typing import Optional, Any
from pydantic import BaseModel, Field
from gentopia.tools.basetool import BaseTool
import requests
import pdfplumber
from io import BytesIO

class PDFReadArgs(BaseModel):
    url: str = Field(..., description="The URL of the PDF document.")

class PDFReader(BaseTool):
    name = "pdf_reader"
    args_schema: Optional[type[BaseModel]] = PDFReadArgs
    description: str = "A tool to read and extract text from a PDF file located at a specified URL."

    def _run(self, url: str) -> str:
        """
        Reads a PDF file from a given URL and extracts the text.

        Parameters:
            url (str): The URL to the PDF document.

        Returns:
            str: The extracted text from the PDF document.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure the request was successful

            # Use BytesIO to provide a file-like object for pdfplumber to read from
            with pdfplumber.open(BytesIO(response.content)) as pdf:
                pages = [page.extract_text() for page in pdf.pages]

            text_content = "\n".join(filter(None, pages))  # Filter out any None values from empty pages
            return text_content

        except requests.RequestException as e:
            error_message = f"Failed to retrieve PDF from URL: {url}. Error: {e}"
            print(error_message)
            return error_message
        except Exception as e:  # Catching a general exception because pdfplumber does not have a custom exceptions module
            error_message = f"Failed to parse PDF content. Error: {e}"
            print(error_message)
            return error_message

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
