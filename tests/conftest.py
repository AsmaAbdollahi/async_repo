import pytest
import aiofiles
import os


@pytest.fixture
def sample_urls():
    """Dynamic sample URLs"""
    return [
        "http://example.com/page1",
        "http://example.com/page2"
    ]


@pytest.fixture
def sample_results(sample_urls):
    """Dynamic sample results (url, content)"""
    return [
        (sample_urls[0], "content1" * 100),
        (sample_urls[1], "content2" * 100),
    ]


@pytest.fixture
def temp_output_file(tmp_path):
    """
    Provide a temporary output file path.
    Cleanup automatically after the test.
    """
    file_path = tmp_path / "output.txt"
    yield str(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
async def async_file_reader():
    """
    Provide async file reader helper
    """
    async def _reader(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return await f.read()
    yield _reader
