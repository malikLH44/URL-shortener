from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import secrets

app = FastAPI(title="URL Shortener")

# Stockage temporaire en mémoire (Phase 2 : PostgreSQL)
links: dict[str, dict] = {}


class LinkIn(BaseModel):
    url: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten")
def shorten(payload: LinkIn):
    code = secrets.token_urlsafe(4)[:6]
    links[code] = {"url": payload.url, "clicks": 0}
    return {"code": code, "short_url": f"/{code}"}


@app.get("/{code}")
def redirect(code: str):
    link = links.get(code)
    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")
    link["clicks"] += 1
    return RedirectResponse(url=link["url"])


@app.get("/stats/{code}")
def stats(code: str):
    link = links.get(code)
    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")
    return {"code": code, "url": link["url"], "clicks": link["clicks"]}