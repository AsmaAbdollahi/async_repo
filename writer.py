import aiofiles

class Writer:
    def __init__(self, filename):
        self.filename = filename

    async def write(self, results):
        # فایل رو به صورت async باز می‌کنیم
        async with aiofiles.open(self.filename, "w", encoding="utf-8") as f:
            for url, content in results:
                # هر بار async بنویس
                await f.write(f"===== {url} =====\n")
                await f.write(content[:500])  # فقط ۵۰۰ کاراکتر اول برای کوتاهی
                await f.write("\n\n")
