from pathlib import Path

import aiofiles


async def search(conllu_path: Path, lemma: str | None, dependencies: list[str]) -> list[str]:
    def is_row_matched(row: str) -> bool:
        items = row.split("\t")

        return (
                ((lemma.lower() in items[2].lower()) if lemma else True) and
                ((items[7] in dependencies) if dependencies else True)
        )


    async with aiofiles.open(conllu_path, "r") as file:
        sentence_blocks = map(lambda block: block.split("\n"), (await file.read()).strip().split("\n\n"))

    matched_blocks = filter(lambda block: any(filter(is_row_matched, block[2:])), sentence_blocks)

    return list(map(lambda block: block[0][9:], matched_blocks))
