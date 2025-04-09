from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from markitdown import MarkitdownConverter

class BaseMarkitdownLoader(BaseLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> list[Document]:
        """Load file and convert to documents."""
        converter = MarkitdownConverter()
        markdown = converter.convert(self.file_path)
        return [Document(page_content=markdown, metadata={"source": self.file_path})]