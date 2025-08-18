class Writer:
    def __init__(self, filename):
        self.filename = filename

    def write(self, results):
        with open(self.filename, "w", encoding="utf-8") as f:
            for url, content in results:
                f.write(f"===== {url} =====\n")
                f.write(content[:500])  # فقط ۵۰۰ کاراکتر اول برای کوتاهی
                f.write("\n\n")
