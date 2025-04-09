from markitdown_langchain.base_loader import BaseMarkitdownLoader

class AudioLoader(BaseMarkitdownLoader):
    """Loader for audio files."""

    def __init__(self, file_path: str):
        """Initialize with file path."""
        super().__init__(file_path)