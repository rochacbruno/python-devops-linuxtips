from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, RootModel

from core import format_word, get_history, increment_counter, verify_basic_auth

app = FastAPI()


class ResponseModel(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the simple HTML/CSS/JS frontend.
    """
    template_path = Path(__file__).parent / "templates" / "index.html"
    html_content = template_path.read_text()
    return html_content


@app.get("/hello")
@app.get("/hello/{word}")
async def hello(word: str = "world") -> ResponseModel:
    """
    Return a greeting message with the formatted word.

    Args:
        word: The word to include in the greeting (default: "world")

    Returns:
        JSON response with the greeting message
    """
    formatted_word = format_word(word)
    path = f"/hello/{word}" if word != "world" else "/hello"

    # Track the request in history
    increment_counter(path)

    return ResponseModel(message=f"Hello {formatted_word}")


class HistoryResponse(RootModel[dict[str, int]]): ...


@app.get("/history", response_model=HistoryResponse)
async def history(authorization: str | None = Header(None)) -> dict:
    """
    Return the request history.

    Requires Basic Authentication with admin:Batata123

    Returns:
        JSON response with path counters
    """

    if not verify_basic_auth(authorization):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    return get_history()
