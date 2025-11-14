from langchain_core.documents import Document

from langchain_markitdown import PptxLoader


def test_pptx_loader_returns_full_presentation(test_pptx_file, fake_converter_factory):
    """Ensure full presentations are returned when split_by_page is False."""
    converter = fake_converter_factory(text_content="Slide deck summary")
    loader = PptxLoader(test_pptx_file, converter=converter)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert "test.pptx" in documents[0].metadata["source"]
    assert documents[0].metadata["content_type"] == "presentation_full"


def test_pptx_loader_with_split_by_page(test_pptx_file, fake_converter_factory):
    """Ensure slide splits include page metadata."""
    markdown = "Intro\n<!-- Slide number: 1 -->\nSlide One\n<!-- Slide number: 2 -->\nSlide Two"
    converter = fake_converter_factory(text_content=markdown)
    loader = PptxLoader(test_pptx_file, split_by_page=True, converter=converter)
    documents = loader.load()

    assert isinstance(documents, list)
    assert len(documents) >= 2
    assert isinstance(documents[0], Document)
    assert "page_number" in documents[0].metadata
    assert documents[0].metadata["content_type"] == "presentation_slide"
