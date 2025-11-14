from langchain_core.documents import Document

from langchain_markitdown import DocxLoader


def test_docx_loader_returns_single_document(test_docx_file, fake_converter_factory):
    """DocxLoader should return a full document when not splitting."""
    converter = fake_converter_factory(
        text_content="# Heading\n\nParagraph",
        metadata={"producer": "markitdown"},
    )
    loader = DocxLoader(test_docx_file, converter=converter)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert "test.docx" in documents[0].metadata["source"]
    assert documents[0].metadata["content_type"] == "document_full"
    assert documents[0].metadata["markitdown_metadata"]["producer"] == "markitdown"


def test_docx_loader_with_headers(test_docx_file, fake_converter_factory):
    """Header-based splitting should produce multiple sections."""
    converter = fake_converter_factory(
        text_content="# Title\nSection content\n\n## Details\nMore content",
    )
    loader = DocxLoader(test_docx_file, converter=converter)
    documents = loader.load(headers_to_split_on=[("#", "H1"), ("##", "H2")])

    assert len(documents) == 2
    assert all(doc.metadata["content_type"] == "document_section" for doc in documents)


def test_docx_loader_with_split_by_page(test_docx_file, fake_converter_factory):
    """Split-by-page uses the MarkItDown per-page payload."""
    converter = fake_converter_factory(pages=["# Page 1\nAlpha", "# Page 2\nBeta"])
    loader = DocxLoader(test_docx_file, split_by_page=True, converter=converter)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 2
    assert all(isinstance(doc, Document) for doc in documents)
    assert all("page_number" in doc.metadata for doc in documents)
    assert {doc.metadata["page_number"] for doc in documents} == {1, 2}
