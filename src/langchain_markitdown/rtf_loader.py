from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from .base_loader import BaseMarkitdownLoader

class RtfLoader(BaseMarkitdownLoader):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def load(self, headers_to_split_on: Optional[List[str]] = None) -> List[Document]:
        try:
            from markitdown import MarkItDown, StreamInfo
            from markitdown_sample_plugin import RtfConverter

            with open(self.file_path, "rb") as file_stream:
                converter = RtfConverter()
                result = converter.convert(
                    file_stream=file_stream,
                    stream_info=StreamInfo(
                        mimetype="text/rtf", 
                        extension=".rtf", 
                        filename=self._get_file_name(self.file_path)
                    ),
                )

            metadata = {
                "source": self.file_path,
                "file_name": self._get_file_name(self.file_path),
                "file_size": self._get_file_size(self.file_path),
                "conversion_success": True,
            }

            return [Document(page_content=result.text_content, metadata=metadata)]

        except Exception as e:
            raise ValueError(f"Failed to load and convert RTF file: {e}")