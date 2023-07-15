from pathlib import Path

import aiohttp
import aiofiles

from bs4 import BeautifulSoup


async def get_visualization_html(path: Path) -> str:
    async with aiofiles.open(path, "rb") as file:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://urd2.let.rug.nl/~kleiweg/conllu/bin/form",
                    data={"conllu": await file.read()},
                    headers={
                        "Content-Type": "application/octet-stream"
                    }
            ) as response:
                soup = BeautifulSoup(
                    (await response.text()).replace("../../", "https://urd2.let.rug.nl/~kleiweg/"),
                    "lxml"
                )

                soup.find("div", id="top").extract()
                for tag in soup.find_all("div", class_="udcontrol"):
                    tag.extract()

                return str(soup)
