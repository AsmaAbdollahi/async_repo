import pytest
from unittest import mock
from fetch import Fetcher


@pytest.mark.asyncio
async def test_fetch_success(sample_urls):
    """Fetch should return mocked content when patched"""

    with mock.patch("aiohttp.ClientSession.get") as mock_get:
        mock_resp = mock.AsyncMock()
        mock_resp.text.return_value = "mocked content"
        mock_get.return_value.__aenter__.return_value = mock_resp

        fetcher = Fetcher([sample_urls[0]])
        results = await fetcher.run()

    assert results[0][0] == sample_urls[0]
    assert results[0][1] == "mocked content"


@pytest.mark.asyncio
async def test_fetch_error(sample_urls):
    """Fetch should return error message if request fails"""

    fetcher = Fetcher([sample_urls[0]])
    fake_session = mock.AsyncMock()
    fake_session.get.side_effect = Exception("Network error")

    result = await fetcher.fetch(fake_session, sample_urls[0])

    assert sample_urls[0] in result[0]
    assert result[1].startswith("Error:")


@pytest.mark.asyncio
async def test_run_multiple(monkeypatch, sample_urls):
    """run() should return results for multiple URLs"""

    fetcher = Fetcher(sample_urls)

    async def fake_fetch(session, url):
        return url, f"mocked content for {url}"

    monkeypatch.setattr(fetcher, "fetch", fake_fetch)

    results = await fetcher.run()

    assert len(results) == len(sample_urls)
    for (url, content), expected_url in zip(results, sample_urls):
        assert url == expected_url
        assert content.startswith("mocked content")
