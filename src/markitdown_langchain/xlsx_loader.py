from typing import List
from langchain_core.documents import Document
from src.markitdown_langchain.base_loader import BaseMarkitdownLoader

class XlsxLoader(BaseMarkitdownLoader):
    """Loader for XLSX files."""

    def __init__(self, file_path: str, split_by_page: bool = False):
        """Initialize with file path and split_by_page option."""
        super().__init__(file_path)
        self.split_by_page = split_by_page

    def load(self) -> List[Document]:
        """Load and convert XLSX file to Markdown.
        If split_by_page is True, each sheet is a separate document.
        If split_by_page is False, all sheets are combined into a single document.
        """
        from markitdown import MarkItDown
        converter = MarkItDown()
        markdown_content = converter.convert(self.file_path).text_content
        
        documents = []
        # Split Markdown content by sheet headers
        sheet_contents = markdown_content.split("## ")
        for sheet_content in sheet_contents[1:]:
            lines = sheet_content.splitlines()
            sheet_name = lines[0].strip()  # First line is the sheet name
            table_content = '\n'.join(lines[1:])  # Remaining lines are the table
            
            metadata = {"source": self.file_path, "file_name": self._get_file_name(), "page_number": sheet_name}
            doc = Document(page_content=table_content, metadata=metadata)
            documents.append(doc)
            return documents
        else:
            metadata = {"source": self.file_path, "file_name": self._get_file_name()}
            return [Document(page_content=markdown_content, metadata=metadata)]

    def _get_file_name(self) -> str:
        """Extract the file name from the file path."""
        import os
        return os.path.basename(self.file_path)