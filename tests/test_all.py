import pytest
from unittest.mock import patch
from fetch import Fetcher
from writer import Writer


# ---------------------------
# Tests for fetch.py
# ---------------------------

@pytest.mark.asyncio
async def test_fetch_success(fake_fetch_response, sample_urls):
    """
    Test that Fetcher.fetch works correctly
    when the HTTP request succeeds.
    """
    fetcher = Fetcher([sample_urls[0]])

    # Patch aiohttp.ClientSession.get with the fake_fetch_response fixture
    with patch("aiohttp.ClientSession.get", side_effect=fake_fetch_response):
        results = await fetcher.run()

    # Assertions
    assert isinstance(results, list)
    assert results[0][0] == sample_urls[0]
    assert results[0][1] == "mocked content"


@pytest.mark.asyncio
async def test_fetch_error(fake_session_error, sample_urls):
    """
    Test that Fetcher.fetch correctly handles exceptions
    and returns an error message.
    """
    fetcher = Fetcher([sample_urls[0]])

    result = await fetcher.fetch(fake_session_error, sample_urls[0])

    # Assertions
    assert sample_urls[0] in result[0]
    assert result[1].startswith("Error:")


@pytest.mark.asyncio
async def test_run(monkeypatch, sample_urls):
    """
    Test Fetcher.run with multiple URLs by mocking fetch()
    to avoid making real HTTP requests.
    """
    fetcher = Fetcher(sample_urls)

    async def fake_fetch(session, url):
        return url, f"mocked content for {url}"

    # Replace Fetcher.fetch with fake_fetch
    monkeypatch.setattr(fetcher, "fetch", fake_fetch)

    results = await fetcher.run()

    # Assertions
    assert len(results) == len(sample_urls)
    for (url, content), expected_url in zip(results, sample_urls):
        assert url == expected_url
        assert content.startswith("mocked content")


# ---------------------------
# Tests for writer.py
# ---------------------------

@pytest.mark.asyncio
async def test_writer_writes_file(temp_output_file, sample_results, read_file_content):
    """
    Test that Writer writes results into a file correctly.
    Verifies that:
    - Each URL is included in the file.
    - The content is truncated to 500 characters.
    """
    writer = Writer(str(temp_output_file))
    await writer.write(sample_results)

    content = await read_file_content(temp_output_file)

    # Assertions
    for url, text in sample_results:
        assert f"===== {url} =====" in content
        assert text[:500] in content

    
