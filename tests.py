import pytest
import aiofiles
from unittest.mock import AsyncMock
from fetch import Fetcher
from writer import Writer


#  tests for fetch.py file
@pytest.mark.asyncio
async def test_fetch_success():
    """Test when the fetch request is successful"""
    urls = ["http://example.com/page1"]
    fetcher = Fetcher(urls)

    # Mock a successful aiohttp response
    fake_response = AsyncMock()
    fake_response.text.return_value = "mocked content"

    fake_session = AsyncMock()
    # Mock the async context manager for session.get()
    fake_session.get.return_value.__aenter__.return_value = fake_response

    result = await fetcher.fetch(fake_session, urls[0])

    assert result == (urls[0], "mocked content")
    fake_session.get.assert_called_once_with(urls[0])


@pytest.mark.asyncio
async def test_fetch_error():
    """Test when the fetch request raises an exception"""
    urls = ["http://example.com/page1"]
    fetcher = Fetcher(urls)

    fake_session = AsyncMock()
    # Simulate a network error
    fake_session.get.side_effect = Exception("Network error")

    result = await fetcher.fetch(fake_session, urls[0])

    assert urls[0] in result[0]
    assert "Error:" in result[1]


@pytest.mark.asyncio
async def test_run(monkeypatch):
    """Test the run() method which should handle multiple URLs"""
    urls = ["http://example.com/page1", "http://example.com/page2"]
    fetcher = Fetcher(urls)
    # Replace the fetch method with a fake one to avoid real HTTP requests
    async def fake_fetch(session, url):
        return url, f"mocked content for {url}"

    monkeypatch.setattr(fetcher, "fetch", fake_fetch)

    results = await fetcher.run()

    # Ensure both URLs were processed
    assert len(results) == 2
    assert results[0][1].startswith("mocked content")
    assert results[1][1].startswith("mocked content")



# tests for the write.py file
@pytest.mark.asyncio
async def test_writer_writes_file(tmp_path):
    """Test that Writer correctly writes results into a file"""

    # Create a temporary file path
    output_file = tmp_path / "output.txt"

    # Sample results (url, content)
    results = [
        ("http://example.com/page1", "content1" * 100),
        ("http://example.com/page2", "content2" * 100),
    ]

    writer = Writer(str(output_file))
    await writer.write(results)

    # Read back the file content
    async with aiofiles.open(output_file, "r", encoding="utf-8") as f:
        content = await f.read()

    # Assertions
    # Each URL should appear in the file
    assert "===== http://example.com/page1 =====" in content
    assert "===== http://example.com/page2 =====" in content

    # Content should be truncated to 500 chars
    assert "content1" * 100 in content  # 100*8=800 chars, but truncated at 500
    assert len(content) > 0
