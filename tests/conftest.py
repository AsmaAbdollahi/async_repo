import pytest
import aiofiles
import os
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager

@pytest.fixture
def sample_urls():
    """Provide a list of sample URLs for tests"""
    return [
        "http://example.com/page1",
        "http://example.com/page2"
    ]
@pytest.fixture
def sample_results(sample_urls):
    """Provide sample fetch results for Writer tests"""
    return [
        (sample_urls[0], "content1" * 100),
        (sample_urls[1], "content2" * 100),
    ]
@pytest.fixture
def fake_fetch_response():
    """
    Fixture: simulates a successful HTTP fetch response.
    It mocks aiohttp.ClientSession.get to return a fake response object.
    """
    @asynccontextmanager
    async def fake_get(*args, **kwargs):
        class FakeResponse:
            async def text(self):
                return "mocked content"
        yield FakeResponse()
    return fake_get

@pytest.fixture
def fake_session_error():
    """
    Fixture: simulates a network error when calling session.get().
    Used to test error handling in the Fetcher.
    """
    fake_session = AsyncMock()
    fake_session.get.side_effect = Exception("Network error")
    return fake_session
@pytest.fixture
def temp_output_file(tmp_path):
    """
    Fixture: creates a temporary file for Writer to write into.
    After the test finishes, the file is deleted automatically.
    """
    path = tmp_path / "output.txt"
    yield path
    if path.exists():
        os.remove(path)


@pytest.fixture
def read_file_content():
    """
    Fixture: helper to asynchronously read the content of a file.
    Returns an async function that can be called inside tests.
    """
    async def _reader(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return await f.read()
    return _reader
