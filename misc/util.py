from pathlib import Path
from uuid import uuid4

import aiofiles

from fastapi import UploadFile

from textract import process

from bs4.dammit import UnicodeDammit

from misc.fb2_processor import process_fb2
from misc.constants import temp_dir


def get_temp_file_path(extension: str = None) -> Path:
    return Path(temp_dir, str(uuid4()) + ("" if extension.startswith(".") else ".") + (extension if extension else ""))


def get_plain_text(path: Path) -> str:
    if path.suffix == ".fb2":
        return process_fb2(path)
    else:
        return process(str(path), output_encoding="utf-8").decode("utf-8").replace(chr(160), " ")


async def process_files(files: list[UploadFile]) -> Path:
    async with aiofiles.open(text_file_path := get_temp_file_path("txt"), "a", encoding="utf-8") as text_file:
        for file in files:
            suffix = Path(file.filename).suffix
            if suffix in (".docx", ".odt", ".pdf", ".epub", ".xslx", ".htm", ".html"):
                async with aiofiles.open(temp_file_path := get_temp_file_path(suffix), "wb") as temp_file:
                    await temp_file.write(file.file.read())
            else:
                async with aiofiles.open(
                        temp_file_path := get_temp_file_path(suffix), "w", encoding="utf-8"
                ) as temp_file:
                    contents = file.file.read()
                    try:
                        await temp_file.write(contents.decode("utf-8"))
                    except UnicodeDecodeError:
                        await temp_file.write(
                            UnicodeDammit(contents, ["cp1251", "utf-8"]).unicode_markup
                        )

            await text_file.write(get_plain_text(temp_file_path) + "\n")

    return text_file_path
