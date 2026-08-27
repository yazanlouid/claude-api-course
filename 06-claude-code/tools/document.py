from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path

from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Path to a PDF or DOCX file on disk to convert to markdown"
    ),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown-formatted text.

    Reads the file at the given path and converts its contents to markdown,
    preserving structural elements like headings and lists where possible.

    When to use:
    - When you need the text content of a PDF or DOCX file that already
      exists on disk
    - When you have a file path rather than already-loaded binary data (use
      binary_document_to_markdown instead if you already have the bytes)

    When not to use:
    - For file types other than PDF or DOCX

    Examples:
    >>> document_path_to_markdown("/path/to/report.pdf")
    '# Report Title\\n\\nReport contents...'
    """
    path = Path(file_path)
    file_type = path.suffix.lstrip(".")
    binary_data = path.read_bytes()
    return binary_document_to_markdown(binary_data, file_type)
