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


import pytest
import aiofiles
import os

@pytest.fixture
def async_file_reader():
    """Fixture to read file content asynchronously"""
    async def _reader(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return await f.read()
    return _reader


@pytest.fixture
def temp_output_file(tmp_path):
    """Fixture to provide temp output file path with cleanup"""
    file_path = tmp_path / "output.txt"
    yield str(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
