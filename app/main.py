# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.routes import router_v1
from app.core.exception_handler import http_exception_handler

app = FastAPI(title="Services Backend")
app.include_router(router_v1, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Services Backend</title>
        </head>
        <body>
            <h1>Services Backend</h1>
            <p>Backend FastAPI untuk layanan minibank yang konek ke middleware.</p>
            <ul>
                <li><strong>Versi:</strong> 1.0.0</li>
                <li><strong>Dokumentasi:</strong> <a href="/docs">/docs</a></li>
            </ul>
            <p><strong>Made with ❤️ by Choco_Mette</strong></p>
            <img src="https://media.tenor.com/dypucHMixbEAAAAM/patrick-star-no-this-is-patrick.gif" alt="Patrick Star" width="320" height="240" />
        </body>
    </html>
    """

app.add_exception_handler(Exception, http_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)