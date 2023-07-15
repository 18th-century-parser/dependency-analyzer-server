from fastapi import FastAPI, Request, UploadFile, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from engine.dependency_analyzer import process_text, process_text_from_file
from engine.visualization import get_visualization_html
from engine.search import search
from misc.util import process_files


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"response": "I <3 Yandex"}


@app.post("/api/files")
async def api_files(files: list[UploadFile]):
    text_file_path = await process_files(files)

    conllu_path = await process_text_from_file(text_file_path)

    response_html = await get_visualization_html(conllu_path)

    return HTMLResponse(response_html)


@app.post("/api/text")
async def api_text(request: Request):
    conllu_path = process_text((await request.form()).get("text"))

    response_html = await get_visualization_html(conllu_path)

    return HTMLResponse(response_html)


@app.post("/api/search")
async def api_search(
        files: list[UploadFile], lemma: str = Body(embed=True), dependencies: str = Body(embed=True)
):
    text_file_path = await process_files(files)

    conllu_path = await process_text_from_file(text_file_path)

    return {
        "sentences": await search(
            conllu_path,
            None if lemma == "0" else lemma,
            [] if dependencies == "0" else dependencies.split(",")
        )
    }
