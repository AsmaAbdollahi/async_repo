import pytest
from writer import Writer


@pytest.mark.asyncio
async def test_writer_writes_file(sample_results, temp_output_file, async_file_reader):
    """Writer should write results into file with truncated content"""

    writer = Writer(temp_output_file)
    await writer.write(sample_results)

    content = await async_file_reader(temp_output_file)

    for url, text in sample_results:
        assert f"===== {url} =====" in content
        assert text[:500] in content