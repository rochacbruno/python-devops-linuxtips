"""FastAPI application for Hello API.

This module contains the FastAPI application instance and all HTTP endpoints.
Business logic is in core.py.
"""

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
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-top: 0;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        #response {
            margin-top: 20px;
            padding: 15px;
            background-color: #e7f3ff;
            border-left: 4px solid #007bff;
            border-radius: 4px;
            display: none;
        }
        #response.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello API</h1>
        <input type="text" id="wordInput" placeholder="Type a word..." />
        <button onclick="sayHello()">Say Hello</button>
        <div id="response">
            Response: <span id="responseText"></span>
        </div>
    </div>
    <script>
        async function sayHello() {
            const word = document.getElementById('wordInput').value || 'world';
            const responseDiv = document.getElementById('response');
            const responseText = document.getElementById('responseText');

            try {
                const response = await fetch(`/hello/${word}`);
                const data = await response.json();
                responseText.textContent = data.message;
                responseDiv.classList.add('show');
            } catch (error) {
                responseText.textContent = 'Error: ' + error.message;
                responseDiv.classList.add('show');
            }
        }

        document.getElementById('wordInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sayHello();
            }
        });
    </script>
</body>
</html>
    """
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
