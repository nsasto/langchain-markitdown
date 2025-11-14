from langchain_core.documents import Document

from langchain_markitdown import XlsxLoader


def test_xlsx_loader_full_workbook(test_xlsx_file, fake_converter_factory):
    """XlsxLoader should return a single workbook document by default."""
    converter = fake_converter_factory(text_content="| A | B |\n| 1 | 2 |")
    loader = XlsxLoader(test_xlsx_file, converter=converter)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert "test.xlsx" in documents[0].metadata["source"]
    assert documents[0].metadata["content_type"] == "workbook"


def test_xlsx_loader_with_split_by_page(test_xlsx_file, fake_converter_factory):
    """Split-by-page should surface worksheet metadata."""
    converter = fake_converter_factory(pages=["Sheet1 content", "Sheet2 content"])
    loader = XlsxLoader(test_xlsx_file, split_by_page=True, converter=converter)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 2
    assert isinstance(documents[0], Document)
    assert "page_number" in documents[0].metadata
    assert documents[0].metadata["content_type"] == "worksheet"
    assert documents[0].metadata["page_number"] == 1


def test_xlsx_loader_split_fallback(test_xlsx_file, fake_converter_factory):
    """When MarkItDown lacks page hints, fall back to parsing markdown."""
    markdown = "Intro\n\n## Sheet One\nTable one\n\n## Sheet Two\nTable two"
    converter = fake_converter_factory(text_content=markdown)
    loader = XlsxLoader(test_xlsx_file, split_by_page=True, converter=converter)
    documents = loader.load()

    assert len(documents) == 3  # Intro block + two sheets
    assert documents[1].metadata["worksheet"] == "Sheet One"
    assert documents[2].metadata["worksheet"] == "Sheet Two"
