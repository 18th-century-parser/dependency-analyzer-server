from pathlib import Path

import aiofiles

from stanza import Pipeline
from stanza.utils.conll import CoNLL

from misc.util import get_temp_file_path
from misc.constants import model_path


nlp = Pipeline("ru", depparse_batch_size=500, depparse_model_path=str(model_path))


def process_text(text: str) -> Path:
    document = nlp(text)
    CoNLL.write_doc2conll(document, conllu_path := get_temp_file_path("conllu"))

    return conllu_path


async def process_text_from_file(path: Path) -> Path:
    async with aiofiles.open(path, "r") as file:
        return process_text(await file.read())
