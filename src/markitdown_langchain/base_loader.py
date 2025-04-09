from langchain_core.document_loaders import BaseLoader
from typing import List
from langchain_core.documents import Document
import os

class BaseMarkitdownLoader(BaseLoader):
    """Base class for Markitdown document loaders."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:  # Specify return type as List[Document]
        from markitdown import MarkItDown

        file_name = os.path.basename(self.file_path)
        file_size = os.path.getsize(self.file_path)
        converter = MarkItDown()
        markdown_content = converter.convert(self.file_path).text_content
        base_metadata = {"source": self.file_path, "file_name": file_name, "file_size": file_size}

        document = Document(page_content=markdown_content, metadata=base_metadata)

        return [document]